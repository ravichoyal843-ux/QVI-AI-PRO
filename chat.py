import streamlit as st
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

import os

chroma_client = chromadb.PersistentClient(path="chroma_db")

try:
    collection = chroma_client.get_collection("qvi_knowledge")
except Exception:
    import build_database
    collection = chroma_client.get_collection("qvi_knowledge")

st.set_page_config(
    page_title="QVI AI PRO",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 QVI AI PRO")
st.caption("Powered by GPT-5 + Your QVI Knowledge Base")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask anything about QVI...")

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    results = collection.query(
        query_embeddings=[embedding.data[0].embedding],
        n_results=5
    )

    context = "\n\n".join(results["documents"][0])

    prompt = f"""
You are an expert QVI assistant.

Answer ONLY using the information below.

If the answer isn't available, say:
'I couldn't find that information in the QVI knowledge base.'

Information:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    answer = response.output_text

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )