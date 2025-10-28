async function sendMessage() {
  let message = document.getElementById("message").value;
  if (!message) return;

  let chatBox = document.getElementById("chat-box");

  // Mostrar mensagem do usuário
  chatBox.innerHTML += `<p class="user"><b>Você:</b> ${message}</p>`;
  chatBox.scrollTop = chatBox.scrollHeight;

  // Enviar para o backend
  let response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message }),
  });

  let data = await response.json();

  // Mostrar resposta do bot
  chatBox.innerHTML += `<p class="bot"><b>Bot:</b> ${data.reply}</p>`;
  chatBox.scrollTop = chatBox.scrollHeight;

  // Limpar input
  document.getElementById("message").value = "";
}
// Enter
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("message");
  const sendBtn = document.getElementById("send-btn");

  if (input && sendBtn) {
    input.addEventListener("keydown", function (event) {
      // Envia ao pressionar Enter (sem Shift)
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendBtn.click();
      }
    });
  }
});

// Redirecionar para página de lista
document.addEventListener("DOMContentLoaded", () => {
  const listaBtn = document.getElementById("lista-btn");
  if (listaBtn) {
    listaBtn.addEventListener("click", () => {
      window.location.href = "lista";
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const chatBtn = document.getElementById("chat-btn");
  if (chatBtn) {
    chatBtn.addEventListener("click", () => {
      window.location.href = "/";
    });
  }
});
