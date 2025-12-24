
import streamlit as st
from typing import List, Dict
from generation.rag_chat import RAGChat
from retrieval.retrieval_manager import RetrievalManager

st.set_page_config(page_title="RAG Chat", page_icon="💬", layout="centered")
st.title("💬 Enterprise QnA")

st.caption("A minimal UI for a RAG-powered chatbot for enterprise users.")

# ---- Restart button ----
if st.button("🔄 Start New Session", type="secondary"):
    st.session_state.clear()
    st.rerun()

# ---- Initialize chat history ----
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---- Display chat history ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat input ----
user_input = st.chat_input("Ask something about your enterprise policy...")


    
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message in chat message container
    st.chat_message("user").markdown(user_input)

    # Get response from RAG Chat
    rag_chat = RAGChat(retrieval_manager=RetrievalManager())
    response = rag_chat.chat(user_input)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display bot response in chat message container
    st.chat_message("assistant").markdown(response)

    