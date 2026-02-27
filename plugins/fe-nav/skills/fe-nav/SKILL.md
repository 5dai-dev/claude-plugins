---
name: fe-nav
description: >
  Navigate the Fifth Dimension access-ui web application using Chrome MCP
  browser automation. Triggers: navigating the website, clicking UI elements,
  testing the frontend, browser automation, Chrome MCP, access-ui.
---

# Fifth Dimension access-ui — Browser Navigation

> **Prerequisites**: See [SETUP.md](./SETUP.md) for Chrome MCP setup.
> **Regeneration**: See [REGENERATE.md](./REGENERATE.md) to update these files from source.

## Domain

Replace `<domain>` in all URLs below with your target environment:

| Environment | Base URL |
|-------------|----------|
| Local dev | `http://localhost:8502/ui` (can change - check running access-ui container in local-dev) |
| Staging | `https://access-test.5dai.io/ui` |
| Production | `https://access.5dai.io/ui` |
| Production US | `https://access.us.5dai.io/ui` |

## Timing

Recipes use timing labels instead of milliseconds. Adjust for your environment:

| Label | Delay | Use for |
|-------|-------|---------|
| `fast` | 500-1000ms | UI transitions, dialogs, tab switches |
| `slow` | 2000-3000ms | Page navigation, data fetching |
| `very_slow` | 5000-10000ms | AI responses, file uploads, heavy processing |

## Chrome MCP Tools

| Tool | Use for |
|------|---------|
| `navigate` | Go to a URL |
| `click` | Click a button, link, or element |
| `type` | Enter text into a focused input |
| `take_screenshot` | Capture what's visible |
| `take_snapshot` | Get accessibility tree — best for finding elements |
| `press_key` | Keyboard events (Enter, Escape, Tab) |
| `hover` | Trigger tooltips or hover states |
| `wait` | Pause for loading/animations |

**Tip**: Use `take_snapshot()` to get the accessibility tree, then use element labels/roles to target `click` and `type` calls.

## Site Map

<!-- AUTO:SITE_MAP_START -->

### Public pages (no auth required)

| URL | Page | Description |
|-----|------|-------------|
| `/sign-in` | Sign In | Email input, magic link sent |
| `/auth?token=...` | Token Verify | Validates magic link token |
| `/otp?token=...` | OTP Exchange | Exchanges one-time password |
| `/sso-callback` | SSO Callback | Handles SAML SSO response |

### Authenticated pages (redirect to /sign-in if not logged in)

| URL | Page | Description |
|-----|------|-------------|
| `/workspace/threads` | Threads List | All conversation threads with read/unread tabs |
| `/workspace/thread/new` | New Thread | Start a new conversation |
| `/workspace/thread/:id` | Thread Detail | Chat messages, document sidebar, preview panel |
| `/skills` | Skills List | Grid/list of skills with search |
| `/skills/:id` | Skill Detail | View/edit skill name, description, instructions |
| `/data-rooms` | Data Rooms Index | Redirects to first data room |
| `/data-rooms/:id/entries/:path` | Data Room Browser | File/folder table, upload, search |
| `/data-rooms/new` | New Data Room | Connect SharePoint or Box |
| `/data-sources/:source` | Data Source Search | Search an external data source |
| `/home` | Home | Welcome screen, tool cards, search, tag filters |
| `/toolkit` | Toolkit | Team workflows with Launch Now cards |

### Global layout (present on all authenticated pages)

- **Left sidebar**: collapsible — Home, Toolkit, Skills, Threads, Data Rooms, Data Sources
- **Header bar**: sidebar toggle (hamburger), "New Thread" button (orange, top-right)
- **User dropdown**: bottom of sidebar — avatar, name, org, "Sign out"
- **Support**: "Contact Support" link in sidebar footer

<!-- AUTO:SITE_MAP_END -->

## Area Files

<!-- AUTO:AREA_TABLE_START -->

| File | When to read |
|------|-------------|
| [`AUTH.md`](./pages/AUTH.md) | Sign in, sign out, token flows |
| [`THREADS.md`](./pages/THREADS.md) | Thread list, creating threads, chatting, attachments, feedback |
| [`SKILLS.md`](./pages/SKILLS.md) | Creating, editing, sharing, deleting skills |
| [`DATA_ROOMS.md`](./pages/DATA_ROOMS.md) | Browsing files, uploading documents, searching data rooms |
| [`DATA_CONNECTIONS.md`](./pages/DATA_CONNECTIONS.md) | SharePoint/Box OAuth, connect drives, sync folders |
| [`DATA_SOURCES.md`](./pages/DATA_SOURCES.md) | External data source search, web research |
| [`HOME.md`](./pages/HOME.md) | Dashboard, tool cards, prompt suggestions, search |
| [`TOOLKIT.md`](./pages/TOOLKIT.md) | Workflow launcher, team selector, recent executions |
| [`SIDEBAR.md`](./pages/SIDEBAR.md) | Navigation sidebar, switching pages, sign out |

<!-- AUTO:AREA_TABLE_END -->
