from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import Document
from llama_index.llms.llama_api import LlamaAPI
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
from llama_index.core.storage.docstore.simple_docstore import SimpleDocumentStore
import time
import pandas as pd
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests


def extract_text_from_url(url):
    try:
        # Fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.content

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        target = soup.find("div", class_="akoma-ntoso")
        citation = soup.find("div", class_="covers").findChildren("a")
        if len(citation) != 2:
            raise Exception("Error parsing citation information.")
        citation = {"citations": citation[0].text, "cited by": citation[1].text}
        return target.find("span", class_="akn-body").get_text(separator="\n\n", strip=True), citation

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return ""


if __name__ == "__main__":
    batch_size = 64
    embed_model = VoyageEmbedding(model_name="voyage-law-2",
                                  voyage_api_key="pa-wKyQ5fdcznsWKUwI4O6Vh6wv2id7STRkP6MgGZMTDmw")
    llm = LlamaAPI(api_key="LL-VKaeJSiyL9m3GmUd4UmuegM1l3rAsknYs5qB0ui1vBCaHFNG7DAaMktHxPFdy83k",
                   model="mistral-7b-instruct")
    df = pd.read_csv("indian_laws_and_acts.csv")
    text_splitter = SemanticSplitterNodeParser(
        buffer_size=3, breakpoint_percentile_threshold=95, embed_model=embed_model
    )
    dataset_path = f"hub://p1utoze/indian_acts"
    vector_store = DeepLakeVectorStore(
        dataset_path=dataset_path,
        overwrite=True,
        exec_option="compute_engine",
        ingestion_batch_size=batch_size,
    )

    pipeline = IngestionPipeline(
        transformations=[text_splitter, embed_model],
        vector_store=vector_store,
    )

    if os.path.exists("./cache"):
        pipeline.load("./cache")

    documents = []

    docstore = SimpleDocumentStore()
    if not os.path.exists("./docstores"):
        try:
            for idx in tqdm(df.index, desc="Processing URLs"):
                text, cite = extract_text_from_url(df.loc[idx, "url"])
                metadata = df.loc[idx, :].to_dict() | cite  # Merge the metadata dict with the cite information
                doc = Document(text=text, metadata=metadata)
                documents.append(doc)
                time.sleep(0.8)
                if idx % batch_size == 0 and idx:
                    docstore.add_documents(documents)
                    docstore.persist("./docstores")
                    documents = []

            docstore.add_documents(documents)
            docstore.persist("./docstores")

        except Exception as e:
            os.remove("./docstores")
    else:
        docstore = SimpleDocumentStore.from_persist_dir(persist_dir="./docstores")
        documents = docstore.docs
    print(documents[0].metadata)
    pipeline.persist("./cache", cache_name="indian_acts")
