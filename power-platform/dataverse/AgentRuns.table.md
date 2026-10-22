# Dataverse table: AgentRuns

Created in a developer environment (publisher prefix `cr8f1`). Customizations must be published
(Solutions -> Publish all customizations) before flows and Studio can list the table.

| Display name | Schema name | Type | Notes |
|---|---|---|---|
| RunId | cr8f1_RunId | Single line of text | Primary name column, required. Flows set `RUN-<yyyyMMddHHmmss>` |
| Ticket | cr8f1_Ticket | Single line of text | Jira key, filled later |
| Agent | cr8f1_Agent | Single line of text | Which agent handled the step |
| Source | cr8f1_Source | Single line of text | `email` or `teams` |
| Status | cr8f1_Status | Single line of text | `received`, then later stages |
| Result | cr8f1_Result | Text area | Outcome summary |

Logical name `cr8f1_agentruns`; the flow's table value is the collection name `cr8f1_agentrunses`.
Created-on and modified-on system columns stand in for start and end time.
