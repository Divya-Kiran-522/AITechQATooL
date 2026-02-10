from fastapi.responses import HTMLResponse


UI_HTML = """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>AI QA Workflow Assistant</title>
  <style>
    :root { color-scheme: light; }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, Arial, sans-serif;
      color: #0f172a;
      background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
      min-height: 100vh;
    }
    .container {
      max-width: 1120px;
      margin: 0 auto;
      padding: 1rem;
    }
    .header {
      background: #0f172a;
      color: #e2e8f0;
      border-radius: 14px;
      padding: 1rem 1.25rem;
      margin-bottom: 1rem;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.2);
    }
    .header h1 { margin: 0; font-size: 1.4rem; }
    .header p { margin: 0.4rem 0 0; color: #bfdbfe; }

    .grid {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }
    .card {
      background: #ffffff;
      border-radius: 12px;
      padding: 1rem;
      border: 1px solid #dbeafe;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.07);
    }
    .card h2 {
      margin-top: 0;
      font-size: 1.1rem;
      color: #1d4ed8;
    }
    label { display: block; font-weight: 700; margin: 0.5rem 0 0.2rem; font-size: 0.92rem; }
    input, select, textarea, button {
      width: 100%;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      padding: 0.6rem;
      font-size: 0.95rem;
      background: #fff;
    }
    textarea { min-height: 88px; resize: vertical; }
    .button-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.6rem;
      margin-top: 0.8rem;
    }
    button {
      background: #2563eb;
      border: none;
      color: #fff;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.2s ease;
    }
    button:hover { background: #1d4ed8; }
    button.secondary { background: #0f766e; }
    button.secondary:hover { background: #0f5f59; }
    button.ghost {
      background: #e2e8f0;
      color: #0f172a;
    }
    button.ghost:hover { background: #cbd5e1; }

    .status {
      margin-top: 1rem;
      padding: 0.8rem;
      border-radius: 8px;
      border-left: 4px solid #0284c7;
      background: #ecfeff;
      font-size: 0.92rem;
      white-space: pre-wrap;
    }
    .events-list {
      margin: 0;
      padding-left: 1.2rem;
      max-height: 210px;
      overflow: auto;
    }
    .events-list li { margin-bottom: 0.5rem; }
    .artifacts pre {
      margin: 0.3rem 0 0.8rem;
      background: #0f172a;
      color: #e2e8f0;
      border-radius: 8px;
      padding: 0.75rem;
      max-height: 190px;
      overflow: auto;
      white-space: pre-wrap;
      font-size: 0.88rem;
    }
    @media (max-width: 700px) {
      .button-row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class=\"container\">
    <header class=\"header\">
      <h1>AI QA Workflow Assistant</h1>
      <p>Website to perform workflow actions, review captured steps, and generate QA artifacts in one place.</p>
    </header>

    <div class=\"grid\">
      <section class=\"card\">
        <h2>1) Create Session</h2>
        <label for=\"appName\">Application Name</label>
        <input id=\"appName\" placeholder=\"E-Commerce Portal\" />
        <label for=\"workflowName\">Workflow Name</label>
        <input id=\"workflowName\" placeholder=\"Guest Checkout\" />
        <label for=\"objective\">Objective</label>
        <textarea id=\"objective\" placeholder=\"Validate guest user purchase flow\"></textarea>
        <div class=\"button-row\">
          <button id=\"createSessionBtn\">Create Session</button>
          <button id=\"loadSessionBtn\" class=\"secondary\">Load Session</button>
        </div>
      </section>

      <section class=\"card\">
        <h2>2) Perform Action</h2>
        <label for=\"sessionId\">Session ID</label>
        <input id=\"sessionId\" placeholder=\"Auto-filled after session creation\" />
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
        <div class=\"button-row\">
          <button id=\"addEventBtn\">Add Action</button>
          <button id=\"clearEventBtn\" class=\"ghost\">Clear Action Form</button>
        </div>
      </section>

      <section class=\"card\">
        <h2>3) Session Actions</h2>
        <div class=\"button-row\">
          <button id=\"generateBtn\">Generate Artifacts</button>
          <button id=\"refreshBtn\" class=\"secondary\">Refresh Session Details</button>
        </div>
        <div id=\"status\" class=\"status\">Ready.</div>
        <h3>Captured Actions</h3>
        <ol id=\"eventsList\" class=\"events-list\"></ol>
      </section>
    </div>

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
    const eventsListEl = document.getElementById('eventsList');

    function setStatus(msg) { statusEl.textContent = msg; }

    function renderEvents(events) {
      eventsListEl.innerHTML = '';
      if (!events || events.length === 0) {
        const item = document.createElement('li');
        item.textContent = 'No actions captured yet.';
        eventsListEl.appendChild(item);
        return;
      }
      events.forEach((event, index) => {
        const item = document.createElement('li');
        item.textContent = `${index + 1}. [${event.action_type}] ${event.screen} - ${event.description}`;
        eventsListEl.appendChild(item);
      });
    }

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

    async function loadSession() {
      const sessionId = sessionIdEl.value.trim();
      if (!sessionId) throw new Error('Session ID is required');
      const data = await jsonRequest(`/sessions/${sessionId}`, 'GET');
      renderEvents(data.events || []);
      setStatus(`Loaded session ${sessionId}. Total actions: ${(data.events || []).length}`);
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
        renderEvents([]);
        setStatus(`Session created: ${data.session_id}`);
      } catch (error) {
        setStatus(`Create session failed: ${error.message}`);
      }
    });

    document.getElementById('loadSessionBtn').addEventListener('click', async () => {
      try {
        await loadSession();
      } catch (error) {
        setStatus(`Load session failed: ${error.message}`);
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
        await loadSession();
        setStatus(`Action recorded. Total actions: ${data.events_count}`);
      } catch (error) {
        setStatus(`Record action failed: ${error.message}`);
      }
    });

    document.getElementById('clearEventBtn').addEventListener('click', () => {
      document.getElementById('screen').value = '';
      document.getElementById('description').value = '';
      document.getElementById('expectedResult').value = '';
      setStatus('Action form cleared.');
    });

    document.getElementById('refreshBtn').addEventListener('click', async () => {
      try {
        await loadSession();
      } catch (error) {
        setStatus(`Refresh failed: ${error.message}`);
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

    renderEvents([]);
  </script>
</body>
</html>
"""


def get_ui_page() -> HTMLResponse:
    return HTMLResponse(content=UI_HTML)
