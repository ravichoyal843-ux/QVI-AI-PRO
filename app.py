from openai import OpenAI
from dotenv import load_dotenv
import os

#Load the API key from .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("QVI AI Assistant")
print("Type 'exit'to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    response = client.responses.create(
        model="gpt-5",
        input=question
    )

    print("\nAI:", response.output_text)
    print()