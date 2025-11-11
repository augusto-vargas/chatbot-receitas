// Handles sending messages to the backend and updating the chat UI.
async function sendMessage() {
  const inputEl = document.getElementById("message");
  const chatBox = document.getElementById("chat-box");
  const message = inputEl && inputEl.value.trim();
  if (!message) return;

  chatBox.insertAdjacentHTML('beforeend', `<p class="user"><b>Você:</b> ${message}</p>`);
  chatBox.scrollTop = chatBox.scrollHeight;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  chatBox.insertAdjacentHTML('beforeend', `<p class="bot"><b>Bot:</b> ${data.reply}</p>`);
  chatBox.scrollTop = chatBox.scrollHeight;
  inputEl.value = "";
}

// Display welcome message with username and tips.
function showWelcomeMessage() {
  const chatBox = document.getElementById("chat-box");
  const username = chatBox && chatBox.getAttribute("data-username");
  
  if (!chatBox || !username) return;

  const welcome = `
    <p class="bot"><b>Bot:</b> Olá, ${username}! 👋 Bem-vindo ao ChefBot.</p>
    <p class="bot"><b>Bot:</b> Aqui você pode buscar receitas digitando:</p>
    <p class="bot">• Um ingrediente (ex: "frango", "tomate")</p>
    <p class="bot">• O nome de uma receita (ex: "sushi", "pizza")</p>
    <p class="bot">Explore a biblioteca completa em "Lista de Ingredientes" ou crie suas próprias receitas em "Minhas Receitas". Bom apetite! 🍳</p>
  `;
  
  chatBox.insertAdjacentHTML('beforeend', welcome);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Single DOM-ready entry point: wire UI controls.
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("message");
  const sendBtn = document.getElementById("send-btn");
  const listaBtn = document.getElementById("lista-btn");
  const chatBtn = document.getElementById("chat-btn");

  showWelcomeMessage();

  if (input && sendBtn) {
    // Enter submits (without Shift)
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" && !ev.shiftKey) {
        ev.preventDefault();
        sendBtn.click();
      }
    });
    sendBtn.addEventListener("click", sendMessage);
  }

  if (listaBtn) listaBtn.addEventListener("click", () => window.location.href = "lista");
  if (chatBtn) chatBtn.addEventListener("click", () => window.location.href = "/");
});

