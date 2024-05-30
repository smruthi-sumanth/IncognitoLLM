import os

import modal
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider, NlpEngine
from presidio_anonymizer import AnonymizerEngine
from common import app, volume, MODEL_DIR
import spacy
from presidio_analyzer.predefined_recognizers import AzureAILanguageRecognizer
from typing import Tuple
from pydantic import BaseModel

class AnalyzerInput(BaseModel):
    text: str
    entities: list = None
    language: str = "en"
    score_threshold: float = 0.5

@app.cls(container_idle_timeout=1200, gpu="T4", enable_memory_snapshot=True)
class AzureAIAnalyzer:
    def __init__(self):
        self.analyzer = self.initialize_analyzer()
        self.anonymizer = AnonymizerEngine()

    def anonymize(self, text):
        """
        Anonymize the given text.

        Args:
            text (str): The text to anonymize.

        Returns:
            str: The anonymized text.
        """
        # Analyze the text using the analyzer engine
        analyzer_results = self.analyzer.analyze(text=text, language='en')

        # Anonymize the text using the analyzer results
        anonymized_text = self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results)

        return anonymized_text

    def initialize_analyzer(self):
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


@app.cls(container_idle_timeout=1200, gpu="T4", volumes={MODEL_DIR: volume})
class FlairAnalyzer:
    def __init__(self):
        self.engine_and_registry = self.create_nlp_engine_with_flair()
        self.anonymizer = AnonymizerEngine()
        self.analyzer = None
        if isinstance(self.engine_and_registry, tuple):
            print("Engine and registry created successfully.")

    @modal.enter()
    def load_engine(self):
        self.analyzer = AnalyzerEngine(nlp_engine=self.engine_and_registry[0], registry=self.engine_and_registry[1])
        print(self.analyzer.get_supported_entities())
        print(f"{self.__class__.__name__} loaded successfully.")

    def create_nlp_engine_with_flair(self,
            model_path: str = None
    ) -> Tuple[NlpEngine, RecognizerRegistry]:
        """
        Instantiate an NlpEngine with a FlairRecognizer and a small spaCy model.
        The FlairRecognizer would return results from Flair models, the spaCy model
        would return NlpArtifacts such as POS and lemmas.
        """
        from flair_ner import FlairRecognizer

        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()

        # there is no official Flair NlpEngine, hence we load it as an additional recognizer

        if not spacy.util.is_package("en_core_web_sm"):
            spacy.cli.download("en_core_web_sm")
        # Using a small spaCy model + a Flair NER model
        flair_recognizer = FlairRecognizer()
        nlp_configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
        }
        registry.add_recognizer(flair_recognizer)
        registry.remove_recognizer("SpacyRecognizer")

        nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()

        return nlp_engine, registry


    @modal.web_endpoint(method="POST")
    async def flair_text_analyzer(self, item: AnalyzerInput) -> list:
        """
        Analyze the given text using the Flair analyzer.

        Args:
            text (str): The text to analyze.

        Returns:
            str: The analysis results.
        """

        entitites = item.entities if item.entities else self.analyzer.get_supported_entities()
        results = self.analyzer.analyze(
            text=item.text,
            language=item.language,
            entities=entitites,
            score_threshold=item.score_threshold,
            return_decision_process=True,
        )
        # print("RESULTS: ", results)
        # for result in results:
        #     print(result)
        #     print(result.analysis_explanation)
        return results





