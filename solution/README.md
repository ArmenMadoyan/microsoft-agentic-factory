# AgenticSDLC solution (unpacked)

Exported with the Power Platform CLI and unpacked as unmanaged:

    pac solution export --name AgenticSDLC --path AgenticSDLC.zip --overwrite
    pac solution unpack --zipfile AgenticSDLC.zip --folder solution --packagetype Unmanaged

Contents: the `AgentRuns` Dataverse table (`Entities/cr8f1_AgentRuns`), the "Email request intake"
and "Teams request intake" flows (`Workflows/`), and connection references (`Other/Customizations.xml`).

## Sanitised values
Three environment-specific values were replaced with placeholders in `Workflows/`:
the sender allow-list address, the Teams team (group) id and the Teams channel id. Re-set them
after import. Connection references carry no credentials; connections must be created again by a
signed-in user in the target environment.

The publisher name still contains the source environment's org id (`org5b5587f4`).

The Copilot Studio agents are versioned separately as YAML in `copilot-studio/`.
