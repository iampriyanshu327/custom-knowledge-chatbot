
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

genai.configure(api_key="<Your api key>")

model2 = genai.GenerativeModel('gemini-1.5-flash')

# client = OpenAI(api_key="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")

# Config
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "website_chunks"
TOP_K = 5

# Optional: GPT-powered RAG
# USE_GPT = True  # Set to True if using OpenAI

def embed_query(query, model):
    return model.encode([query])[0]

def retrieve_relevant_chunks(query, model):
    query_embedding = embed_query(query, model)

    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(query_embeddings=[query_embedding], n_results=TOP_K)

    docs = results['documents'][0]
    return docs

# def generate_response(context_chunks, query):
#     if USE_GPT:
#         # Concatenate context
#         context = "\n\n".join(context_chunks)
#         client = OpenAI()
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that answers queries based on website content."},
#                 {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
#             ],
#             temperature=0.2,
#             max_tokens=400
#         )
#         return response.choices[0].message.content.strip()
#     else:
#         # Simple rule-based response using top chunks
#         return f"Top relevant content based on your query:\n\n" + "\n\n".join(context_chunks)

def generate_response(context_chunks, query):
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a smart, friendly assistant that helps users by answering clearly and precisely in bullet points using 📌 emoji. 
Based on the following website content, answer the user’s question. If the answer isn't available, say so directly.

Context:
{context}

Question:
{query}

Answer:"""

    response = model2.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    query = input("Enter your query: ")

    print("Loading model and retrieving relevant chunks...")
    model = SentenceTransformer(MODEL_NAME)
    top_chunks = retrieve_relevant_chunks(query, model)

    print("\nGenerating response...\n")
    response = generate_response(top_chunks, query)
    print(response)
