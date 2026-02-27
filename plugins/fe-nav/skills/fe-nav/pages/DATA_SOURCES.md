# Data Sources — Browser Navigation

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/data-sources/:source` | Data Source Search | Search an external data source |

## Available data sources

| URL slug | Title | Search placeholder |
|----------|-------|--------------------|
| `fred` | FRED | `"Search federal reserve economic data..."` |
| `companies_house` | Companies House | `"Search companies house..."` |
| `web-research` | Web Research | `"Search web..."` |

## What you see (standard data sources: FRED, Companies House)

- Page title heading (e.g., "FRED", "Companies House")
- Search bar with source-specific placeholder + search button (magnifying glass)
- Results list with pagination
- Each result clickable → detail panel with metadata, documents, notes
- No results state (empty by default until search)

**Web Research** (`<domain>/data-sources/web-research`):
- Title: "Web Research"
- Subtitle: "Search the web for comprehensive research on any topic. Results include citations and sources."
- Search input: placeholder `"Search web..."`
- Mode dropdown: `"Snapshot"` (default) | `"Deep Research"` (3-5 min)
- Search button (magnifying glass)
- Results: markdown content with numbered citation sources

## UI Elements

**Inputs**: `"Select a Mode..."`, `"Search web..."`
**Dialogs**: `"Notes"`, `"Are you sure?"`
**Aria labels**: `"Mode"`

## Recipes

### Recipe: Navigate to Data Source Search

```
1. navigate("<domain>/data-sources/:source")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Search

```
1. click the search input (placeholder "Search web...")
2. type("your search query")
3. press_key("Enter")
4. wait(slow)
5. take_snapshot()
```

### Recipe: Search a data source

```
1. navigate("<domain>/data-sources/<source-slug>")
2. wait(fast)
3. click the search input
4. type("search query")
5. press_key("Enter")
6. wait(slow)  # results load
7. take_snapshot()  # find result titles
```

### Recipe: Web research

```
1. navigate("<domain>/data-sources/web-research")
2. click the search input (placeholder "Search web...")
3. type("your research question")
4. press_key("Enter")
5. wait(very_slow)  # research takes time
6. take_screenshot()
```
