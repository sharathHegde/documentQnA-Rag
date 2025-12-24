
import os
import sys
import argparse
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from ingestion.ingestion_manager import IngestionManager


def main():
    parser = argparse.ArgumentParser(description="Document Ingestion - Ingest documents into search index")
    parser.add_argument(
        "--create-indexer",
        action="store_true",
        default=False,
        help="Create a new indexer (default: False)"
    )
    
    args = parser.parse_args()
    
    print(f"Creating indexer: {args.create_indexer}")
    IngestionManager(create_indexer=args.create_indexer)

if __name__ == "__main__":
    main()