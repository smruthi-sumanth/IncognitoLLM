model_config = [{"lang_code": "en", "model_name": {
    "spacy": "en_core_web_sm",  # use a small spaCy model for lemmas, tokens etc.
    "transformers": "Venkatesh4342/NER-Indian-xlm-roberta",  # use a BERT model for embeddings
    }
}]

PRESIDIO_SUPPORTED_ENTITIES = [
        "LOCATION",
        "PERSON",
        "ORGANIZATION",
        "AGE",
        "PHONE_NUMBER",
        "EMAIL",
        "DATE_TIME",
        "ZIP",
        "PROFESSION",
        "USERNAME",
        "ID"
    ],
