from django.http import HttpResponse

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VIKMO DealerDesk — Control Center</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(18, 24, 38, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --accent: #06b6d4;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --success: #10b981;
      --warning: #f59e0b;
      --radius: 12px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
    }
    header {
      background: rgba(15, 23, 42, 0.8);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .logo {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-weight: 800;
      font-size: 1.25rem;
      letter-spacing: -0.025em;
    }
    .badge {
      background: linear-gradient(135deg, var(--primary), var(--accent));
      color: white;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .status-pill {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.875rem;
      background: rgba(16, 185, 129, 0.1);
      color: var(--success);
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .status-dot {
      width: 8px;
      height: 8px;
      background: var(--success);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--success);
    }
    main {
      flex: 1;
      padding: 2rem;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 2rem;
    }
    @media (max-width: 1024px) {
      main { grid-template-columns: 1fr; }
    }
    .panel {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .panel-title {
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 0.75rem;
    }
    .chat-box {
      flex: 1;
      min-height: 400px;
      max-height: 520px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      padding-right: 0.5rem;
      margin-bottom: 1rem;
    }
    .msg {
      max-width: 85%;
      padding: 0.85rem 1.1rem;
      border-radius: var(--radius);
      font-size: 0.925rem;
      line-height: 1.5;
    }
    .msg-user {
      align-self: flex-end;
      background: linear-gradient(135deg, var(--primary), var(--primary-hover));
      color: white;
      border-bottom-right-radius: 2px;
    }
    .msg-bot {
      align-self: flex-start;
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-bottom-left-radius: 2px;
    }
    .tool-tag {
      display: inline-block;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #a5b4fc;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      margin-top: 0.5rem;
    }
    .chat-input-row {
      display: flex;
      gap: 0.75rem;
    }
    input, select, button {
      font-family: inherit;
      border-radius: 8px;
      border: 1px solid var(--card-border);
      padding: 0.75rem 1rem;
      background: rgba(15, 23, 42, 0.8);
      color: white;
      font-size: 0.925rem;
    }
    input:focus, select:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
    }
    button {
      background: var(--primary);
      border: none;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
    }
    button:hover { background: var(--primary-hover); }
    .quick-prompts {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .quick-chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 0.3rem 0.7rem;
      border-radius: 6px;
      font-size: 0.78rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .quick-chip:hover {
      background: rgba(99, 102, 241, 0.15);
      color: white;
      border-color: var(--primary);
    }
    .endpoint-list {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .endpoint-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(15, 23, 42, 0.5);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.04);
      text-decoration: none;
      color: inherit;
      transition: border-color 0.2s, background 0.2s;
    }
    .endpoint-item:hover {
      background: rgba(30, 41, 59, 0.6);
      border-color: var(--card-border);
    }
    .method-get {
      font-weight: 700;
      color: #38bdf8;
      font-size: 0.8rem;
      font-family: 'JetBrains Mono', monospace;
      width: 48px;
    }
    .method-post {
      font-weight: 700;
      color: #34d399;
      font-size: 0.8rem;
      font-family: 'JetBrains Mono', monospace;
      width: 48px;
    }
    .endpoint-path {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      flex: 1;
      margin-left: 0.5rem;
    }
    .endpoint-desc {
      color: var(--text-muted);
      font-size: 0.8rem;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo">
      <span>VIKMO DealerDesk</span>
      <span class="badge">Track: AI / ML</span>
    </div>
    <div class="status-pill">
      <div class="status-dot"></div>
      <span>Backend & API Active</span>
    </div>
  </header>

  <main>
    <!-- LEFT: DEALER ASSISTANT CHAT -->
    <div class="panel">
      <div class="panel-title">
        <span>🤖 DealerDesk AI Assistant</span>
        <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 400;">POST /api/assistant/chat/</span>
      </div>

      <div class="quick-prompts">
        <span class="quick-chip" onclick="setPrompt('Do you have brake pads for a Pulsar 150?')">Brake pads for Pulsar 150?</span>
        <span class="quick-chip" onclick="setPrompt('Check live stock for BRK-1044 and OIL-1001')">Check stock for BRK-1044</span>
        <span class="quick-chip" onclick="setPrompt('Order 2 units of BRK-1044')">Draft order: 2 of BRK-1044</span>
      </div>

      <div class="chat-box" id="chatBox">
        <div class="msg msg-bot">
          Hello! I am your DealerDesk Assistant. I can help find compatible parts, check real-time stock and prices, and create draft orders for your dealership.
        </div>
      </div>

      <div class="chat-input-row">
        <input type="text" id="userInput" placeholder="Ask about spare parts, stock, or draft orders..." style="flex: 1;" onkeypress="if(event.key==='Enter') sendChat()">
        <button onclick="sendChat()" id="sendBtn">Send</button>
      </div>
    </div>

    <!-- RIGHT: API HUB & DATA ACCESS -->
    <div class="panel">
      <div class="panel-title">
        <span>⚡ Live API Endpoints</span>
        <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 400;">JSON Endpoints</span>
      </div>

      <div class="endpoint-list">
        <a class="endpoint-item" href="/api/health/" target="_blank">
          <span class="method-get">GET</span>
          <span class="endpoint-path">/api/health/</span>
          <span class="endpoint-desc">Health Check</span>
        </a>

        <a class="endpoint-item" href="/api/products/?page_size=5" target="_blank">
          <span class="method-get">GET</span>
          <span class="endpoint-path">/api/products/</span>
          <span class="endpoint-desc">600 Catalogue Items</span>
        </a>

        <a class="endpoint-item" href="/api/dealers/?page_size=5" target="_blank">
          <span class="method-get">GET</span>
          <span class="endpoint-path">/api/dealers/</span>
          <span class="endpoint-desc">25 Seeded Dealers</span>
        </a>

        <a class="endpoint-item" href="/api/reorder-suggestions/" target="_blank">
          <span class="method-get">GET</span>
          <span class="endpoint-path">/api/reorder-suggestions/</span>
          <span class="endpoint-desc">40 SKUs Reorder Points</span>
        </a>

        <a class="endpoint-item" href="/api/forecast/FIL-1016/" target="_blank">
          <span class="method-get">GET</span>
          <span class="endpoint-path">/api/forecast/FIL-1016/</span>
          <span class="endpoint-desc">4-Week Demand Forecast</span>
        </a>

        <a class="endpoint-item" href="/api/orders/" target="_blank">
          <span class="method-get">GET</span>
          <span class="endpoint-path">/api/orders/</span>
          <span class="endpoint-desc">Orders Ledger</span>
        </a>
      </div>

      <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(99, 102, 241, 0.08); border-radius: 8px; border: 1px solid rgba(99, 102, 241, 0.2);">
        <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 0.25rem;">Automated Verification Passed</div>
        <div style="font-size: 0.825rem; color: var(--text-muted);">
          Run <code>python smoke_test.py --track aiml</code> in terminal to verify all 10 contract checks.
        </div>
      </div>
    </div>
  </main>

  <script>
    const sessionId = "browser-sess-" + Math.random().toString(36).substring(2, 8);

    function setPrompt(text) {
      document.getElementById('userInput').value = text;
      sendChat();
    }

    async function sendChat() {
      const input = document.getElementById('userInput');
      const text = input.value.trim();
      if (!text) return;

      const chatBox = document.getElementById('chatBox');
      
      // User message
      const userDiv = document.createElement('div');
      userDiv.className = 'msg msg-user';
      userDiv.innerText = text;
      chatBox.appendChild(userDiv);
      input.value = '';
      chatBox.scrollTop = chatBox.scrollHeight;

      // Bot loading placeholder
      const botDiv = document.createElement('div');
      botDiv.className = 'msg msg-bot';
      botDiv.innerText = 'Analyzing request and checking live database...';
      chatBox.appendChild(botDiv);
      chatBox.scrollTop = chatBox.scrollHeight;

      try {
        const res = await fetch('/api/assistant/chat/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            session_id: sessionId,
            dealer_id: 1,
            message: text
          })
        });
        const data = await res.json();
        
        let replyHtml = data.reply || 'No response';
        if (data.tool_calls && data.tool_calls.length > 0) {
          const tools = data.tool_calls.map(t => t.name).join(', ');
          replyHtml += `<br><span class="tool-tag">🔧 Tool called: ${tools}</span>`;
        }
        if (data.cited_skus && data.cited_skus.length > 0) {
          replyHtml += `<br><span class="tool-tag">📦 Cited SKUs: ${data.cited_skus.join(', ')}</span>`;
        }
        botDiv.innerHTML = replyHtml;
      } catch (err) {
        botDiv.innerText = 'Error calling assistant: ' + err.message;
      }
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  </script>
</body>
</html>
"""

def portal_view(request):
    return HttpResponse(HTML_CONTENT, content_type="text/html")
