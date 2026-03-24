const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatBody = document.getElementById('chatBody');
const typingIndicator = document.getElementById('typingIndicator');

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom() {
    chatBody.scrollTo({
        top: chatBody.scrollHeight,
        behavior: 'smooth'
    });
}

// Format message using Marked and DOMPurify
function formatMessage(text) {
    if (window.marked && window.DOMPurify) {
        return DOMPurify.sanitize(marked.parse(text));
    }
    return text;
}

function addMessage(text, sender) {
    const isBot = sender === 'bot';
    
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isBot ? 'bot-message' : 'user-message');
    
    messageDiv.innerHTML = `
        <div class="message-content markdown-body">
            ${isBot ? formatMessage(text) : text}
        </div>
        <div class="timestamp">${getCurrentTime()}</div>
    `;
    
    chatBody.appendChild(messageDiv);
    scrollToBottom();
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const messageText = userInput.value.trim();
    if (!messageText) return;

    // Add user message
    addMessage(messageText, 'user');
    userInput.value = '';

    // Show typing indicator
    typingIndicator.classList.add('active');
    scrollToBottom();

    try {
        // Fetch response from Flask ML endpoint
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        const botResponse = data.response;
        
        // Hide typing indicator before showing msg
        typingIndicator.classList.remove('active');
        
        // Simulate a slight typing delay based on response length for realism
        setTimeout(() => {
             addMessage(botResponse, 'bot');
        }, 300);
       
    } catch (err) {
        console.error("Chat API error:", err);
        typingIndicator.classList.remove('active');
        addMessage("Oops! My backend ML server seems to be currently unavailable.", 'bot');
    }
});
