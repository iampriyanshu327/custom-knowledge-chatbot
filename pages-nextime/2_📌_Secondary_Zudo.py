import streamlit as st
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import google.generativeai as genai

#api setup
genai.configure(api_key="AIzaSyDj2ssBbwiPQ7oHIoAXfFc1o-3u9ErCYD4")
model2 = genai.GenerativeModel('gemini-1.5-flash')

#some compulsions
MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "website_chunks"
TOP_K = 5

st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("🤖 Zudo AI")

#resources for  the project
@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_resource
def load_vector_db():
    client = PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)

# main functions!
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

#model load-out
model = load_model()
collection = load_vector_db()

if "messages" not in st.session_state:
    st.session_state.messages = []

# chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input for the chat
user_input = st.chat_input("Ask me anything about the website...")

if user_input:
    # User message (Input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Processing (Process)
    with st.spinner("Thinking..."):
        chunks = retrieve_chunks(user_input, model, collection)
        response = generate_response(chunks, user_input)

    # Bot response (Output)
    st.session_state.messages.append({"role": "AI", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
