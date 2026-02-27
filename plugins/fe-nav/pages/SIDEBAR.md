# Sidebar — Browser Navigation

## What you see

The sidebar is visible on ALL authenticated pages (left side).

**Sections (top to bottom):**
1. Header: "Fifth Dimension" logo (orange "5D" icon) + text
2. Main nav: "Home" (house icon)
3. Threads section:
   - "New Thread" (green + icon, highlighted orange) → `/workspace/thread/new`
   - Recent thread list (up to ~5), each with bullet dot and truncated title
   - "All Threads" link → `/workspace/threads` (with unread badge count)
4. Library section:
   - "Skills" → `/skills` (may show "New" badge)
5. Data Rooms section:
   - "Data Rooms" (collapsible with chevron): "My Data Room", "Shared", plus any additional rooms
6. Data Sources section:
   - "FRED" (chart icon) → `/data-sources/fred`
   - "Web Research" (globe icon) → `/data-sources/web-research`
   - "Companies House" (building icon) → `/data-sources/companies_house`
7. Footer: "Knowledge Base" link, "Contact Support" link, user profile dropdown

**Global header (top-right, present on all pages):**
- "New Thread" button (orange with + icon) → `/workspace/thread/new`

**States:** Expanded (full labels) | Collapsed (icons only, toggle via hamburger)

**User dropdown (click profile at bottom):** "5D" avatar, display name, org name, "Sign out"

## UI Elements

**Dialogs**: `"Toolkit"`, `"Library"`, `"Skills"`, `"Data Rooms"`, `"Add Data Room"`, `"Data Sources"`, `"Web Research"`, `"Companies House"`, `"Workflows"`, `"Threads"`, `"New Thread"`, `"All Threads"`
**Dropdown items**: `"Sign out"`
**Aria labels**: `"Branched"`, `"Copied"`

## Recipes

### Recipe: Navigate via sidebar

```
1. take_snapshot()  # find sidebar items
2. click("Home")  # or "Toolkit", "Skills", etc.
3. wait(fast)
4. take_screenshot()
```

### Recipe: Open a thread from sidebar

```
1. take_snapshot()  # find thread subjects in sidebar
2. click("<thread subject>")
3. wait(slow)
```

### Recipe: Collapse/expand sidebar

```
1. click the sidebar trigger (hamburger icon in header)
```

### Recipe: Sign out

```
1. click the user avatar at bottom of sidebar
2. click("Sign out")
```
