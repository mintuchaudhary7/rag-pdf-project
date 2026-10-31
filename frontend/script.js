const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");

function addMessage(message, type) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");

  const isUser = type === "user";
  messageElement.classList.add(isUser ? "user-message" : "assistant-message");

  const labelElement = document.createElement("div");
  labelElement.classList.add("message-label");
  labelElement.textContent = isUser ? "You" : "AI";

  const contentElement = document.createElement("div");
  contentElement.classList.add("message-content");
  contentElement.textContent = message;

  messageElement.appendChild(labelElement);
  messageElement.appendChild(contentElement);

  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const question = questionInput.value.trim();

  if (!question) {
    return;
  }

  // Show user's question
  addMessage(question, "user");

  // Clear input
  questionInput.value = "";

  // Disable button while waiting
  sendButton.disabled = true;
  sendButton.textContent = "Thinking...";

//   const API_URL = "https://YOUR-RENDER-SERVICE.onrender.com";

  try {
    const response = await fetch("https://rag-pdf-rag-api.onrender.com/ask", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question: question,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to get response from server.");
    }

    const data = await response.json();

    // Display AI answer
    addMessage(data.answer, "assistant");
  } catch (error) {
    console.error(error);

    addMessage(
      "Sorry, something went wrong while getting the answer.",
      "assistant",
    );
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "Ask";
  }
}

sendButton.addEventListener("click", sendMessage);

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();

    sendMessage();
  }
});
