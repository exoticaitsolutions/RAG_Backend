(function() {
    document.head.insertAdjacentHTML('beforeend', 
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.16/tailwind.min.css" rel="stylesheet" />'
    );

    // Chatbot container
    var chatbotContainer = document.createElement("div");
    chatbotContainer.id = "chatbot-container";
    chatbotContainer.style.position = "fixed";
    chatbotContainer.style.bottom = "20px";
    chatbotContainer.style.right = "20px";
    chatbotContainer.style.width = "300px";
    chatbotContainer.style.height = "400px";
    chatbotContainer.style.background = "#fff";
    chatbotContainer.style.border = "1px solid #ccc";
    chatbotContainer.style.borderRadius = "10px";
    chatbotContainer.style.overflow = "hidden";
    chatbotContainer.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
    chatbotContainer.innerHTML = `
        <div id="chat-header" style="background: #007bff; color: white; padding: 10px; text-align: center;">
            Chatbot
        </div>
        <div id="chat-messages" style="height: 300px; overflow-y: auto; padding: 10px;">
            <p>Welcome! Ask me anything.</p>
        </div>
        <input type="text" id="chat-input" placeholder="Type your message..." 
            style="width: 80%; padding: 10px; border: none; border-top: 1px solid #ccc;">
        <button id="chat-submit" style="width: 20%; padding: 10px; border: none; background: #007bff; color: white; cursor: pointer;">Send</button>
    `;

    document.body.appendChild(chatbotContainer);

    // Function to send a message to the API
    function sendMessageToAPI(message) {
        fetch("http://127.0.0.1:8000/pdf/api/v1/query/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: message })
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.response, "bot");
        })
        .catch(error => {
            console.error("Error:", error);
            displayMessage("Error fetching response.", "bot");
        });
    }

    // Function to display messages
    function displayMessage(message, sender) {
        var chatMessages = document.getElementById("chat-messages");
        var msgDiv = document.createElement("div");
        msgDiv.textContent = message;
        msgDiv.style.padding = "10px";
        msgDiv.style.margin = "5px";
        msgDiv.style.borderRadius = "5px";

        if (sender === "bot") {
            msgDiv.style.background = "#f1f1f1";
            msgDiv.style.textAlign = "left";
        } else {
            msgDiv.style.background = "#007bff";
            msgDiv.style.color = "white";
            msgDiv.style.textAlign = "right";
        }

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event listener for the send button
    document.getElementById("chat-submit").addEventListener("click", function() {
        var chatInput = document.getElementById("chat-input");
        var userMessage = chatInput.value.trim();
        if (userMessage) {
            displayMessage(userMessage, "user");
            sendMessageToAPI(userMessage);
            chatInput.value = "";
        }
    });

    // Enter key listener
    document.getElementById("chat-input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            document.getElementById("chat-submit").click();
        }
    });

})();
