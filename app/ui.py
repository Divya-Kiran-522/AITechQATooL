from fastapi.responses import HTMLResponse


UI_HTML = """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>AI QA Workflow Assistant</title>
  <style>
    :root { color-scheme: light dark; }
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background: #f5f7fb;
      color: #1f2937;
    }
    .container {
      max-width: 1024px;
      margin: 0 auto;
      padding: 1rem;
    }
    h1 { margin-bottom: 0.25rem; }
    .subtitle { color: #4b5563; margin-top: 0; }
    .grid {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }
    .card {
      background: white;
      border-radius: 10px;
      padding: 1rem;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    label { display: block; font-weight: 600; margin: 0.5rem 0 0.25rem; }
    input, select, textarea, button {
      width: 100%;
      box-sizing: border-box;
      padding: 0.55rem;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      font-size: 0.95rem;
    }
    textarea { min-height: 84px; resize: vertical; }
    button {
      border: 0;
      background: #2563eb;
      color: white;
      font-weight: 700;
      cursor: pointer;
      margin-top: 0.8rem;
    }
    button:hover { background: #1d4ed8; }
    .status {
      margin-top: 1rem;
      padding: 0.75rem;
      background: #ecfeff;
      border-left: 4px solid #0ea5e9;
      border-radius: 6px;
      font-size: 0.9rem;
      white-space: pre-wrap;
    }
    .artifacts pre {
      background: #111827;
      color: #f3f4f6;
      border-radius: 8px;
      padding: 0.75rem;
      max-height: 220px;
      overflow: auto;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class=\"container\">
    <h1>AI QA Workflow Assistant</h1>
    <p class=\"subtitle\">Create a session, record workflow events, and generate QA artifacts in one place.</p>

    <div class=\"grid\">
      <section class=\"card\">
        <h2>1) Create Session</h2>
        <label for=\"appName\">Application Name</label>
        <input id=\"appName\" placeholder=\"E-Commerce Portal\" />
        <label for=\"workflowName\">Workflow Name</label>
        <input id=\"workflowName\" placeholder=\"Guest Checkout\" />
        <label for=\"objective\">Objective</label>
        <textarea id=\"objective\" placeholder=\"Validate guest user purchase flow\"></textarea>
        <button id=\"createSessionBtn\">Create Session</button>
      </section>

      <section class=\"card\">
        <h2>2) Record Event</h2>
        <label for=\"sessionId\">Session ID</label>
        <input id=\"sessionId\" placeholder=\"Session ID auto-fills after creation\" />
        <label for=\"actionType\">Action Type</label>
        <select id=\"actionType\">
          <option value=\"click\">click</option>
          <option value=\"input\">input</option>
          <option value=\"navigate\">navigate</option>
          <option value=\"assert\">assert</option>
          <option value=\"api_call\">api_call</option>
          <option value=\"custom\">custom</option>
        </select>
        <label for=\"screen\">Screen</label>
        <input id=\"screen\" placeholder=\"Checkout\" />
        <label for=\"description\">Description</label>
        <input id=\"description\" placeholder=\"Click Place Order\" />
        <label for=\"expectedResult\">Expected Result</label>
        <input id=\"expectedResult\" placeholder=\"Order confirmation is displayed\" />
        <button id=\"addEventBtn\">Add Event</button>
      </section>
    </div>

    <section class=\"card\" style=\"margin-top:1rem\">
      <h2>3) Generate Artifacts</h2>
      <button id=\"generateBtn\">Generate for Current Session</button>
      <div id=\"status\" class=\"status\">Ready.</div>
    </section>

    <section class=\"card artifacts\" style=\"margin-top:1rem\">
      <h2>Generated Output</h2>
      <h3>Test Strategy</h3>
      <pre id=\"testStrategy\"></pre>
      <h3>Manual Test Scenarios</h3>
      <pre id=\"manualScenarios\"></pre>
      <h3>Test Cases</h3>
      <pre id=\"testCases\"></pre>
      <h3>Test Plan</h3>
      <pre id=\"testPlan\"></pre>
    </section>
  </div>

  <script>
    const statusEl = document.getElementById('status');
    const sessionIdEl = document.getElementById('sessionId');

    function setStatus(msg) { statusEl.textContent = msg; }

    async function jsonRequest(url, method, body) {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: body ? JSON.stringify(body) : undefined,
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || JSON.stringify(data) || `HTTP ${response.status}`);
      }
      return data;
    }

    document.getElementById('createSessionBtn').addEventListener('click', async () => {
      try {
        const payload = {
          app_name: document.getElementById('appName').value,
          workflow_name: document.getElementById('workflowName').value,
          objective: document.getElementById('objective').value,
        };
        const data = await jsonRequest('/sessions', 'POST', payload);
        sessionIdEl.value = data.session_id;
        setStatus(`Session created: ${data.session_id}`);
      } catch (error) {
        setStatus(`Create session failed: ${error.message}`);
      }
    });

    document.getElementById('addEventBtn').addEventListener('click', async () => {
      try {
        const sessionId = sessionIdEl.value.trim();
        if (!sessionId) throw new Error('Session ID is required');

        const payload = {
          action_type: document.getElementById('actionType').value,
          screen: document.getElementById('screen').value,
          description: document.getElementById('description').value,
          actor: 'user',
          expected_result: document.getElementById('expectedResult').value,
          metadata: {},
        };
        const data = await jsonRequest(`/sessions/${sessionId}/events`, 'POST', payload);
        setStatus(`Event recorded. Total events: ${data.events_count}`);
      } catch (error) {
        setStatus(`Record event failed: ${error.message}`);
      }
    });

    document.getElementById('generateBtn').addEventListener('click', async () => {
      try {
        const sessionId = sessionIdEl.value.trim();
        if (!sessionId) throw new Error('Session ID is required');
        const data = await jsonRequest(`/sessions/${sessionId}/generate`, 'POST');
        document.getElementById('testStrategy').textContent = data.test_strategy || '';
        document.getElementById('manualScenarios').textContent = data.manual_test_scenarios || '';
        document.getElementById('testCases').textContent = data.test_cases || '';
        document.getElementById('testPlan').textContent = data.test_plan || '';
        setStatus('Artifacts generated successfully.');
      } catch (error) {
        setStatus(`Generation failed: ${error.message}`);
      }
    });
  </script>
</body>
</html>
"""


def get_ui_page() -> HTMLResponse:
    return HTMLResponse(content=UI_HTML)
