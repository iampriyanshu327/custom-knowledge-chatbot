import re
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

CHUNK_SIZE = 500  
def clean_text(text):
    
    text = re.sub(r'http\S+', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = text.lower()
    return text.strip()

def split_into_chunks(text, chunk_size=CHUNK_SIZE):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def preprocess_and_chunk(file_path="raw_text_data.txt", output_path="text_chunks.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = f.read()

    raw_pages = raw_data.split("=" * 80)
    all_chunks = []

    for page in raw_pages:
        if not page.strip():
            continue

        # cleaned = clean_text(page)
        parts = page.strip().split("\n\n")
        main = clean_text(parts[0])
        extras = "\n\n".join(parts[1:])
        combined = main + "\n\n" + extras

        chunks = split_into_chunks(combined)
        all_chunks.extend(chunks)

    with open(output_path, "w", encoding="utf-8") as out:
        for i, chunk in enumerate(all_chunks):
            out.write(f"[CHUNK {i+1}]\n{chunk}\n\n")

    print(f"✅ Preprocessing complete. {len(all_chunks)} chunks saved to '{output_path}'.")

if __name__ == "__main__":
    preprocess_and_chunk()
