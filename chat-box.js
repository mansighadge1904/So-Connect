document.getElementById('send-button').addEventListener('click', function() {
    const messageInput = document.getElementById('message-input');
    const messageText = messageInput.value.trim();
  
    if (messageText !== '') {
      // Create new message element
      const newMessage = document.createElement('div');
      newMessage.classList.add('message', 'user');
      newMessage.textContent = messageText;
  
      // Append the message to the chat box
      const chatBox = document.getElementById('chat-box');
      chatBox.appendChild(newMessage);
  
      // Scroll to the bottom of the chat box
      chatBox.scrollTop = chatBox.scrollHeight;
  
      // Clear the input field
      messageInput.value = '';
    }
  });
  
  // Optional: Press "Enter" to send message
  document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      document.getElementById('send-button').click();
    }
  });
  