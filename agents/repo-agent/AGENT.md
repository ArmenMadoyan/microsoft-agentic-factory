# Repo agent

Purpose: gather the code context a ticket needs and hand it to the Dev agent.
Access: GitHub only (GitHub MCP / `gh`). Read-only; it never commits or pushes.

## Input
Path to the ticket memory file (`agents/memory/<TICKET>.json`) containing `assignment` and `plan`.

## Steps
1. Clone or update `repo` into a workspace dir; check out the default branch.
2. Search for files and symbols mentioned in `assignment` / `plan`.
3. Read the matching files and their tests.
4. Write `relevant_files` (path plus one-line reason each) back into the memory file and set `status` to `gathered`.

## Output
Updated memory file only. No code changes.
