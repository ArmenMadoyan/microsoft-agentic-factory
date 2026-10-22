# Copilot Studio definitions

`engineering-software-factory-orchestrator/` was cloned from Copilot Studio with the VS Code
Copilot Studio extension and contains the agent as YAML:

- `agent.mcs.yml`, `settings.mcs.yml`: the Orchestrator (generative orchestration on)
- `agents/<name>/agent.mcs.yml`: Planning, Development, Validation, Deployment and Sandbox child agents
- `agents/Development Agent/actions/`: the GitHub MCP tool reference
- `connectionreferences.mcs.yml`: names the GitHub connection reference (no credentials)
- `topics/`: default system topics

## Not committed
The extension's `.mcs/` folder (environment endpoint, account info, change token, full bot
definition) is deliberately left out. It is recreated by cloning the agent again.

## Using it
1. Install the Copilot Studio VS Code extension and sign in to the target environment.
2. Clone the agent (this recreates `.mcs/`), then copy the YAML from this folder over it.
3. Apply the changes to Copilot Studio from the extension.

This round trip (apply to a fresh environment) has not been tested. Connections such as GitHub
must be created again by a signed-in user in the target environment.
