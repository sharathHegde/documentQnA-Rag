from ingestion.search_service_manager import SearchServiceManager


class IngestionManager:
    # Implementation of ingestion manager
    def __init__(self, create_indexer: bool = True):
        # initiate the search service manager
        self.create_indexer = create_indexer
        self.search_service_manager = SearchServiceManager()
        if self.create_indexer:
            print("Setting up the ingestion pipeline with indexer.")
            self.search_service_manager.setup_ingestion()
        else:
            print("Indexer creation skipped as per the argument.")
            print("Run the indexer")
            self.search_service_manager.run_indexer()
