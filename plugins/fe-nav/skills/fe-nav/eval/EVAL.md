# FE Nav Eval Runner

Eval scenarios that validate the fe-nav skill works end-to-end via Chrome MCP.

## How to run

1. Ensure Chrome MCP is connected (`/chrome` in Claude Code)
2. Have the access-ui running locally at `http://localhost:5173/ui`
3. Be logged in (valid auth session in the browser)
4. Spawn a subagent with the eval scenario file + relevant skill context files

Example:

```
Read the following files for context, then follow the eval steps:
- skills/fe-nav/SKILL.md
- skills/fe-nav/pages/THREADS.md
- skills/fe-nav/eval/01_navigate_and_explore.md

Use <domain> = http://localhost:5173/ui
Use timing: fast=500, slow=2000, very_slow=5000
```

## Pass criteria

The subagent must complete the task using ONLY the skill files as guidance (no reading application source code). The recipes and UI element references in the skill files should be sufficient.

## Eval scenarios

| File | What it tests |
|------|---------------|
| `01_navigate_and_explore.md` | Navigate to major pages, take screenshots, verify layout |
| `02_send_message.md` | Open a thread, send a message, wait for AI response |
| `03_create_skill.md` | Create a new skill, verify it appears in the list |
