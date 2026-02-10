# Recommended architecture for your full application

## Core modules

- **Action Capture SDK**: captures user behavior from web/desktop/mobile and sends normalized events.
- **Workflow Engine**: groups events into coherent business workflows and subflows.
- **AI Generation Service**: transforms workflows into strategy, scenarios, cases, and plans.
- **QA Knowledge Base**: stores domain templates, standards, and historical defects.
- **Review & Approval UI**: human-in-the-loop editing and approval of generated artifacts.

## Suggested event schema

- Timestamp
- Actor/Role
- App module/screen
- Action type (`click`, `input`, `navigate`, `api_call`, etc.)
- Input/output data (masked when sensitive)
- Expected outcome
- Actual outcome (optional during recording)

## AI pipeline idea

1. **Ingest** event stream
2. **Cluster** events into workflows
3. **Summarize** intent of each step
4. **Generate**:
   - Test strategy
   - Manual scenarios (BDD style)
   - Test cases (tabular)
   - Test plan
5. **Score coverage** and identify gaps
6. **Human review** and finalize exports

## Governance

- PII masking for captured data
- Prompt/version tracking for auditability
- Artifact versioning with approvals
- Role-based access control
