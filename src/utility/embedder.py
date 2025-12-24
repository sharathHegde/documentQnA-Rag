from typing import List
import os
import time
from pathlib import Path
from dotenv import load_dotenv

from openai import AzureOpenAI

class Embedder:
    def __init__(self):
        """Initialize embedder with Azure OpenAI."""
        # Load environment variables from .env file
        dotenv_path = Path(__file__).parent.parent / '.env'
        load_dotenv(dotenv_path)
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_FOR_EMBEDDING")
        self.azure_openai_key = os.getenv("AZURE_OPENAI_KEY_FOR_EMBEDDING")
        self.client = AzureOpenAI(
            api_key=self.azure_openai_key,
            api_version="2024-10-21",
            azure_endpoint=self.azure_openai_endpoint
        )
        
        self.deployment_name = "text-embedding-3-large"
        self.dimension = 1024  # Assuming the embedding dimension for "text-embedding-3-large"
        self.batch_size = 16  # Default batch size
        
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.deployment_name,
                dimensions=self.dimension
            )
            
            return response.data[0].embedding
        
        except Exception as e:
            raise

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Query text
        
        Returns:
            Query embedding vector
        """
        return self.embed_text(query)