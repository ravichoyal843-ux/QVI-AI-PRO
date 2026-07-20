import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

chroma_client = chromadb.PersistentClient(path="chroma_db")

collection = chroma_client.get_collection("qvi_knowledge")

print("QVI AI Assistant")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

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
You are a QVI expert.

Answer ONLY using the information below.

If the answer is not available, say:
"I couldn't find that information in the QVI knowledge base."

Information:

{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    print("\nAI:")
    print(response.output_text)
    print()