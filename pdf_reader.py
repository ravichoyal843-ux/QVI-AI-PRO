from pypdf import PdfReader

reader = PdfReader("data/OBJECTION HANDLING..pdf")

text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"

print(text)