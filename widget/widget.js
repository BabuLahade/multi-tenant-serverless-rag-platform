(function () {

  // ── Config injected by the script tag ──────────────────────
  const script = document.currentScript;
  const CLIENT_ID  = script.getAttribute("data-client-id");
  const API_KEY    = script.getAttribute("data-api-key");
  const BOT_NAME   = script.getAttribute("data-bot-name")   || "Nova AI";
  const BRAND      = script.getAttribute("data-brand-color") || "#2563eb";
  const API_URL    = script.getAttribute("data-api-url")     ||
    "https://dh90wd8pxc.execute-api.ap-south-1.amazonaws.com/dev/chat";

  // ── Inject CSS ─────────────────────────────────────────────
  const style = document.createElement("style");
  style.textContent = `
    #nova-bubble {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: ${BRAND};
      color: white;
      font-size: 26px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(0,0,0,0.25);
      z-index: 9999;
      user-select: none;
    }
    #nova-window {
      position: fixed;
      bottom: 92px;
      right: 24px;
      width: 360px;
      height: 520px;
      background: white;
      border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.18);
      display: flex;
      flex-direction: column;
      z-index: 9998;
      overflow: hidden;
      display: none;
    }
    #nova-header {
      padding: 16px 18px;
      background: ${BRAND};
      color: white;
      font-weight: bold;
      font-size: 15px;
      font-family: Arial, sans-serif;
    }
    #nova-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-family: Arial, sans-serif;
    }
    .nova-msg {
      max-width: 80%;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 14px;
      line-height: 1.5;
      word-wrap: break-word;
    }
    .nova-user {
      background: ${BRAND};
      color: white;
      align-self: flex-end;
      border-bottom-right-radius: 4px;
    }
    .nova-bot {
      background: #f1f1f1;
      color: #222;
      align-self: flex-start;
      border-bottom-left-radius: 4px;
    }
    .nova-typing {
      background: #f1f1f1;
      color: #888;
      align-self: flex-start;
      font-style: italic;
      font-size: 13px;
      padding: 10px 14px;
      border-radius: 12px;
    }
    #nova-input-area {
      display: flex;
      padding: 12px;
      gap: 8px;
      border-top: 1px solid #eee;
    }
    #nova-input {
      flex: 1;
      padding: 9px 12px;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 14px;
      outline: none;
      font-family: Arial, sans-serif;
    }
    #nova-send {
      padding: 9px 16px;
      background: ${BRAND};
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      font-weight: bold;
    }
    #nova-send:disabled {
      opacity: 0.5;
      cursor: default;
    }
  `;
  document.head.appendChild(style);

  // ── Build DOM ──────────────────────────────────────────────
  const bubble = document.createElement("div");
  bubble.id = "nova-bubble";
  bubble.innerHTML = "💬";

  const win = document.createElement("div");
  win.id = "nova-window";
  win.innerHTML = `
    <div id="nova-header">${BOT_NAME}</div>
    <div id="nova-messages"></div>
    <div id="nova-input-area">
      <input id="nova-input" type="text" placeholder="Ask a question..." autocomplete="off" />
      <button id="nova-send">Send</button>
    </div>
  `;

  document.body.appendChild(bubble);
  document.body.appendChild(win);

  // ── Toggle open/close ──────────────────────────────────────
  let isOpen = false;

  bubble.addEventListener("click", function () {
    isOpen = !isOpen;
    win.style.display = isOpen ? "flex" : "none";
    bubble.innerHTML = isOpen ? "✕" : "💬";
    if (isOpen) {
      document.getElementById("nova-input").focus();
      if (document.getElementById("nova-messages").children.length === 0) {
        addMsg(`Hi! I'm ${BOT_NAME}. How can I help you today?`, "bot");
      }
    }
  });

  // ── Add message to chat ────────────────────────────────────
  function addMsg(text, type) {
    const msgs = document.getElementById("nova-messages");
    const div = document.createElement("div");
    div.className = "nova-msg nova-" + type;
    div.innerText = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }

  // ── Send message ───────────────────────────────────────────
  async function send() {
    const input  = document.getElementById("nova-input");
    const btn    = document.getElementById("nova-send");
    const msgs   = document.getElementById("nova-messages");
    const question = input.value.trim();

    if (!question) return;

    addMsg(question, "user");
    input.value = "";
    btn.disabled = true;

    // Typing indicator
    const typing = document.createElement("div");
    typing.className = "nova-typing";
    typing.innerText = "Typing...";
    msgs.appendChild(typing);
    msgs.scrollTop = msgs.scrollHeight;

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": API_KEY
        },
        body: JSON.stringify({
          client_id: CLIENT_ID,
          message: question
        })
      });

      const data = await res.json();
      typing.remove();

      if (!res.ok) {
        addMsg(data.error || "Something went wrong.", "bot");
        return;
      }

      addMsg(data.answer || "No answer received.", "bot");

    } catch (err) {
      typing.remove();
      addMsg("Unable to reach the server. Please try again.", "bot");
      console.error(err);
    } finally {
      btn.disabled = false;
      input.focus();
    }
  }

  document.getElementById("nova-send")
    .addEventListener("click", send);

  document.getElementById("nova-input")
    .addEventListener("keypress", function (e) {
      if (e.key === "Enter") send();
    });

})();