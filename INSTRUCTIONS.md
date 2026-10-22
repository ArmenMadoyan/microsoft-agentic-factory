# Agentic SDLC Pipeline: Teams → Jira → Plan → Code → Fix → Deploy → Close

## Goal
An orchestrator agent takes an assignment posted in a Teams channel and drives it to
a closed Jira ticket, delegating each stage to a specialised sub-agent.

## Flow
1. **Intake**: Orchestrator reads the assignment from the Teams channel.
2. **Ticket**: Creates a Jira ticket and assigns it to itself.
3. **Plan**: Calls the *Planner* agent (open-source SDD, e.g. GitHub Spec Kit) to produce a spec and execution plan.
4. **Gather**: Calls the *Repo* agent (GitHub access) to clone and collect the relevant code.
5. **Execute**: *Dev* agent runs in Docker (or against Azure via `az`), reproduces the issue, and fixes it using Copilot CLI.
6. **Ship**: *Release* agent commits, pushes, opens a PR and deploys via GitHub Actions.
7. **Close**: Orchestrator comments on the Jira ticket with results and closes it.

## Agents
| Agent | Responsibility | Tools / MCPs |
|---|---|---|
| Orchestrator | State machine, delegation, memory, skills | Copilot Studio; Teams, Jira MCP |
| Planner | Spec + plan (SDD) | Spec Kit, Miro MCP (optional diagram) |
| Repo | Clone, search, gather context | GitHub MCP / `gh` |
| Dev | Reproduce + fix in sandbox | Docker, `az` CLI, Copilot CLI |
| Release | Commit, push, PR, deploy | GitHub MCP, GitHub Actions |

## Cross-cutting
- **Memory**: per-ticket state file (ticket id, plan, branch, PR, deploy URL) so any agent can resume.
- **Skills**: one skill per stage (`intake`, `plan`, `gather`, `fix`, `ship`, `close`).
- **MCPs**: Teams, Jira, GitHub, Miro.

## Walkthrough order (one agent at a time)
- [x] 0. GitHub account `ArmenMadoyan` connected + project repo created
- [x] 1. Repo agent (GitHub access)  ← scaffolded; seeded Python bug in app/pricing.py
- [x] 2. Orchestrator skeleton in Copilot Studio (generative orchestration on); memory still a JSON file
- [ ] 2b. Sandbox agent for large attachments (worker built and tested locally; Azure untested), see agents/sandbox-agent/
- [ ] 3. Jira MCP: create / assign / comment / close
- [ ] 4. Teams intake
- [ ] 5. Planner (SDD)
- [ ] 6. Dev agent (Docker + Copilot CLI, az later)
- [ ] 7. Release agent
- [ ] 8. End-to-end run on a seeded bug

## Open questions
- Copilot Studio vs. local-first: build and prove each agent locally (Copilot CLI + MCPs), then port to Copilot Studio.
- `az` CLI is not installed; install before step 6 if targeting Azure.

## Architecture v2: Power Platform backbone (decided)
```
Teams message -> Power Automate trigger -> Copilot Studio Orchestrator
  -> Dataverse (memory, AgentRuns) -> Jira -> Planning agent -> GitHub / Dev agent
  -> Validation -> Power Automate Approval (Teams Adaptive Card) -> Azure deployment
  -> Dataverse update -> Teams card -> Power BI
```
- **Power Automate**: event bus and action layer. Copilot Studio actions are backed by cloud flows.
- **Dataverse**: agent memory. Tables: Projects, Repositories, Incidents, Deployments, AgentRuns, ExecutionPlans. Replaces the JSON ticket file (schema: agents/memory/TICKET.template.json).
- **Custom connector** to an HTTP API in front of the harness and sandbox worker (needs an Azure Function or Container App; not built).
- **Approvals**: no deployment without a recorded human approval.
- **Power Apps**: control tower (requests, agent runs, failures, approve or reject). **Power BI**: success rate, resolution time, deployment frequency.
- **ALM**: environment variables for GitHub, Jira, Azure and endpoint URLs; `pac solution export` and `unpack` into `solution/`.

### Build order
1. Check tenant limits (Dataverse, custom connectors, DLP) with one small table.
2. Dataverse tables, then the Teams trigger flow and Copilot Studio call (Flow 1).
3. Jira flow, Planning agent, Teams reply.
4. Approval card, then GitHub and Dev agent, then deployment.
5. HTTP API and custom connector for harness and sandbox.
6. Power Apps control tower, Power BI, pac export.
