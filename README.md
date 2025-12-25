# 💬 Document Q&A System

An enterprise-grade Retrieval-Augmented Generation (RAG) application built with Azure AI Search, OpenAI, and Streamlit. This system enables users to query enterprise documents and receive intelligent, context-aware responses.

## 🎯 Overview

This project implements a complete RAG pipeline that ingests documents, creates searchable embeddings, and generates accurate answers to user questions based on retrieved context. The system leverages Azure's cognitive services and OpenAI's language models to provide a seamless question-answering experience.

## 🔧 Technical Components

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Search Engine** | Azure AI Search | Document indexing and retrieval |
| **Vector Database** | Azure AI Search (Vector Store) | Semantic search capabilities |
| **LLM Provider** | OpenAI API | Response generation |
| **Embedding Model** | Azure OpenAI Embeddings | Text vectorization |
| **Web Framework** | Streamlit | User interface |
| **Prompt Management** | Prompty | Prompt templating and orchestration |
| **Cloud Storage** | Azure Blob Storage | Document storage |

### Project Structure

```
documentQnA/
├── src/
│   ├── app.py                      # Streamlit web application entry point
│   ├── ingestion/                  # Document ingestion pipeline
│   │   ├── ingest.py              # CLI for document ingestion
│   │   ├── ingestion_manager.py   # Handles document processing
│   │   └── search_service_manager.py # Azure Search configuration
│   ├── retrieval/                  # Document retrieval system
│   │   ├── retrieval_manager.py   # Multi-strategy search (text/vector/hybrid)
│   │   └── search_test.py         # Retrieval testing utilities
│   ├── generation/                 # Response generation
│   │   ├── rag_chat.py            # RAG orchestration logic
│   │   ├── rag_chat.prompty       # Prompt template
│   │   └── rag_test.py            # Generation testing utilities
│   └── utility/                    # Shared utilities
│       ├── embedder.py            # Text embedding service
│       └── embedder_test.py       # Embedding testing utilities
├── infrastructure/
│   └── bicep/                     # Azure infrastructure as code
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## 🚀 Features

- **Multi-Strategy Search**: Support for text, vector, and hybrid search modes
- **Real-Time Chat Interface**: Interactive Streamlit-based UI
- **Document Ingestion Pipeline**: Automated indexing and embedding creation
- **Context-Aware Responses**: RAG-powered answer generation
- **Session Management**: Chat history tracking and conversation context
- **Modular Architecture**: Separated concerns for ingestion, retrieval, and generation

## 📋 Prerequisites

- Python 3.8+
- Azure subscription with:
  - Azure AI Search service
  - Azure OpenAI service
  - Azure Blob Storage account
- OpenAI API access

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd documentQnA
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the `src` directory with the following:
   ```env
   AZURE_SEARCH_SERVICE_ENDPOINT=<your-search-endpoint>
   AZURE_SEARCH_INDEX=<your-index-name>
   AZURE_SEARCH_DATASOURCE=<your-datasource>
   AZURE_SEARCH_SKILLSET=<your-skillset>
   AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
   AZURE_OPENAI_API_KEY=<your-api-key>
   AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
   ```

## 📖 Usage

### Document Ingestion

Ingest documents into the search index:

```bash
cd src/ingestion
python ingest.py --create-indexer  # Creates indexer and ingests documents
python ingest.py                   # Ingests documents using existing indexer
```

Use `--create-indexer` flag when setting up the indexer for the first time. Omit the flag to ingest documents with an existing indexer.
```

### Run the Application

Launch the Streamlit web interface:

```bash
cd src
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Testing Components

Test individual components:

```bash
# Test retrieval
python src/retrieval/search_test.py

# Test embeddings
python src/utility/embedder_test.py

# Test RAG generation
python src/generation/rag_test.py
```

## 🔍 Search Types

The system supports three search strategies:

1. **Text Search**: Traditional keyword-based search
2. **Vector Search**: Semantic similarity using embeddings
3. **Hybrid Search**: Combined text and vector search for optimal results

**Built with ❤️ for Enterprise Document Intelligence**
