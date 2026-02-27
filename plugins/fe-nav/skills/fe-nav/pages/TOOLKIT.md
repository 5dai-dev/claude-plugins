# Toolkit — Browser Navigation

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/toolkit` | Toolkit | Team workflows with Launch Now cards |

## What you see

- Welcome heading: "Welcome back, {name}" (user's display name)
- Subtitle: "Agentic AI for Real Estate.  your team" (with dropdown link)
- Team selector: click underlined "your team" link → dropdown of teams
  - May show "No teams available" if user has no teams
- Section heading: "{team name} Workflows" or "No team selected Workflows"
- Subtitle: "Select a workflow to get started with AI-powered automation"
- Workflow cards grid (when team has workflows):
  - Each: icon, name, description, usage stats, "Launch Now" button
- "Ask Ellie" card (always present):
  - Chat icon, description, example prompt text
  - Tags: "AI Expert", "Analysis", "RE Focus"
  - `"Start a Conversation"` button (orange with send icon)

## Recipes

### Recipe: Navigate to Toolkit

```
1. navigate("<domain>/toolkit")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Launch a workflow

```
1. navigate("<domain>/toolkit")
2. wait(slow)  # cards load
3. take_snapshot()  # find workflow names
4. click("Launch Now")  # on the desired card
5. wait(slow)  # thread created, redirected
6. take_screenshot()
```

### Recipe: Switch team

```
1. navigate("<domain>/toolkit")
2. click the team name link (underlined text near subtitle)
3. click("<team name>")  # select from dropdown
4. wait(fast)  # cards reload
```

### Recipe: Start a freeform conversation

```
1. navigate("<domain>/toolkit")
2. scroll to the "Ask {assistantName}" card
3. click("Start a Conversation")
4. wait(slow)  # new thread opens
```
