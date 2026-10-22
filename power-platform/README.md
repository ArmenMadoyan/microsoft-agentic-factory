# Power Platform configs

Reference copies of what was built in the developer environment. They are documentation, not
deployable exports.

- `dataverse/AgentRuns.table.md`: table and columns
- `flows/email-request-intake.json`: trigger and action definitions from the designer's Code view
- `flows/teams-request-intake.md`: Teams flow settings

For deployable source control, export a solution with the Power Platform CLI
(`pac solution export`, then `pac solution unpack`) and commit the result to `solution/`.
Not done yet. Connections and environment variables are never committed.
