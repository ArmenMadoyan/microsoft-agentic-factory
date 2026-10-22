# Power Platform configs

Reference copies of what was built in the developer environment. They are documentation, not
deployable exports.

- `dataverse/AgentRuns.table.md`: table and columns
- `flows/email-request-intake.json`: trigger and action definitions from the designer's Code view
- `flows/teams-request-intake.md`: Teams flow settings

The real export (`pac solution export` then `unpack`) is in `solution/`; see `docs/solution-export.md`.
These files are readable summaries of the same flows. Connections and environment variables are
never committed.
