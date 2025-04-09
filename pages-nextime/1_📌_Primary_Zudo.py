
import streamlit as st
from sentence_transformers import SentenceTransformer
# import chromadb
# from chromadb.config import Settings (depreciated)

from chromadb import PersistentClient
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDj2ssBbwiPQ7oHIoAXfFc1o-3u9ErCYD4")  # or directly insert it as api_key="your-key"

model2 = genai.GenerativeModel('gemini-1.5-flash') 

# configurations!
MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "website_chunks"
TOP_K = 5
USE_GPT = True  

st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("🤖 Zudo AI")

@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_resource
def load_vector_db():
    # return chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR)).get_collection(COLLECTION_NAME)
    # return PersistentClient(path="./chroma_db")

    client = PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(name="website_chunks")


#main functions
def embed_query(query, model):
    return model.encode([query])[0]

def retrieve_chunks(query, model, collection, top_k=TOP_K):
    query_embedding = embed_query(query, model)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results['documents'][0]

def generate_response(context_chunks, query):
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a smart, friendly assistant that helps users by answering clearly and precisely in bullet points using 📌 emoji. 
Based on the following website content, answer the user’s question. If the answer isn't available, say something similar to "The Answer to this query is currently not available".

Context:
{context}

Question:
{query}

Answer:"""

    response = model2.generate_content(prompt)
    return response.text.strip()


# --- STREAMLIT UI ---
model = load_model()
collection = load_vector_db()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask me anything about the website:", key="query_input")

if user_input:
    with st.spinner("Thinking..."):
        chunks = retrieve_chunks(user_input, model, collection)
        answer = generate_response(chunks, user_input)
        st.session_state.chat_history.append((user_input, answer))

# Display chat history
for q, a in reversed(st.session_state.chat_history):
    # st.markdown(f"**You:** {q}")
    st.markdown(f"**🧑‍💼:** {a}")
    st.markdown("---")
