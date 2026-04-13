import fitz  # pymupdf
import os
import re
import json

DATA_PATH = "data"   # folder with english/ and hindi/
OUTPUT_FILE = "output/chunks.json"

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        try:
            text += page.get_text()
        except Exception as e:
            print(f"Skipping page due to error: {e}")

    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

all_chunks = []

for lang in ["english", "hindi"]:
    folder = os.path.join(DATA_PATH, lang)

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)

            print(f"Processing {file}...")
            text = extract_text(path)
            text = clean_text(text)
            chunks = chunk_text(text)

            for chunk in chunks:
                all_chunks.append({
                    "text": chunk,
                    "language": lang
                })

# Save
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"Saved {len(all_chunks)} chunks to {OUTPUT_FILE}")