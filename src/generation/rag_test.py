import os
import sys
import argparse
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))
from generation.rag_chat import RAGChat
from retrieval.retrieval_manager import RetrievalManager


def main():
    print("RAG Chat initiated.")
    parser = argparse.ArgumentParser(description="RAG Chat Test - Query documents using RAG")
    parser.add_argument(
        "query",
        type=str,
        nargs="?",
        help="The query to ask the RAG system"
    )
    
    args = parser.parse_args()
    
    # If no command-line argument, prompt for input
    if args.query:
        query = args.query
    else:
        query = input("Enter your query: ")
    
    print(f"\nQuery: {query}\n")
    response = RAGChat(retrieval_manager=RetrievalManager()).chat(query)
    print(f"Response:\n{response}")

if __name__ == "__main__":
    main()