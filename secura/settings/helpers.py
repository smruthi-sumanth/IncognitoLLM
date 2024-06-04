from presidio_anonymizer import AnonymizerEngine
import streamlit as st
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer import RecognizerResult
from typing import List, Optional
from enum import Enum
from .utils import markdown_insert_images
import requests, tempfile
from .config import ANALYZER_INFERENCE_URL
from sqlalchemy import create_engine
from .config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
import pymupdf4llm
from bs4 import BeautifulSoup
import markdown, re, random

class ModelType(Enum):
    """Model types for text analysis."""
    FLAIR = "flair"
    AZURE = "azure"
    TRANSFORMERS = "transformers"

def enhance_line_breaks(text):
    # Replace single line breaks with space
    text = text.replace('\n', ' ')
    # Replace double spaces with paragraph separator
    text = text.replace('  ', '\n\n')
    return text


def markdown_table_to_csv(markdown_table):
    lines = markdown_table.split("\n")
    headers = lines[0].strip("|").split("|")[1:-1]
    rows = lines[2:-1]
    csv_rows = []
    for row in rows:
        cells = row.strip("|").split("|")[1:-1]
        csv_row = ",".join(cells).strip()
        csv_rows.append(csv_row)
    csv_content = ",".join(headers) + "\n" + "\n".join(csv_rows)
    return csv_content


# Function to find and replace Markdown tables with CSV
def replace_markdown_tables_with_csv(text):
    # Define regex pattern for Markdown tables
    pattern = r"\|\n(?:.*?\|.*?)+"
    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        # Convert Markdown table to CSV
        csv_content = markdown_table_to_csv(match)
        # Replace Markdown table with CSV in the original text
        text = text.replace(match, csv_content)

    return text


def redact_encrypted_text(enc_txt):
    # Replace encrypted text with REDACTED
    size = len(enc_txt)
    if size < 4:
        return enc_txt[0] + "X" * (size - 1)
    redact_len = random.randint(1, 5)
    res = enc_txt[:redact_len] + "X" * (size - redact_len)
    return res

def convert_markdown_to_plain_text(md_content):
    # Convert Markdown to HTML
    html = markdown.markdown(md_content)

    # Parse HTML to handle tables
    soup = BeautifulSoup(html, "html.parser")
    plain_text = soup.get_text()
    # print(plain_text)

    # Enhance line breaks
    plain_text = enhance_line_breaks(plain_text)

    return plain_text


@st.cache_resource
def init_db_engine():
    """Initialize database engine."""
    return create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        connect_args={
            'sslmode': 'require',
        }
    )


@st.cache_resource
def anonymizer_engine():
    """Return AnonymizerEngine."""
    return AnonymizerEngine()


@st.cache_data
def pdf_to_text(pdf_path: str):
    """Convert PDF to text."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with tempfile.NamedTemporaryFile(dir=temp_dir, suffix=".pdf", delete=False) as tmp_pdf:
            tmp_pdf.write(pdf_path)
            tmp_pdf.flush()
            pdf_path = tmp_pdf.name
            text_data = pymupdf4llm.to_markdown(pdf_path, write_images=True)
            # print(os.listdir(temp_dir))
            # print(os.getcwd())
            md = markdown_insert_images(text_data, dir_name=temp_dir)
            return text_data, md


@st.cache_data
def text_analyze(text: str, language: str = "en", entities: List[str] = None, score_threshold: float = 0.35):
    """Analyze text using Presidio Analyzer."""
    response = requests.post(
        ANALYZER_INFERENCE_URL,
        json={
            "text": text,
            "language": language,
            "entities": entities,
            "score_threshold": score_threshold,
        },
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    analyis_results = [RecognizerResult(**d) for d in response.json()]

    return analyis_results


def anonymize(
        text: str,
        operator: str,
        analyze_results: List[RecognizerResult],
        mask_char: Optional[str] = None,
        number_of_chars: Optional[int] = None,
        encrypt_key: Optional[str] = None,
):
    """Anonymize identified input using Presidio Anonymizer.
    :param text: Full text
    :param operator: Operator name
    :param mask_char: Mask char (for mask operator)
    :param number_of_chars: Number of characters to mask (for mask operator)
    :param encrypt_key: Encryption key (for encrypt operator)
    :param analyze_results: list of results from presidio analyzer engine
    """

    if operator == "mask":
        operator_config = {
            "type": "mask",
            "masking_char": mask_char,
            "chars_to_mask": number_of_chars,
            "from_end": False,
        }

    # Define operator config
    elif operator == "encrypt":
        operator_config = {"key": encrypt_key}
    elif operator == "highlight":
        operator_config = {"lambda": lambda x: x}
    else:
        operator_config = None

    # Change operator if needed as intermediate step
    if operator == "highlight":
        operator = "custom"
    elif operator == "synthesize":
        operator = "replace"
    else:
        operator = operator

    res = anonymizer_engine().anonymize(
        text,
        analyze_results,
        operators={"DEFAULT": OperatorConfig(operator, operator_config)},
    )
    return res


def annotate(text: str, analyze_results: List[RecognizerResult]):
    """Highlight the identified PII entities on the original text
    :param text: Full text
    :param analyze_results: list of results from presidio analyzer engine
    """
    tokens = []

    # Use the anonymizer to resolve overlaps
    results = anonymize(
        text=text,
        operator="highlight",
        analyze_results=analyze_results,
    )
    print(results)

    # sort by start index
    results = sorted(results.items, key=lambda x: x.start)
    for i, res in enumerate(results):
        if i == 0:
            tokens.append(text[: res.start])

        # append entity text and entity type
        tokens.append((text[res.start: res.end], res.entity_type))

        # if another entity coming i.e. we're not at the last results element, add text up to next entity
        if i != len(results) - 1:
            tokens.append(text[res.end: results[i + 1].start])
        # if no more entities coming, add all remaining text
        else:
            tokens.append(text[res.end:])
    return tokens



if __name__ == "__main__":
    text = "HI I am JaySON and I live in bengaluru. My aadhar card number is: 222818318317"

    results = text_analyze(text)
    print(results)
    res = anonymize(text, "mask", analyze_results=results, mask_char="X", number_of_chars=3)
    print(res)
