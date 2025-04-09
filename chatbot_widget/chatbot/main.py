from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retrieval_and_response import SentenceTransformer, retrieve_relevant_chunks, generate_response

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and vector DB once
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

from chromadb import PersistentClient
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "website_chunks"
client = PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    query = chat.message
    chunks = retrieve_relevant_chunks(query, model)
    response = generate_response(chunks, query)
    return {"response": response}
