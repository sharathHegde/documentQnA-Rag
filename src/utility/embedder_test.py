import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utility.embedder import Embedder

def main():
    print("Running embedder tests...")
    embedder = Embedder()
    sample_text = "This is a sample text for embedding."
    embedding = embedder.embed_text(sample_text)
    print(f"Embedding for sample text: {embedding}")

if __name__ == "__main__":
    main()