from retrieval.retrieval_manager import RetrievalManager, SearchType
import prompty
import prompty.azure
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables from the src directory
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path,override=True)

class RAGChat:

    def __init__(self, retrieval_manager: RetrievalManager):
        self.retrieval_manager = retrieval_manager
        self.chat_history = []

    def chat(self, user_query: str) -> str:
        
        print(f"User Query: {user_query}")
        self.chat_history.append({"role": "user", "content": user_query})
        # Step 1: Retrieve relevant documents based on the user query
        retrieved_docs = self.retrieval_manager.search_documents(user_query, top_k=3, search_type=SearchType.HYBRID)

        # Step 2: Generate a response using the retrieved documents
        data_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "rag_chat.prompty")
        prompty_obj = prompty.load(data_path)
        #TO DO: Add chat history support
        prepared_template = prompty.prepare(prompty_obj, inputs= {"question":user_query, "context":retrieved_docs, "chat_history":self.chat_history})
        full_context = prepared_template[0]["content"]
        result = prompty.execute(data_path, inputs= {"question":user_query, "context":retrieved_docs, "chat_history":self.chat_history})
        self.chat_history.append({"role": "assistant", "content": result})
        return result