
import os
import sys
from pathlib import Path
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from azure.search.documents import SearchClient
from enum import Enum

from utility.embedder import Embedder

#define an enum for search types if needed in future
class SearchType(Enum):
    TEXT = 1
    VECTOR = 2
    HYBRID = 3

class RetrievalManager:
    #Constructor and methods for RetrievalManager
    def __init__(self):
        # Load environment variables from .env file
        dotenv_path = Path(__file__).parent.parent / '.env'
        load_dotenv(dotenv_path)
        
        #Load env variables and config
        self.search_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
        self.search_index = os.getenv("AZURE_SEARCH_INDEX")
        self.search_datasource = os.getenv("AZURE_SEARCH_DATASOURCE")
        self.search_skillset = os.getenv("AZURE_SEARCH_SKILLSET")
        self.search_indexer = os.getenv("AZURE_SEARCH_INDEXER")
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_FOR_EMBEDDING")
        self.search_credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY",""))
        self.azure_openai_key = os.getenv("AZURE_OPENAI_KEY_FOR_EMBEDDING")
        self.blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
        self.blob_container_name = os.getenv("AZURE_BLOB_CONTAINER")
        # Search index client initialization for executing Azure Search operations
        self.search_client = SearchClient(
            endpoint=self.search_endpoint,
            index_name=self.search_index,
            credential=self.search_credential
        )

        self.embedder = Embedder()
    def search_documents(self, query, top_k=5, search_type=SearchType.TEXT):
        # Perform a search query against the Azure Search index
        results = None
        match search_type:
            case SearchType.HYBRID:
                query_vector = self.embedder.embed_query(query)
                results = self.search_client.search(
                    search_text=query,
                    vector_queries=[{
                        "kind": "vector",
                        "vector": query_vector,
                        "k": top_k,
                        "fields": "text_vector"
                    }],
                    top=top_k,
                    select=["title", "chunk","chunk_id","parent_id"]
                )
            case SearchType.VECTOR:
                query_vector = self.embedder.embed_query(query)
                results = self.search_client.search(
                    search_text=None,
                    vector_queries=[{
                        "kind": "vector",
                        "vector": query_vector,
                        "k": top_k,
                        "fields": "text_vector"
                    }],
                    top=top_k,
                    select=["title", "chunk","chunk_id","parent_id"]
                )
            case SearchType.TEXT:
                results = self.search_client.search(
                    search_text=query,
                    top=top_k,
                    select=["title", "chunk","chunk_id","parent_id"]
                )

        return [
                {
                    "title": doc.get("title", ""),
                    "chunk": doc.get("chunk", ""),
                    "chunk_id": doc.get("chunk_id", 0),
                    "parent_id": doc.get("parent_id", 0),
                    "score": doc.get("@search.score", 0.0)
                }
                for doc in results
        ]
    
    def search_documents_with_vectors(self, query_text, query_vector, top_k=5):
        # Perform a vector search query against the Azure Search index
        results = self.search_client.search(
            search_text="*",
            vector={"value": query_vector, "k": top_k, "fields": "text_vector"},
            select=["title", "chunk","chunk_id","parent_id"]
        )

        return [
                {
                    "title": doc.get("title", ""),
                    "chunk": doc.get("chunk", ""),
                    "chunk_id": doc.get("chunk_id", 0),
                    "parent_id": doc.get("parent_id", 0),
                    "score": doc.get("@search.score", 0.0)
                }
                for doc in results
        ]