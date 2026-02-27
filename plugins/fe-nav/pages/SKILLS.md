# Skills — Browser Navigation

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/skills` | Skills List | Grid/list of skills with search |
| `<domain>/skills/:id` | Skill Detail | View/edit skill name, description, instructions |

## What you see

**Skills List:**
- Header: "Skills" + description text
- "Create Skill" button (top-right), search input, grid/list toggle
- Grid of skill cards: name, owner badge, description (each clickable)

**Skill Detail:**
- Back arrow, skill name (h1), owner badge, "Updated ..." date
- "Run" button (orange gradient, play icon)
- Form: Name input, Description textarea, Instructions textarea (monospace)
- "Save" button (outline, right-aligned)
- Sharing section: private/shared status, "Edit" button
- Danger zone: "Delete" button (red)

## UI Elements

**Buttons**: `"Delete"`, `"Edit"`, `"Browse Skills"`
**Inputs**: `"e.g., Lease Summary Extractor"`, `"Describe what this process does and when to use it. e.g.,"`, `"Describe the process step by step — the way you"`, `"Search users..."`, `"Search skills..."`
**Dialogs**: `"Delete Skill"`, `"Unsaved changes"`, `"Create Skill"`, `"Discard changes?"`
**Dropdown items**: `"Create with {assistantName}"`, `"Create manually"`
**Aria labels**: `"Grid view"`, `"List view"`

## Recipes

### Recipe: Navigate to Skills List

```
1. navigate("<domain>/skills")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Navigate to Skill Detail

```
1. navigate("<domain>/skills/:id")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Search

```
1. click the search input (placeholder "Search skills...")
2. type("your search query")
3. press_key("Enter")
4. wait(slow)
5. take_snapshot()
```

### Recipe: Create a skill

```
1. navigate("<domain>/skills")
2. click("Create Skill")  # or use dropdown for "Create manually"
3. wait(fast)
4. type("My Skill Name")  # name input
5. click the Description textarea
6. type("What this skill does")
7. click the Instructions textarea
8. type("Step 1: Do this\nStep 2: Do that")
9. click("Create Skill")  # submit in dialog footer
10. wait(slow)
11. take_screenshot()
```

### Recipe: Edit a skill

```
1. navigate("<domain>/skills/<skillId>")
2. wait(fast)
3. triple-click the Name input to select all
4. type("Updated Skill Name")
5. click("Save")
6. wait(fast)
7. take_screenshot()
```

### Recipe: Run a skill

```
1. navigate("<domain>/skills/<skillId>")
2. click("Run")  # navigates to new thread with skill pre-filled
3. wait(slow)
4. take_screenshot()
```

### Recipe: Delete a skill

```
1. navigate("<domain>/skills/<skillId>")
2. scroll to bottom
3. click("Delete")  # in danger zone
4. click the confirm button in dialog
5. wait(fast)
```
