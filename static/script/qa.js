let sessionId = null;
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function startNewChat() {
            fetch('/new_session')
                .then(response => response.json())
                .then(data => {
                    sessionId = data.session_id;
                    document.getElementById('chat-box').innerHTML = '';
                });
        }

        function sendMessage() {
            const userInput = document.getElementById('user-input');
            const message = userInput.value;
            if (message.trim() === '') return;

            addMessageToChat('user', message);
            userInput.value = '';

            fetch(`/chat/${sessionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                addMessageToChat('bot', data.response);
            });
        }

        function addMessageToChat(sender, message) {
            const chatBox = document.getElementById('chat-box');
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', sender);
            const messageText = document.createElement('div');
            messageText.classList.add('message-text');
            messageText.textContent = message;
            messageElement.appendChild(messageText);
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function uploadPDF() {
            const form = document.getElementById('upload-form');
            const formData = new FormData(form);

            fetch('{{ url_for("qa") }}', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                alert('PDF uploaded successfully!');
            })
            .catch(error => {
                console.error('Error uploading PDF:', error);
                alert('Failed to upload PDF.');
            });
        }