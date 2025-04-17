import streamlit as st
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import google.generativeai as genai

genai.configure(api_key="<your api key>")
model2 = genai.GenerativeModel('gemini-1.5-flash')

MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "website_chunks"
TOP_K = 5

# st.set_page_config(page_title="AI Chatbot", layout="centered")

#adding more pages..
st.set_page_config(page_title="PageUp Assistant", layout="centered", page_icon="🤖")

with st.sidebar:
    # st.image("https://www.facebook.com/pageupsoft/?locale=pt_BR", width=120)  # Replace with your logo URL
    st.markdown("### 🤖 **PageUp Assistant**")
    # st.caption("Your smart website assistant 💡")
    st.code("Your smart website assistant 💡")

    st.divider()

    st.markdown("#### 💬 Tips")
    st.info("Ask questions like:\n- `What services do you offer?`\n- `Where is the company located?`")

    st.divider()

    theme = st.radio("🌗 Theme", ["Light", "Dark"], horizontal=True)
    if theme == "Dark":
        st.write("🔧 Go to ⋮ > Settings > Theme > Dark")

    st.divider()

    if st.button("📞 Contact Us"):
        st.markdown("[📧 https://pageupsoft.com/](mailto:contact@pageupsoft.com)")

# st.sidebar.title("Welcome to AI Chatbot - Zudo🤖")
st.title("🤖 PageUp AI")

@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_resource
def load_vector_db():
    client = PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)

def embed_query(query, model):
    return model.encode([query])[0]

def retrieve_chunks(query, model, collection, top_k=TOP_K):
    query_embedding = embed_query(query, model)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results['documents'][0]

def generate_response(context_chunks, query):
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a smart, friendly assistant working at **PageUp** also known as **pageupsoftwareservicespvt**, a software development company. 
Your job is to help users by answering their questions about PageUp using the website content provided below.
remember that the content on the website is about pageupsoftwareservicespvt only, also known as Pageup
When asks about PageUp they actually mean about this company!! (Remeber this)

Please:
📌 Always respond in bullet points using the 📌 emoji.  
🧠 Be friendly and human-like. Greet the user if they greet you.  
🎯 Stay clear, precise, and split answers into small readable chunks.  
🤐 If the answer is not available, say: “📌 The answer to this query is currently not available.”  

Content from the PageUp website:
{context}

Question:
{query}

Answer:"""
    response = model2.generate_content(prompt)
    return response.text.strip()

model = load_model()
collection = load_vector_db()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("👋 Hi! I'm **PageUp's Assistant BOT**. Ask me anything about PageUp!")

with st.container():
    st.markdown("<div style='max-width: 700px; margin: auto;'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input("Ask me anything about the PageUp..")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        chunks = retrieve_chunks(user_input, model, collection)
        response = generate_response(chunks, user_input)

    bot_msg = f"🧠 **PageUp Assistant**\n\n{response}"
    st.session_state.messages.append({"role": "assistant", "content": bot_msg})
    with st.chat_message("assistant"):
        st.markdown(bot_msg)
