# 5D Claude Code Plugins

A plugin marketplace for Claude Code by Fifth Dimension AI.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| **granola** | Interact with Granola AI meeting notes — browse folders, read transcripts, and chat with meetings. |
| **fe-nav** | Navigate the Fifth Dimension access-ui web application using Chrome MCP browser automation. |

## Installation

### 1. Add the marketplace

In Claude Code, run:
```
/plugin marketplace add 5dai-dev/claude-plugins
```

### 2. Install a plugin

```
/plugin install granola@5dai-plugins
/plugin install fe-nav@5dai-plugins
```

## Plugin Details

### Granola

Browse your Granola meeting notes, get full transcripts, and chat with individual meetings or entire folders using Granola's AI.

**Prerequisites:** Granola desktop app installed and signed in (macOS).

**Capabilities:**
- List workspaces, folders, and documents
- Get full meeting transcripts with speaker attribution
- Chat with individual documents using Granola's AI
- Chat across all documents in a folder
- Auto-authentication via local Granola app credentials

### FE Nav

Navigate the Fifth Dimension access-ui web application using Chrome MCP browser automation.

**Prerequisites:** Chrome browser with Claude Code Chrome Connector extension (v1.0.36+).

**Capabilities:**
- Step-by-step recipes for every major page and workflow
- Auto-extracted UI element references (buttons, inputs, dialogs)
- Domain-agnostic (`<domain>` placeholder) — works with local dev, staging, and production
- Regeneration script to keep navigation files in sync with source code
