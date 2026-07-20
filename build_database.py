import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

chroma_client = chromadb.PersistentClient(path="chroma_db")

collection = chroma_client.get_or_create_collection(
    name="qvi_knowledge"
)

folder = "scraped"

count = 0

for file in os.listdir(folder):

    if not file.endswith(".txt"):
        continue

    path = os.path.join(folder, file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into chunks
    chunks = [
        text[i:i+1000]
        for i in range(0, len(text), 1000)
    ]

    for chunk in chunks:

        if len(chunk.strip()) < 100:
            continue

        embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )

        collection.add(
            documents=[chunk],
            embeddings=[embedding.data[0].embedding],
            ids=[f"{file}_{count}"]
        )

        count += 1

print(f"\nAdded {count} chunks.")