const form = document.getElementById("emailForm");
const linkInput = document.getElementById("linkInput");
const generateBtn = document.getElementById("generateBtn");
const chatMessages = document.getElementById("chatMessages");

// Store messages in memory
let messages = [];

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const link = linkInput.value.trim();
  if (!link) return;

  // Clear empty state if it exists
  if (messages.length === 0) {
    chatMessages.innerHTML = "";
  }

  // Add user message
  addMessage("user", `Generate email for: ${link}`);

  // Show loading state
  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";

  const loadingMessage = addMessage("bot", "", true);

  try {
    // Simulate API call to backend
    const response = await fetch("/link", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: link }),
    });

    if (!response.ok) {
      throw new Error("Failed to generate email");
    }

    const data = await response.json();

    // Remove loading message
    removeMessage(loadingMessage);

    // Add bot response
    const emailText =
      data.emails && data.emails.length > 0
        ? data.emails[0]
        : "Email generated successfully!";

    addMessage("bot", emailText);
  } catch (error) {
    // Remove loading message
    removeMessage(loadingMessage);

    // Add error message
    addMessage("bot", `Error: ${error.message}. Please try again.`);
  } finally {
    // Reset button state
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate Email";

    // Clear input
    linkInput.value = "";
  }
});

function addMessage(type, content, isLoading = false) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}-message`;

  if (isLoading) {
    messageDiv.innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        <span>Generating your email...</span>
                    </div>
                `;
  } else {
    // Improved formatting based on content type
    if (type === "bot" && content.includes("Error:")) {
      // Error messages - simple text
      messageDiv.innerHTML = `<div class="error-content">${content}</div>`;
    } else if (type === "bot") {
      // Email content - formatted properly
      messageDiv.innerHTML = `<div class="email-content">${formatEmailContent(
        content
      )}</div>`;
    } else {
      // User messages - simple text
      messageDiv.innerHTML = `<div class="user-content">${content}</div>`;
    }
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // Store message
  messages.push({ type, content, element: messageDiv });

  return messageDiv;
}

function formatEmailContent(content) {
  // Handle different content formats

  // If content is HTML, return as-is
  if (content.includes("<") && content.includes(">")) {
    return content;
  }

  // If content contains markdown-style formatting
  if (
    content.includes("**") ||
    content.includes("*") ||
    content.includes("#")
  ) {
    return formatMarkdown(content);
  }

  // If content has line breaks, preserve them
  if (content.includes("\n")) {
    return content
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map((line) => `<p>${line}</p>`)
      .join("");
  }

  // Default: wrap in paragraph
  return `<p>${content}</p>`;
}

function formatMarkdown(text) {
  return (
    text
      // Bold text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      // Italic text
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      // Headers
      .replace(/^### (.*$)/gm, "<h3>$1</h3>")
      .replace(/^## (.*$)/gm, "<h2>$1</h2>")
      .replace(/^# (.*$)/gm, "<h1>$1</h1>")
      // Line breaks
      .replace(/\n\n/g, "</p><p>")
      .replace(/\n/g, "<br>")
      // Wrap in paragraphs
      .replace(/^(.*)$/gm, "<p>$1</p>")
      // Clean up empty paragraphs
      .replace(/<p><\/p>/g, "")
      .replace(/<p><h/g, "<h")
      .replace(/<\/h([1-6])><\/p>/g, "</h$1>")
  );
}

function removeMessage(messageElement) {
  if (messageElement && messageElement.parentNode) {
    messageElement.parentNode.removeChild(messageElement);
    // Remove from messages array
    messages = messages.filter((msg) => msg.element !== messageElement);
  }
}

// Auto-focus on input when page loads
window.addEventListener("load", () => {
  linkInput.focus();
});
