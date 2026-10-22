# Sandbox agent (Copilot Studio child agent)

Processes large attachments (CSV, Parquet, xlsx; 1M+ rows) without sending rows through the model.

## Flow
1. User attaches a file in Teams or chat.
2. Agent flow saves it to Azure Blob `input/<run-id>/<file>` (Power Automate Azure Blob Storage connector).
3. Agent flow starts the Container Apps Job (`agenticsdlc-sandbox-job`) with args:
   `--input az://input/<run-id>/<file> --output az://output/<run-id> --task profile|script [--script ...]`
4. Worker (`sandbox/worker.py`) reads the blob, processes it with DuckDB, writes `summary.json` and result files to `output/<run-id>`.
5. Agent flow returns a summary and a link; the agent never receives raw rows.

## Agent instructions (paste into Copilot Studio)
You are the Sandbox Agent. You process large data files by delegating to the sandbox worker; you never read or reproduce raw rows yourself. For each request: save the attachment to storage, start the sandbox job with the right task, wait for completion, then return the row count, column summary and a link to the output files. If the job fails, return the error log and stop.

## Tested locally (Docker, `--network none --read-only --memory 2g`)
- `sales_1m.csv` (1,000,000 rows): profile and by-region aggregate correct.
- `sales_50k.xlsx`: profile correct.
- Azure paths (`az://`) and `infra/main.bicep` are NOT tested; no Azure subscription or `az` CLI was available.

## Azure notes
- Identity: user-assigned managed identity with Storage Blob Data Contributor; shared-key and public blob access are disabled.
- The Bicep job pulls `image` as given; add a registry and AcrPull role for a private ACR before deploying.
- Container Apps cannot fully block egress like `--network none`; use a locked-down VNet if the data requires it.
