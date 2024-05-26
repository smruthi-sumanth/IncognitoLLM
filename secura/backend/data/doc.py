from llama_index.core.storage.docstore.simple_docstore import SimpleDocumentStore
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core import (
    SimpleDirectoryReader,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)
import faiss
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
d = 1536
faiss_index = faiss.IndexFlatL2(d)
# Load the documents from the SimpleDocumentStore
from dotenv import load_dotenv
import os
load_dotenv()

vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
docstore = SimpleDocumentStore.from_persist_path("./docstore.json")
documents = docstore.docs
docs = []
for doc in documents:
    docs.append(documents[doc])

print(len(docs), type(docs[0]), docs[0].metadata)
# create a new index

index = VectorStoreIndex(nodes=docs)
retriver = index.as_retriever()
print(retriver.retrieve("indian penal code"))
