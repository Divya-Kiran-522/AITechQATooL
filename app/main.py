from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.core import ActionEvent as CoreActionEvent
from app.core import ActionType, GeneratedArtifacts, SessionData, generate_from_workflow
from app.ui import get_ui_page


class ActionEvent(BaseModel):
    action_type: ActionType
    screen: str = Field(..., description="UI screen or component name")
    description: str = Field(..., description="Human-readable description of the action")
    actor: str = Field(default="user", description="Who performed the action")
    expected_result: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class SessionCreateRequest(BaseModel):
    app_name: str
    workflow_name: str
    objective: str


class SessionResponse(BaseModel):
    session_id: str
    app_name: str
    workflow_name: str
    objective: str
    started_at: datetime


class GeneratedArtifactsResponse(BaseModel):
    test_strategy: str
    manual_test_scenarios: str
    test_cases: str
    test_plan: str


app = FastAPI(
    title="AI QA Workflow Assistant",
    description=(
        "Capture user actions and workflow events, then generate manual test scenarios, "
        "test cases, test strategy, and a test plan."
    ),
)

SESSIONS: Dict[str, SessionData] = {}


@app.get("/")
def home():
    return get_ui_page()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/sessions", response_model=SessionResponse)
def create_session(payload: SessionCreateRequest) -> SessionResponse:
    session_id = str(uuid4())
    data = SessionData(
        app_name=payload.app_name,
        workflow_name=payload.workflow_name,
        objective=payload.objective,
    )
    SESSIONS[session_id] = data
    return SessionResponse(
        session_id=session_id,
        app_name=data.app_name,
        workflow_name=data.workflow_name,
        objective=data.objective,
        started_at=data.started_at,
    )


@app.post("/sessions/{session_id}/events")
def record_event(session_id: str, event: ActionEvent) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.events.append(
        CoreActionEvent(
            action_type=event.action_type,
            screen=event.screen,
            description=event.description,
            actor=event.actor,
            expected_result=event.expected_result,
            metadata=event.metadata,
        )
    )
    return {"status": "recorded", "events_count": len(session.events)}


@app.get("/sessions/{session_id}")
def get_session(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session_id,
        "app_name": session.app_name,
        "workflow_name": session.workflow_name,
        "objective": session.objective,
        "started_at": session.started_at,
        "events": [event.__dict__ for event in session.events],
    }


@app.post("/sessions/{session_id}/generate", response_model=GeneratedArtifactsResponse)
def generate_artifacts(session_id: str) -> GeneratedArtifacts:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.events:
        raise HTTPException(status_code=400, detail="No actions captured yet")

    return generate_from_workflow(session)
