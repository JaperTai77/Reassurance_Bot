document.addEventListener('DOMContentLoaded', () => {
  const chatbotTab = document.getElementById('chatbot-tab');
  const quotesTab = document.getElementById('quotes-tab');
  const chatbotContent = document.getElementById('chatbot-content');
  const quotesContent = document.getElementById('quotes-content');

  function activateTab(tab) {
    if (tab === 'chatbot') {
      chatbotTab.classList.add('active');
      quotesTab.classList.remove('active');
      chatbotContent.style.display = 'block';
      quotesContent.style.display = 'none';
    } else if (tab === 'quotes') {
      quotesTab.classList.add('active');
      chatbotTab.classList.remove('active');
      quotesContent.style.display = 'block';
      chatbotContent.style.display = 'none';
    }
  }

  chatbotTab.addEventListener('click', () => activateTab('chatbot'));
  quotesTab.addEventListener('click', () => activateTab('quotes'));

  const chatInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-button');
  const chatMessages = document.getElementById('chat-messages');

  sendButton.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });

  function sendMessage() {
    const messageText = chatInput.value.trim();
    if (messageText !== '') {
      appendMessage(messageText, 'user');
      chatInput.value = '';
      sendButton.disabled = true;
      fetch(`http://localhost:8000/chat/gettopresponse?text=${encodeURIComponent(messageText)}`, {
        method: 'GET',
        headers: {
          'accept': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        const revised = data?.messages?.["Revised Response"];
        if (revised) {
          appendMessage(revised, 'bot');
        } else {
          appendMessage("Bot response unavailable.", 'bot');
        }
      })
      .catch(() => {
        appendMessage("Error: Unable to reach chatbot API.", 'bot');
      })
      .finally(() => {
        sendButton.disabled = false;
      });
    }
  }

  function appendMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = text;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
  }
});
