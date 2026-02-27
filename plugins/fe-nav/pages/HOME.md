# Home / Dashboard — Browser Navigation

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/home` | Home | Welcome screen, tool cards, search, tag filters |

## What you see

- Welcome heading: "Welcome back, {name}" (user's display name)
- Subtitle: "Agentic AI for Real Estate"
- Search input: placeholder `"Search..."`
- Tag filter pills: `"All"` (orange, selected by default) + dynamic tag buttons
- Tool cards grid (filtered by search + selected tag)
- Each card: icon/emoji, tool name, description (clickable)
- Empty state: "No results found." + "Try adjusting your search terms"

## UI Elements

**Inputs**: `"Search..."`

## Recipes

### Recipe: Navigate to Home

```
1. navigate("<domain>/home")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Search

```
1. click the search input (placeholder "Search...")
2. type("your search query")
3. press_key("Enter")
4. wait(slow)
5. take_snapshot()
```

### Recipe: Search and launch a tool

```
1. navigate("<domain>/home")
2. wait(fast)  # cards load
3. type("lease")  # search is auto-focused
4. wait(fast)  # cards filter
5. take_snapshot()  # find matching tools
6. click("<tool name>")
```

### Recipe: Filter by tag

```
1. navigate("<domain>/home")
2. wait(fast)
3. click("<tag name>")  # e.g., a category tag
4. take_snapshot()  # see filtered tools
```
