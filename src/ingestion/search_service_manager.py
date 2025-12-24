from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    SearchIndex,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SplitSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    AzureOpenAIEmbeddingSkill,
    EntityRecognitionSkill,
    SearchIndexerIndexProjection,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode,
    SearchIndexerSkillset,
    CognitiveServicesAccountKey,
    SearchIndexer
)
import os
import sys
from pathlib import Path

class SearchServiceManager:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Retrieve configuration from environment variables
        self.search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
        self.search_index = os.environ["AZURE_SEARCH_INDEX"]
        self.search_datasource = os.environ["AZURE_SEARCH_DATASOURCE"]
        self.search_skillset = os.environ["AZURE_SEARCH_SKILLSET"]
        self.search_indexer = os.environ["AZURE_SEARCH_INDEXER"]
        self.azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT_FOR_EMBEDDING"]
        self.search_credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"])
        self.azure_openai_key = os.environ["AZURE_OPENAI_KEY_FOR_EMBEDDING"]
        self.blob_connection_string = os.environ["AZURE_BLOB_CONNECTION_STRING"]
        self.blob_container_name = os.environ["AZURE_BLOB_CONTAINER"]
    # Create a search index with vector search capabilities
    def create_search_index(self):
        index_client = SearchIndexClient(endpoint=self.search_endpoint, credential=self.search_credential)  
        fields = [
            SearchField(name="parent_id", type=SearchFieldDataType.String),  
            SearchField(name="title", type=SearchFieldDataType.String),
            SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
            SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
            SearchField(name="text_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=1024, vector_search_profile_name="myHnswProfile")
            ]

        # Configure the vector search configuration  
        vector_search = VectorSearch(  
            algorithms=[  
                HnswAlgorithmConfiguration(name="myHnsw"),
            ],  
            profiles=[  
                VectorSearchProfile(  
                    name="myHnswProfile",  
                    algorithm_configuration_name="myHnsw",  
                    vectorizer_name="myOpenAI",  
                )
            ],  
            vectorizers=[  
                AzureOpenAIVectorizer(  
                    vectorizer_name="myOpenAI",  
                    kind="azureOpenAI",  
                    parameters=AzureOpenAIVectorizerParameters(  
                        resource_url=self.azure_openai_endpoint,  
                        api_key=self.azure_openai_key,
                        deployment_name="text-embedding-3-large",
                        model_name="text-embedding-3-large"
                    ),
                ),  
            ], 
        )  

        # Create the search index
        print(f"creating the search index - {self.search_index}") 
        index = SearchIndex(name=self.search_index, fields=fields, vector_search=vector_search)  
        result = index_client.create_or_update_index(index)  
        print(f"{result.name} created")  

    # Create a data source connection to Azure Blob Storage
    def create_data_source_connection(self):
        indexer_client = SearchIndexerClient(endpoint=self.search_endpoint, credential=self.search_credential)
        container = SearchIndexerDataContainer(name=self.blob_container_name)
        print(f"creating the data source connection - {self.search_datasource}") 
        data_source_connection = SearchIndexerDataSourceConnection(
            name=self.search_datasource,
            type="azureblob",
            connection_string=self.blob_connection_string,
            container=container
        )
        data_source = indexer_client.create_or_update_data_source_connection(data_source_connection)

        print(f"Data source '{data_source.name}' created or updated")

    # Create a skillset for data enrichment
    def create_skillset(self):
        # Create a skillset  
        split_skill = SplitSkill(  
            description="Split skill to chunk documents",  
            text_split_mode="pages",  
            context="/document",  
            maximum_page_length=2000,  
            page_overlap_length=500,  
            inputs=[  
                InputFieldMappingEntry(name="text", source="/document/content"),  
            ],  
            outputs=[  
                OutputFieldMappingEntry(name="textItems", target_name="pages")  
            ],  
        )  
        
        embedding_skill = AzureOpenAIEmbeddingSkill(  
            description="Skill to generate embeddings via Azure OpenAI",  
            context="/document/pages/*",  
            resource_url=self.azure_openai_endpoint,  
            api_key= self.azure_openai_key,  
            deployment_name="text-embedding-3-large",  
            model_name="text-embedding-3-large",
            dimensions=1024,
            inputs=[  
                InputFieldMappingEntry(name="text", source="/document/pages/*"),  
            ],  
            outputs=[  
                OutputFieldMappingEntry(name="embedding", target_name="text_vector")  
            ],  
        )
        
        index_projections = SearchIndexerIndexProjection(  
            selectors=[  
                SearchIndexerIndexProjectionSelector(  
                    target_index_name=self.search_index,  
                    parent_key_field_name="parent_id",  
                    source_context="/document/pages/*",  
                    mappings=[  
                        InputFieldMappingEntry(name="chunk", source="/document/pages/*"),  
                        InputFieldMappingEntry(name="text_vector", source="/document/pages/*/text_vector"),
                        InputFieldMappingEntry(name="title", source="/document/metadata_storage_name"),  
                    ],  
                ),  
            ],  
            parameters=SearchIndexerIndexProjectionsParameters(  
                projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS  
            ),  
        ) 

        skills = [split_skill, embedding_skill]
        print(f"creating the search skillset - {self.search_skillset}") 
        skillset = SearchIndexerSkillset(  
            name=self.search_skillset,  
            description="Skillset to chunk documents and generating embeddings",  
            skills=skills,  
            index_projection=index_projections
        )
        
        client = SearchIndexerClient(endpoint=self.search_endpoint, credential=self.search_credential)  
        client.create_or_update_skillset(skillset)  
        print(f"{skillset.name} created")

    # Create an indexer to orchestrate data ingestion
    def create_indexer(self):
        # Create an indexer  

        indexer_parameters = None

        print(f"creating the search indexer - {self.search_indexer}")
        
        indexer = SearchIndexer(  
            name=self.search_indexer,  
            description="Indexer to index documents and generate embeddings",  
            skillset_name=self.search_skillset,  
            target_index_name=self.search_index,  
            data_source_name=self.search_datasource,
            parameters=indexer_parameters
        )  

        # Create and run the indexer  
        indexer_client = SearchIndexerClient(endpoint=self.search_endpoint, credential=self.search_credential)  
        indexer_result = indexer_client.create_or_update_indexer(indexer)  

        print(f' {self.search_indexer} is created and running. Give the indexer a few minutes before running a query.')

    def setup_ingestion(self):
        self.create_search_index()
        self.create_data_source_connection()
        self.create_skillset()
        self.create_indexer()
    
    def run_indexer(self):
        indexer_client = SearchIndexerClient(endpoint=self.search_endpoint, credential=self.search_credential)  
        indexer_client.run_indexer(self.search_indexer)
        print(f' {self.search_indexer} is running. Give the indexer a few minutes before running a query.')


        