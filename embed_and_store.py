
from sentence_transformers import SentenceTransformer
# import chromadb
from chromadb import PersistentClient

def load_chunks(file_path="text_chunks.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()
    
    chunks = []
    for block in raw.strip().split("[CHUNK ")[1:]:
        try:
            text = block.split("]", 1)[1].strip()
            chunks.append(text)
        except IndexError:
            continue
    return chunks

def embed_and_store(chunks, collection_name="website_chunks"):
    
    model = SentenceTransformer('all-MiniLM-L6-v2')

    
    # client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db")) [this was depreciated]

    client = PersistentClient(path="./chroma_db") # new addition!
    collection = client.get_or_create_collection(name=collection_name)

    embeddings = model.encode(chunks, show_progress_bar=True)

    documents = []
    ids = []
    metadatas = []
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        ids.append(f"chunk_{i+1}")
        metadatas.append({"source": "pageupsoft", "chunk_id": i+1})

    collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
    # client.persist() #Supposedly depreciated in the newer version and happens automatically

    print(f"✅ {len(documents)} chunks embedded and stored in ChromaDB.")

if __name__ == "__main__":
    chunks = load_chunks()
    embed_and_store(chunks)
