import os
import weaviate
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.weaviate import WeaviateVectorStore

def load_apostilas():
    """Carrega e indexa apostilas em background no Weaviate Cloud."""
    client = weaviate.Client(
        url=f"https://{os.environ['WEAVIATE_URL']}",
        auth_client_secret=weaviate.AuthApiKey(api_key=os.environ['WEAVIATE_API_KEY'])
    )

    vector_store = WeaviateVectorStore(weaviate_client=client, index_name="ABAPDocs")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if os.path.exists("data/apostilas"):
        documents = SimpleDirectoryReader("data/apostilas").load_data()
        if documents:
            VectorStoreIndex.from_documents(documents, storage_context=storage_context)
            print(f"📚 Apostilas indexadas no Weaviate ({len(documents)} docs).")
