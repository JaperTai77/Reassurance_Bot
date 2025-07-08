document.addEventListener('DOMContentLoaded', () => {
  const BACKEND_ORIGIN = window.BACKEND_ORIGIN;
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
      appendThinkingMessage();
      chatInput.value = '';
      sendButton.disabled = true;
      fetch(`${BACKEND_ORIGIN}/chat/gettopresponse?text=${encodeURIComponent(messageText)}`, {
        method: 'GET',
        headers: {
          'accept': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        removeThinkingMessage();
        const revised = data?.messages?.["Revised Response"];
        if (revised) {
          appendMessage(revised, 'bot');
        } else {
          appendMessage("Bot response unavailable.", 'bot');
        }
      })
      .catch(() => {
        removeThinkingMessage();
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

  function appendThinkingMessage() {
    // Only add if not already present
    if (!chatMessages.querySelector('.message.thinking')) {
      const thinkingElement = document.createElement('div');
      thinkingElement.classList.add('message', 'bot', 'thinking');
      thinkingElement.textContent = '...';
      chatMessages.appendChild(thinkingElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }

  function removeThinkingMessage() {
    const thinkingElement = chatMessages.querySelector('.message.thinking');
    if (thinkingElement) {
      chatMessages.removeChild(thinkingElement);
    }
  }

  // Quotes functionality
  const quotesSearchInput = document.getElementById('quotes-search-input');
  const quotesSearchButton = document.getElementById('quotes-search-button');
  const quotesGetAllButton = document.getElementById('quotes-getall-button');
  const quotesMessages = document.getElementById('quotes-messages');

  quotesSearchButton.addEventListener('click', searchQuotes);
  quotesGetAllButton.addEventListener('click', getAllQuotes);
  quotesSearchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      searchQuotes();
    }
  });

  function searchQuotes() {
    const searchText = quotesSearchInput.value.trim();
    if (searchText !== '') {
      quotesSearchButton.disabled = true;
      fetch(`${BACKEND_ORIGIN}/vs/getsearchtexts?text=${encodeURIComponent(searchText)}&k=6`, {
        method: 'GET',
        headers: {
          'accept': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data?.messages && Array.isArray(data.messages)) {
          clearQuotesMessages();
          data.messages.forEach(message => {
            appendQuoteMessage(message);
          });
        } else {
          clearQuotesMessages();
          appendQuoteMessage("沒有找到相關語錄。");
        }
      })
      .catch(() => {
        clearQuotesMessages();
        appendQuoteMessage("錯誤：無法連接到語錄搜尋 API。");
      })
      .finally(() => {
        quotesSearchButton.disabled = false;
      });
    }
  }

  function getAllQuotes() {
    quotesGetAllButton.disabled = true;
    fetch(`${BACKEND_ORIGIN}/vs/getalltexts`, {
      method: 'GET',
      headers: {
        'accept': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data?.messages && Array.isArray(data.messages)) {
        clearQuotesMessages();
        data.messages.forEach(message => {
          appendQuoteMessage(message);
        });
      } else {
        clearQuotesMessages();
        appendQuoteMessage("無法取得語錄。");
      }
    })
    .catch(() => {
      clearQuotesMessages();
      appendQuoteMessage("錯誤：無法連接到語錄 API。");
    })
    .finally(() => {
      quotesGetAllButton.disabled = false;
    });
  }

  function appendQuoteMessage(text) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('quotes-message');
    messageElement.textContent = text;
    quotesMessages.appendChild(messageElement);
    quotesMessages.scrollTop = quotesMessages.scrollHeight; // Scroll to bottom
  }

  function clearQuotesMessages() {
    quotesMessages.innerHTML = '';
  }
});
