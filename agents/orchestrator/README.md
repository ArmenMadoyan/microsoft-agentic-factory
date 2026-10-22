# Orchestrator (Copilot Studio)

- Name: Engineering Software Factory Orchestrator
- Description: Autonomous engineering orchestrator that receives work from Microsoft Teams, manages Jira tickets, coordinates planning, development, validation and deployment agents, and drives each issue to closure.
- Instructions: `instructions.md` (paste into the agent's Instructions field)
- Tenant: a Microsoft 365 developer environment

## Build order (hybrid: UI + code)
Flow 1: Teams -> Jira -> Planning agent -> Teams reply
Flow 2: + GitHub agent -> PR creation
Flow 3: + Development, Validation, Deployment -> Jira closure -> Teams notification

## Code half (this repo)
- External worker (Docker, Copilot CLI) exposed as MCP/flow; Copilot Studio only orchestrates.
- State keyed by Jira ID; schema in `agents/memory/TICKET.template.json`.
- Source control for the agent: `pac solution export` + `unpack` into `solution/`.
