from app.core import ActionEvent, ActionType, SessionData, generate_from_workflow


def test_generate_from_workflow_creates_all_artifacts():
    session = SessionData(
        app_name="Demo App",
        workflow_name="Checkout",
        objective="Verify checkout flow",
    )
    session.events.extend(
        [
            ActionEvent(
                action_type=ActionType.NAVIGATE,
                screen="Cart",
                description="Open cart",
                expected_result="Cart page is displayed",
            ),
            ActionEvent(
                action_type=ActionType.CLICK,
                screen="Checkout",
                description="Click place order",
                expected_result="Order confirmation appears",
            ),
        ]
    )

    artifacts = generate_from_workflow(session)

    assert "Test Strategy for Demo App / Checkout" in artifacts.test_strategy
    assert "Scenario 1" in artifacts.manual_test_scenarios
    assert "TC-001" in artifacts.test_cases
    assert "Test Plan: Checkout" in artifacts.test_plan
