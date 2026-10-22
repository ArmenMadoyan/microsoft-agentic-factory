# Deployment approval (flow)

Status: built and saved (instant flow); not yet run.

1. Trigger: "Manually trigger a flow" with one text input `RunId`.
2. Standard approvals, "Start and wait for an approval"
   - Type: Approve/Reject - First to respond
   - Title: `concat('Approve deployment for run ', triggerBody()?['text'])`
   - Assigned to: `<approver address>` (the test approver; use a manager or group in real use)
   - Details: "An AI-prepared change is ready for deployment. Approve only if validation passed and the plan was reviewed. Rejecting stops the run."
3. Dataverse, "Add a new row" on `AgentRuns` (audit record of the human decision)
   - RunId: `concat('APPROVAL-', formatDateTime(utcNow(), 'yyyyMMddHHmmss'))`
   - Agent: `Deployment Approval`
   - Status: the approval's Outcome (`Approve` or `Reject`)
   - Result: "Human decision recorded by Standard approvals before deployment."

Not yet wired: the Deployment Agent does not call this flow yet, and a rejection does not stop a
deployment because no deployment step exists. The Orchestrator and Deployment Agent instructions
require a recorded approval; this flow is where that record comes from.
