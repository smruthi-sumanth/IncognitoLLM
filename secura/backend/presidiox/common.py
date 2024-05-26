import os

import modal, spacy
from dotenv import load_dotenv
load_dotenv()

def download_model_weights() -> None:
    from huggingface_hub import snapshot_download

    snapshot_download(repo_id=os.environ["HF_MODEL_NAME"])

def download_spacy_model() -> None:
    spacy.cli.download("en_core_web_sm")

image = (
    modal.Image.debian_slim(python_version="3.9")
    .pip_install(
        "azure-ai-textanalytics==5.3.0",
        "huggingface-hub==0.23.1",
        "transformers==4.41.1",
        "presidio-analyzer==2.2.354",
        "presidio-anonymizer==2.2.354",
        "python-dotenv==1.0.1",
        "flair==0.13.1",
        "scipy==1.10.1",
    ).workdir("/securax")
    .copy_local_file("flair_ner.py", "/securax/flair_ner.py")
    .env({"FLAIR_CACHE_ROOT": "/vol/model_files"})
    .run_function(download_spacy_model)
    # .run_function(download_model_weights)
)
volume = modal.Volume.from_name("hf_local_models", create_if_missing=True)

MODEL_DIR = "/vol/model_files"

app = modal.App("presidio-analyzers", image=image, volumes={MODEL_DIR: volume})
