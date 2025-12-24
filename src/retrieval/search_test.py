import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from retrieval.retrieval_manager import RetrievalManager, SearchType


def main():
    print("Searching for documents related to 'Reimbursement Program':")
    searchResults = RetrievalManager().search_documents("Reimbursement Program", top_k=5, search_type=SearchType.HYBRID)
    print("Search Completed. Results:")
    # Print out the search results. Results are formatted in azure core ItemPaged
    if len(searchResults) > 0:
        for result in searchResults:
            print(f"{result}\n")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()