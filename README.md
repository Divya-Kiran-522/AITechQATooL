# AI QA Workflow Assistant (MVP)

This repository now contains a starter backend for an AI-driven QA assistant that can:

1. Capture user/app workflow actions.
2. Store action sequences by session.
3. Generate in one place:
   - Manual test scenarios
   - Test cases
   - Test strategy
   - Test plan

## Why this helps your goal

You asked for one app that records actions and workflow, then produces QA artifacts. This MVP gives you exactly that pipeline as API endpoints, so you can connect:

- Browser extension / desktop recorder / RPA log source -> event capture endpoint
- LLM provider (OpenAI/Azure/etc.) -> replace the deterministic generator with AI prompts
- Web UI -> display generated deliverables in a single dashboard

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open App UI: `http://127.0.0.1:8000/`

Open Swagger UI: `http://127.0.0.1:8000/docs`

## API flow

1. `POST /sessions` create a workflow capture session
2. `POST /sessions/{session_id}/events` record each action
3. `POST /sessions/{session_id}/generate` generate all QA artifacts
4. `GET /sessions/{session_id}` inspect captured workflow

## Example payloads

### Create session

```json
{
  "app_name": "E-Commerce Portal",
  "workflow_name": "Guest Checkout",
  "objective": "Validate guest user purchase flow"
}
```

### Record event

```json
{
  "action_type": "click",
  "screen": "Checkout",
  "description": "Click Place Order",
  "actor": "user",
  "expected_result": "Order confirmation page is displayed",
  "metadata": {
    "priority": "high"
  }
}
```

## Suggested next steps

- Add persistent storage (PostgreSQL).
- Add authentication and team workspaces.
- Add prompt templates and LLM integration with guardrails.
- Add export formats: Markdown, CSV, XLSX, PDF.
- Add traceability matrix from workflow step -> scenario -> test case.

## Packaging & Local Install

To work with this repository locally using the project's editable install:

PowerShell (Windows):

```powershell
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
. .\.venv\Scripts\Activate.ps1
pip install -e .
```

Bash (WSL/Git Bash/macOS):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

After install you can run the test-suite with `pytest`.
