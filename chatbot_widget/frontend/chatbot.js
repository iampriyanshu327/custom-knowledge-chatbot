const chatToggle = document.getElementById("chat-toggle");
const chatWidget = document.getElementById("chat-widget");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");
const sendBtn = document.getElementById("send-btn");

const API_URL = "http://127.0.0.1:8000/chat"; 

chatToggle.onclick = () => {
  chatWidget.style.display = chatWidget.style.display === "flex" ? "none" : "flex";
};

function appendMessage(sender, text) {
  const msg = document.createElement("p");
  msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage("🧑‍💼", message);
  chatInput.value = "";
  appendMessage("🤖", "Thinking...");

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: message })
    });
    const data = await res.json();
    chatMessages.lastChild.innerHTML = `<strong>🤖:</strong> ${data.answer}`;
  } catch (err) {
    chatMessages.lastChild.innerHTML = "<strong>🤖:</strong> Oops! Something went wrong.";
  }
}

sendBtn.onclick = sendMessage;

chatInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});