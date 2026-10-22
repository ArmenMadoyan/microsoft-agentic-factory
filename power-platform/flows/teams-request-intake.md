# Teams request intake (flow)

Status: built and saved, trigger not yet verified (no run seen after two test posts).
These values were set in the designer form; the code view was not captured.

- Trigger: Microsoft Teams, "When a new channel message is added"
  - Team: a private single-member test team; Channel: `requests`
- Action: Microsoft Dataverse, "Add a new row" on `AgentRuns`
  - RunId = `concat('RUN-', formatDateTime(utcNow(), 'yyyyMMddHHmmss'))`
  - Agent = `Orchestrator`, Source = `teams`, Status = `received`

Design note: a trigger that fires on every chat message was rejected as too broad; this one is
scoped to one channel.
