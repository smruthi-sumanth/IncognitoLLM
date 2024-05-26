from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.predefined_recognizers import AzureAILanguageRecognizer


def initialize_analyzer():
    """
    Initialize the Presidio analyzer engine.

    Returns:
        AnalyzerEngine: The Presidio analyzer engine.
    """
    # Initialize the Presidio analyzer engine
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
    }

    provider = NlpEngineProvider(nlp_configuration=configuration)
    analyzer = AnalyzerEngine(nlp_engine=provider.create_engine())
    azure_recognizer = AzureAILanguageRecognizer()
    analyzer.registry.add_recognizer(azure_recognizer)

    return analyzer
