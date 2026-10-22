# Orchestrator (Copilot Studio)

The live definition is source-controlled as YAML in
`copilot-studio/engineering-software-factory-orchestrator/` (orchestrator in `agent.mcs.yml`,
child agents in `agents/*/agent.mcs.yml`). Edit instructions there, not in a copy.

- Flow and agent roles: see `docs/ARCHITECTURE.md`.
- Build order: Flow 1 Teams or email -> Jira -> Planning agent -> reply; Flow 2 adds GitHub and PR; Flow 3 adds Development, Validation, approval, Deployment, closure.
