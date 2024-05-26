from presidio_anonymizer import AnonymizerEngine
import streamlit as st
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer import RecognizerResult
from typing import List, Optional
from enum import Enum
from .utils import markdown_insert_images
import requests, tempfile
import pymupdf4llm
from .config import ANALYZER_INFERENCE_URL
import os


class ModelType(Enum):
    """Model types for text analysis."""
    FLAIR = "flair"
    AZURE = "azure"
    TRANSFORMERS = "transformers"


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
def text_analyze(text: str, language: str = "en", model_type: ModelType = None):
    """Analyze text using Presidio Analyzer."""
    response = requests.post(
        ANALYZER_INFERENCE_URL,
        json={"text": text, "language": language},
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
