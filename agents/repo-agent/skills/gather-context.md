---
name: gather-context
description: Find and summarise the files relevant to a ticket in the target repo.
---
1. Read the ticket memory JSON.
2. Use `gh search code` / `rg` for keywords from the assignment.
3. List each hit with a one-line reason; include the matching test file.
4. Update `relevant_files` in the memory JSON and set `status: gathered`.
