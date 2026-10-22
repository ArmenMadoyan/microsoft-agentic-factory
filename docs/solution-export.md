# AgenticSDLC solution export (`solution/`)

Exported with the Power Platform CLI and unpacked as unmanaged:

    pac solution export --name AgenticSDLC --path AgenticSDLC.zip --overwrite
    pac solution unpack --zipfile AgenticSDLC.zip --folder solution --packagetype Unmanaged

Note: unpacking with `--allowDelete true` clears unknown files in `solution/`, so keep docs
outside that folder (this file lives in `docs/` for that reason).

## Contents (re-exported after the Orchestrator step, approval flow and app were added)
- `AgentRuns` Dataverse table: `Entities/cr8f1_AgentRuns` (columns, forms, views)
- Cloud flows in `Workflows/`:
  - "Email request intake": Outlook trigger, writes an `AgentRuns` row, calls the Orchestrator
  - "Teams request intake": channel-message trigger, writes a row, calls the Orchestrator
  - "Deployment approval": manual trigger, Standard approval, writes an audit row
- Model-driven app "Agentic Control Tower": `AppModules/cr8f1_AgenticControlTower`
- Connection references (Dataverse, Outlook, Teams, Standard approvals): `Other/Customizations.xml`

## Sanitised values
Replaced with placeholders in `Workflows/`: the sender allow-list address, the approver
address, the Teams team (group) id and the Teams channel id. Re-set them after an import.
Connection references carry no credentials; connections must be created again by a signed-in
user in the target environment. The publisher name still contains the source environment's org id.

## Not in this export
- Copilot Studio agents: versioned as YAML in `copilot-studio/`.
- Jira integration: not built.
