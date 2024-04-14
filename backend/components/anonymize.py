# For console output
from pprint import pprint
from streamlit import cache_data, cache_resource
# For Presidio
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_analyzer.predefined_recognizers import AzureAILanguageRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import TransformersNlpEngine

# For extracting text
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine

from backend.utils.config import model_config

# For updating the PDF
from pikepdf import Pdf, AttachedFileSpec, Name, Dictionary, Array
def initialize_analyzer():
    """
    Initialize the Presidio analyzer engine.

    Returns:
        AnalyzerEngine: The Presidio analyzer engine.
    """
    # Initialize the Presidio analyzer engine
    nlp_engine = TransformersNlpEngine(models=model_config)
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine)

    azure_recognizer = AzureAILanguageRecognizer()
    analyzer.registry.add_recognizer(azure_recognizer)
    # Add the pattern recognizer to the analyzer
    pattern_recognizer = PatternRecognizer(supported_entity="PHONE_NUMBER", supported_language="en")
    analyzer.registry.add_recognizer(pattern_recognizer)
    return analyzer

def analyze_text(text: bytes):
    """
    Analyze the text using the Presidio analyzer engine.

    Args:
        text (bytes): The text to analyze.

    Returns:
        list: The results of the analysis.
    """
    analyzed_character_sets = []
    analyzer = initialize_analyzer()
    for page_layout in extract_pages("./sample_data/sample.pdf"):
        for text_container in page_layout:
            if isinstance(text_container, LTTextContainer):

                # The element is a LTTextContainer, containing a paragraph of text.
                text_to_anonymize = text_container.get_text()

                # Analyze the text using the analyzer engine
                analyzer_results = analyzer.analyze(text=text_to_anonymize, language='en')

                if text_to_anonymize.isspace() == False:
                    print(text_to_anonymize)
                    print(analyzer_results)

                characters = list([])

                # Grab the characters from the PDF
                for text_line in filter(lambda t: isinstance(t, LTTextLine), text_container):
                    for character in filter(lambda t: isinstance(t, LTChar), text_line):
                        characters.append(character)

                # Slice out the characters that match the analyzer results.
                for result in analyzer_results:
                    start = result.start
                    end = result.end
                    analyzed_character_sets.append({"characters": characters[start:end], "result": result})
