import os, weaviate
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.weaviate import WeaviateVectorStore

def load_apostilas():
    """Carrega apostilas locais e indexa no Weaviate em background."""
    client = weaviate.Client(
        url=os.getenv("WEAVIATE_URL"),
        auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))
    )

    vector_store = WeaviateVectorStore(weaviate_client=client, index_name="ABAPDocs")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if os.path.exists("data/apostilas"):
        documents = SimpleDirectoryReader("data/apostilas").load_data()
        if documents:
            VectorStoreIndex.from_documents(documents, storage_context=storage_context)
            print(f"📚 Apostilas indexadas ({len(documents)} docs).")
