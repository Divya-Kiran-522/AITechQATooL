from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


class ActionType(str, Enum):
    CLICK = "click"
    INPUT = "input"
    NAVIGATE = "navigate"
    ASSERT = "assert"
    API_CALL = "api_call"
    CUSTOM = "custom"


@dataclass
class ActionEvent:
    action_type: ActionType
    screen: str
    description: str
    actor: str = "user"
    expected_result: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class SessionData:
    app_name: str
    workflow_name: str
    objective: str
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    events: List[ActionEvent] = field(default_factory=list)


@dataclass
class GeneratedArtifacts:
    test_strategy: str
    manual_test_scenarios: str
    test_cases: str
    test_plan: str


def generate_from_workflow(session: SessionData) -> GeneratedArtifacts:
    steps = [f"{idx + 1}. [{event.action_type}] {event.description} on {event.screen}" for idx, event in enumerate(session.events)]

    scenario_lines = [
        f"Scenario {idx + 1}: Validate {event.description.lower()} ({event.screen})\n"
        f"  Given user is on {event.screen}\n"
        f"  When user performs '{event.description}'\n"
        f"  Then {event.expected_result or 'the expected behavior is observed'}"
        for idx, event in enumerate(session.events)
    ]

    test_case_rows = [
        f"TC-{idx + 1:03d} | {event.screen} | {event.description} | "
        f"{event.expected_result or 'Verify expected system response'}"
        for idx, event in enumerate(session.events)
    ]

    test_strategy = (
        f"Test Strategy for {session.app_name} / {session.workflow_name}\n"
        f"Objective: {session.objective}\n\n"
        "Scope:\n- Functional workflow validation\n- Negative path exploration\n"
        "- Usability and data integrity checks\n\n"
        "Approach:\n- Capture real user actions\n"
        "- Convert workflow steps into scenario-based coverage\n"
        "- Maintain traceability from action to test case\n"
        "- Prioritize high-risk screens and transitions\n\n"
        "Captured Workflow Steps:\n" + "\n".join(steps)
    )

    manual_test_scenarios = "\n\n".join(scenario_lines)

    test_cases = (
        "Test Case ID | Module/Screen | Steps | Expected Result\n"
        "---|---|---|---\n" + "\n".join(test_case_rows)
    )

    test_plan = (
        f"Test Plan: {session.workflow_name}\n"
        f"Application: {session.app_name}\n"
        f"Goal: {session.objective}\n\n"
        "Entry Criteria:\n- Workflow events captured\n- Environment is available\n\n"
        "Exit Criteria:\n- All critical test cases executed\n"
        "- No Sev-1/Sev-2 defects open\n\n"
        "Deliverables:\n- Manual scenarios\n- Detailed test cases\n"
        "- Execution report and defect summary"
    )

    return GeneratedArtifacts(
        test_strategy=test_strategy,
        manual_test_scenarios=manual_test_scenarios,
        test_cases=test_cases,
        test_plan=test_plan,
    )
