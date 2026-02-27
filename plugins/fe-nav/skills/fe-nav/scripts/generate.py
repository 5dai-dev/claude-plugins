#!/usr/bin/env python3
"""
Generates browser-navigation context files for the access-ui frontend.

Scans the access-ui source tree to extract UI elements (buttons, inputs,
dialogs, etc.) and produces per-area markdown files that describe the
rendered website for Chrome MCP browser automation.

Usage:
    python generate.py --src <path-to-access-ui/src>
    python generate.py --src ~/workspace/m5/application/access-ui/src --out ./pages
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class RouteConfig:
    """A single route/page within an area."""

    route_file: str  # relative path under src/routes, e.g. "_public/sign-in.tsx"
    url_path: str  # URL path, e.g. "/sign-in"
    label: str  # human-readable page name
    description: str  # short description
    public: bool = False  # True for unauthenticated pages


@dataclass
class RecipeConfig:
    """A step-by-step Chrome MCP recipe."""

    title: str
    steps: list[str]


@dataclass
class AreaConfig:
    """Declarative config for one area of the app."""

    key: str  # e.g. "AUTH", used as filename
    title: str  # e.g. "Auth"
    when_to_read: str  # description for area-file table in SKILL.md
    routes: list[RouteConfig] = field(default_factory=list)
    component_dirs: list[str] = field(default_factory=list)
    layout_notes: str = ""  # 3-8 line overview of what you see
    recipes: list[RecipeConfig] = field(default_factory=list)


@dataclass
class ScanData:
    """Extracted UI elements from component source code."""

    buttons: list[str] = field(default_factory=list)
    placeholders: list[str] = field(default_factory=list)
    dialogs: list[str] = field(default_factory=list)
    aria_labels: list[str] = field(default_factory=list)
    dropdown_items: list[str] = field(default_factory=list)
    tabs: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Source-code extraction helpers
# ---------------------------------------------------------------------------

# Regex for JSX template expressions like {variable}, {foo.bar}, {isX ? ... : ...}
_JSX_EXPR = re.compile(r"^\{.*\}$")
# Regex for HTML entities
_HTML_ENTITY = re.compile(r"&\w+;")


def _is_template_expr(s: str) -> bool:
    """Return True if s looks like a JSX template expression."""
    return bool(_JSX_EXPR.match(s.strip()))


def _clean_items(items: list[str]) -> list[str]:
    """Filter out template expressions, HTML entities, and very short strings."""
    result: list[str] = []
    for item in items:
        item = item.strip()
        if not item:
            continue
        if _is_template_expr(item):
            continue
        if _HTML_ENTITY.search(item):
            continue
        if "$" in item and "{" in item:
            continue
        result.append(item)
    return list(dict.fromkeys(result))  # dedupe preserving order


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def list_files(directory: Path, ext: tuple[str, ...] = (".ts", ".tsx")) -> list[Path]:
    if not directory.exists():
        return []
    result = []
    for root, _dirs, files in os.walk(directory):
        for f in sorted(files):
            if f.endswith(ext):
                result.append(Path(root) / f)
    return result


def extract_button_labels(text: str) -> list[str]:
    """Extract visible button text from JSX."""
    labels: list[str] = []
    for m in re.finditer(
        r"<(?:Button|button)[^>]*>\s*(?:<[^>]+>\s*)?([^<{][^<]*?)\s*</", text
    ):
        label = m.group(1).strip().strip("\"'")
        if label and not label.startswith("{") and len(label) < 60:
            labels.append(label)
    for m in re.finditer(r'>\s*["\'`]([A-Z][^"\'`]{1,40})["\'`]\s*</', text):
        labels.append(m.group(1))
    return _clean_items(labels)


def extract_placeholders(text: str) -> list[str]:
    """Extract placeholder and placeholderSearchText values."""
    items: list[str] = []
    items.extend(
        re.findall(r'placeholder\s*[=:]\s*[{]?\s*["\'`]([^"\'`]+)["\'`]', text)
    )
    items.extend(
        re.findall(
            r'placeholderSearchText\s*[=:]\s*[{]?\s*["\'`]([^"\'`]+)["\'`]', text
        )
    )
    return _clean_items(items)


def extract_dialog_titles(text: str) -> list[str]:
    titles: list[str] = []
    for m in re.finditer(
        r"<(?:Dialog|Sheet|AlertDialog)Title[^>]*>\s*[\"'`]?([^<\"'`{][^<]*?)\s*[\"'`]?\s*</",
        text,
    ):
        titles.append(m.group(1).strip())
    for m in re.finditer(
        r"(?:title|confirmTitle)\s*[=:]\s*[\"'`]([^\"'`]+)[\"'`]", text
    ):
        t = m.group(1).strip()
        # Filter tooltip-like short strings (single words < 5 chars)
        if len(t) >= 5 or " " in t:
            titles.append(t)
    return _clean_items(titles)


def extract_aria_labels(text: str) -> list[str]:
    items = re.findall(r'aria-label\s*[=:]\s*[{]?\s*["\'`]([^"\'`]+)["\'`]', text)
    return _clean_items(items)


def extract_dropdown_items(text: str) -> list[str]:
    items: list[str] = []
    for m in re.finditer(
        r"<DropdownMenuItem[^>]*>\s*(?:<[^>]+>\s*)*[\"'`]?([^<{][^<]*?)[\"'`]?\s*</",
        text,
    ):
        label = m.group(1).strip()
        if label and len(label) < 60:
            items.append(label)
    return _clean_items(items)


def extract_tab_labels(text: str) -> list[str]:
    labels: list[str] = []
    for m in re.finditer(
        r"<TabsTrigger[^>]*>\s*[\"'`]?([^<{][^<]*?)[\"'`]?\s*</", text
    ):
        labels.append(m.group(1).strip())
    return _clean_items(labels)


def scan_component_dir(src: Path, dirname: str) -> ScanData:
    """Scan a component directory and extract all visible UI elements."""
    comp_dir = src / "components" / dirname
    data = ScanData()
    for f in list_files(comp_dir):
        text = read_text(f)
        data.buttons.extend(extract_button_labels(text))
        data.placeholders.extend(extract_placeholders(text))
        data.dialogs.extend(extract_dialog_titles(text))
        data.aria_labels.extend(extract_aria_labels(text))
        data.dropdown_items.extend(extract_dropdown_items(text))
        data.tabs.extend(extract_tab_labels(text))
    # Dedupe each field
    data.buttons = list(dict.fromkeys(data.buttons))
    data.placeholders = list(dict.fromkeys(data.placeholders))
    data.dialogs = list(dict.fromkeys(data.dialogs))
    data.aria_labels = list(dict.fromkeys(data.aria_labels))
    data.dropdown_items = list(dict.fromkeys(data.dropdown_items))
    data.tabs = list(dict.fromkeys(data.tabs))
    return data


def merge_scan_data(*scans: ScanData) -> ScanData:
    """Merge multiple ScanData into one, deduplicating."""
    merged = ScanData()
    for s in scans:
        merged.buttons.extend(s.buttons)
        merged.placeholders.extend(s.placeholders)
        merged.dialogs.extend(s.dialogs)
        merged.aria_labels.extend(s.aria_labels)
        merged.dropdown_items.extend(s.dropdown_items)
        merged.tabs.extend(s.tabs)
    merged.buttons = list(dict.fromkeys(merged.buttons))
    merged.placeholders = list(dict.fromkeys(merged.placeholders))
    merged.dialogs = list(dict.fromkeys(merged.dialogs))
    merged.aria_labels = list(dict.fromkeys(merged.aria_labels))
    merged.dropdown_items = list(dict.fromkeys(merged.dropdown_items))
    merged.tabs = list(dict.fromkeys(merged.tabs))
    return merged


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _render_ui_elements(scan: ScanData) -> str:
    """Render auto-extracted UI elements as markdown subsections."""
    sections: list[str] = []

    if scan.buttons:
        items = ", ".join(f'`"{b}"`' for b in scan.buttons)
        sections.append(f"**Buttons**: {items}")

    if scan.placeholders:
        items = ", ".join(f'`"{p}"`' for p in scan.placeholders)
        sections.append(f"**Inputs**: {items}")

    if scan.dialogs:
        items = ", ".join(f'`"{d}"`' for d in scan.dialogs)
        sections.append(f"**Dialogs**: {items}")

    if scan.dropdown_items:
        items = ", ".join(f'`"{d}"`' for d in scan.dropdown_items)
        sections.append(f"**Dropdown items**: {items}")

    if scan.tabs:
        items = ", ".join(f'`"{t}"`' for t in scan.tabs)
        sections.append(f"**Tabs**: {items}")

    if scan.aria_labels:
        items = ", ".join(f'`"{a}"`' for a in scan.aria_labels)
        sections.append(f"**Aria labels**: {items}")

    return "\n".join(sections)


def _render_recipes(recipes: list[RecipeConfig]) -> str:
    """Render manual recipes."""
    parts: list[str] = []
    for recipe in recipes:
        parts.append(f"### Recipe: {recipe.title}\n")
        parts.append("```")
        for i, step in enumerate(recipe.steps, 1):
            parts.append(f"{i}. {step}")
        parts.append("```")
        parts.append("")
    return "\n".join(parts)


def _render_auto_recipes(config: AreaConfig, scan: ScanData) -> str:
    """Generate automatic recipes from routes and scan data."""
    parts: list[str] = []

    # Navigate-to recipe for each route
    for route in config.routes:
        url = f"<domain>{route.url_path}" if not route.url_path.startswith("<") else route.url_path
        parts.append(f"### Recipe: Navigate to {route.label}\n")
        parts.append("```")
        parts.append(f'1. navigate("{url}")')
        parts.append("2. wait(slow)")
        parts.append("3. take_screenshot()")
        parts.append("```")
        parts.append("")

    # Search recipe if a search placeholder is found
    search_placeholders = [
        p for p in scan.placeholders if "search" in p.lower()
    ]
    if search_placeholders:
        # Prefer placeholder that matches the area title (e.g. "Search skills..." for Skills)
        title_lower = config.title.lower()
        matching = [p for p in search_placeholders if title_lower in p.lower()]
        ph = matching[0] if matching else search_placeholders[-1]
        parts.append("### Recipe: Search\n")
        parts.append("```")
        parts.append(f'1. click the search input (placeholder "{ph}")')
        parts.append('2. type("your search query")')
        parts.append("3. press_key(\"Enter\")")
        parts.append("4. wait(slow)")
        parts.append("5. take_snapshot()")
        parts.append("```")
        parts.append("")

    return "\n".join(parts)


def render_area(config: AreaConfig, scan: ScanData) -> str:
    """Render a complete area markdown file."""
    lines: list[str] = []

    # Title
    lines.append(f"# {config.title} — Browser Navigation\n")

    # Pages table
    if config.routes:
        lines.append("## Pages\n")
        lines.append("| URL | Page | Description |")
        lines.append("|-----|------|-------------|")
        for r in config.routes:
            url = f"`<domain>{r.url_path}`"
            lines.append(f"| {url} | {r.label} | {r.description} |")
        lines.append("")

    # Layout notes
    if config.layout_notes:
        lines.append("## What you see\n")
        lines.append(config.layout_notes)
        lines.append("")

    # UI Elements (auto-extracted)
    ui_elements = _render_ui_elements(scan)
    if ui_elements:
        lines.append("## UI Elements\n")
        lines.append(ui_elements)
        lines.append("")

    # Auto-generated recipes
    auto = _render_auto_recipes(config, scan)
    if auto:
        lines.append("## Recipes\n")
        lines.append(auto)

    # Manual recipes
    if config.recipes:
        if not auto:
            lines.append("## Recipes\n")
        lines.append(_render_recipes(config.recipes))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Area configurations
# ---------------------------------------------------------------------------

AREAS: list[AreaConfig] = [
    AreaConfig(
        key="AUTH",
        title="Auth",
        when_to_read="Sign in, sign out, token flows",
        routes=[
            RouteConfig(
                "_public/sign-in.tsx",
                "/sign-in",
                "Sign In",
                "Email input, magic link sent",
                public=True,
            ),
            RouteConfig(
                "_public/auth.tsx",
                "/auth?token=...",
                "Token Verify",
                "Validates magic link token",
                public=True,
            ),
            RouteConfig(
                "_public/otp.tsx",
                "/otp?token=...",
                "OTP Exchange",
                "Exchanges one-time password",
                public=True,
            ),
            RouteConfig(
                "_public/sso-callback.tsx",
                "/sso-callback",
                "SSO Callback",
                "Handles SAML SSO response",
                public=True,
            ),
        ],
        component_dirs=["sign-in"],
        layout_notes="""\
- Centered card: "Sign in to Fifth Dimension"
- Email input (auto-focused), placeholder `"you@example.com"`
- "Sign In" button (full width, shows spinner while loading)
- If email is `@fifthdimensionai.com`: a "Customer ID" field appears
- Error state: `"Something went wrong. Try again."` (red, below button)
- After submit: "check your email" confirmation screen""",
        recipes=[
            RecipeConfig(
                "Sign in",
                [
                    'navigate("<domain>/sign-in")',
                    'type("user@example.com")  # email field is auto-focused',
                    'click("Sign In")',
                    "wait(slow)  # magic link flow",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Sign out",
                [
                    "click the user avatar at bottom-left of sidebar",
                    'click("Sign out")',
                ],
            ),
        ],
    ),
    AreaConfig(
        key="THREADS",
        title="Threads",
        when_to_read="Thread list, creating threads, chatting, attachments, feedback",
        routes=[
            RouteConfig(
                "_app/workspace/threads.tsx",
                "/workspace/threads",
                "Threads List",
                "All conversation threads with read/unread tabs",
            ),
            RouteConfig(
                "_app/workspace/thread/$id.tsx",
                "/workspace/thread/NEW",
                "New Thread",
                "Start a new conversation",
            ),
            RouteConfig(
                "_app/workspace/thread/$id.tsx",
                "/workspace/thread/:id",
                "Thread Detail",
                "Chat messages, document sidebar, preview panel",
            ),
        ],
        component_dirs=[
            "workspace-threads",
            "workspace-thread",
            "message-feedback",
            "message-toolbar",
        ],
        layout_notes="""\
**Threads List:**
- Header "Threads" with "All" | "Unread" tabs (orange badge count)
- Scrollable list of thread cards: icon, subject, status badge, preview, timestamp
- Each card is clickable (navigates to thread detail)

**Thread Detail (3-panel):**
- Left/center: Chat column with message history + input area
- Right sidebar: Documents panel (Attached, Generated, References sections)
- Far right: Document preview panel (opens on demand)
- Chat input: textarea with paperclip (attach), prompt library, skills dropdown
- Submit: "Send" button with dropdown for "Send in Chat" / "Send via Email"
- While processing: "Processing..." button, then "Stop" to cancel""",
        recipes=[
            RecipeConfig(
                "Send a message in existing thread",
                [
                    'navigate("<domain>/workspace/thread/<threadId>")',
                    "wait(slow)  # messages load",
                    'click the textarea (placeholder "Type your message...")',
                    'type("Your message here")',
                    'click("Send")',
                    "wait(very_slow)  # AI response",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Start a new thread",
                [
                    'navigate("<domain>/workspace/thread/NEW")',
                    "wait(fast)",
                    'click the subject input (placeholder "Enter subject...")',
                    'type("My new thread subject")',
                    'click the textarea (placeholder "Start your conversation...")',
                    'type("Hello, I have a question about...")',
                    'click("Send")',
                    "wait(very_slow)  # AI response",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Attach a document from data room",
                [
                    "(on thread detail page)",
                    "click the paperclip icon (attach button, bottom-left of input)",
                    "wait(fast)  # attachment sheet opens",
                    "click the data room name in left sidebar of sheet",
                    "wait(fast)  # file list loads",
                    "click the checkbox next to desired file(s)",
                    'press_key("Escape")  # close sheet',
                ],
            ),
            RecipeConfig(
                "Rename a thread",
                [
                    "(on thread detail page)",
                    'click the gear icon (aria-label "Thread settings")',
                    'click("Rename Thread")',
                    'type("New thread name")',
                    'press_key("Enter")',
                ],
            ),
            RecipeConfig(
                "Delete a thread",
                [
                    "(on thread detail page)",
                    'click the gear icon (aria-label "Thread settings")',
                    'click("Delete Thread")',
                    "click the confirm button in the dialog",
                ],
            ),
        ],
    ),
    AreaConfig(
        key="SKILLS",
        title="Skills",
        when_to_read="Creating, editing, sharing, deleting skills",
        routes=[
            RouteConfig(
                "_app/skills/index.tsx",
                "/skills",
                "Skills List",
                "Grid/list of skills with search",
            ),
            RouteConfig(
                "_app/skills/$id.tsx",
                "/skills/:id",
                "Skill Detail",
                "View/edit skill name, description, instructions",
            ),
        ],
        component_dirs=["skills"],
        layout_notes="""\
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
- Danger zone: "Delete" button (red)""",
        recipes=[
            RecipeConfig(
                "Create a skill",
                [
                    'navigate("<domain>/skills")',
                    'click("Create Skill")  # or use dropdown for "Create manually"',
                    "wait(fast)",
                    'type("My Skill Name")  # name input',
                    "click the Description textarea",
                    'type("What this skill does")',
                    'click the Instructions textarea',
                    'type("Step 1: Do this\\nStep 2: Do that")',
                    'click("Create Skill")  # submit in dialog footer',
                    "wait(slow)",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Edit a skill",
                [
                    'navigate("<domain>/skills/<skillId>")',
                    "wait(fast)",
                    "triple-click the Name input to select all",
                    'type("Updated Skill Name")',
                    'click("Save")',
                    "wait(fast)",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Run a skill",
                [
                    'navigate("<domain>/skills/<skillId>")',
                    'click("Run")  # navigates to new thread with skill pre-filled',
                    "wait(slow)",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Delete a skill",
                [
                    'navigate("<domain>/skills/<skillId>")',
                    "scroll to bottom",
                    'click("Delete")  # in danger zone',
                    "click the confirm button in dialog",
                    "wait(fast)",
                ],
            ),
        ],
    ),
    AreaConfig(
        key="DATA_ROOMS",
        title="Data Rooms",
        when_to_read="Browsing files, uploading documents, searching data rooms",
        routes=[
            RouteConfig(
                "_app/data-rooms/index.tsx",
                "/data-rooms",
                "Data Rooms Index",
                "Redirects to first data room",
            ),
            RouteConfig(
                "_app/data-rooms/$id/entries/$.tsx",
                "/data-rooms/:id/entries/:path",
                "Data Room Browser",
                "File/folder table, upload, search",
            ),
        ],
        component_dirs=["data-room", "data-room-search", "data-rooms"],
        layout_notes="""\
- Breadcrumb navigation (clickable path segments)
- Drag-and-drop file upload zone (if writable)
- Toolbar: current path name, folder-up button, "New Folder" button, sync status
- File/folder table: checkbox, name, type, date columns
- Sync status: "Synchronising..." | "Up to date" | "Error"
- Search: `<domain>/data-rooms/:id/entries/:path?query=searchterm`""",
        recipes=[
            RecipeConfig(
                "Browse a data room",
                [
                    'navigate("<domain>/data-rooms")',
                    "wait(slow)  # redirects to first data room",
                    "take_screenshot()",
                    "take_snapshot()  # get file/folder names",
                ],
            ),
            RecipeConfig(
                "Navigate into a folder",
                [
                    "(on data room page)",
                    "take_snapshot()  # find folder names",
                    'click("<folder name>")',
                    "wait(fast)",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Upload a file",
                [
                    "(on data room page — writable room)",
                    "drag files onto the drop zone, or use file selector",
                    "confirm upload in the dialog",
                    "wait(slow)  # upload progress",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Search a data room",
                [
                    "(on data room page)",
                    "click the search input",
                    'type("search query")',
                    'press_key("Enter")',
                    "wait(slow)",
                    "take_snapshot()  # find results",
                ],
            ),
            RecipeConfig(
                "Create a new folder",
                [
                    "(on data room page)",
                    'click("New Folder")',
                    'type("My Folder Name")',
                    'press_key("Enter")',
                ],
            ),
        ],
    ),
    AreaConfig(
        key="DATA_CONNECTIONS",
        title="Data Connections",
        when_to_read="SharePoint/Box OAuth, connect drives, sync folders",
        routes=[
            RouteConfig(
                "_app/data-rooms/new.tsx",
                "/data-rooms/new",
                "New Data Room",
                "Connect SharePoint or Box",
            ),
        ],
        component_dirs=["data-connections"],
        layout_notes="""\
Two connection cards side by side:

**SharePoint/OneDrive:**
- If not linked: "Link Microsoft Account" button (opens OAuth popup)
- If linked: drive list with "Connect"/"Disconnect" per drive
- Search: placeholder `"Search SharePoint sites"`
- Settings: "Show Empty Drives", "Link New Account", "Unlink Account"

**Box:**
- If not linked: "Link Box Account" button (opens OAuth popup)
- If linked: synced folders list with "Disconnect" buttons
- "Sync a new Box folder" button
- Settings: "Link New Account", "Unlink Account"

**Usage indicator:** file count + size progress bars (green/yellow/red)""",
        recipes=[
            RecipeConfig(
                "Connect a SharePoint drive",
                [
                    'navigate("<domain>/data-rooms/new")',
                    "wait(slow)",
                    'click("Link Microsoft Account")  # opens OAuth popup',
                    "(complete OAuth in popup)",
                    "wait(slow)  # drives list loads",
                    "take_snapshot()  # find drive names",
                    'click("Connect")  # next to desired drive',
                    "wait(very_slow)  # sync begins",
                ],
            ),
            RecipeConfig(
                "Sync a Box folder",
                [
                    'navigate("<domain>/data-rooms/new")',
                    "wait(slow)",
                    'click("Sync a new Box folder")',
                    "wait(fast)  # folder picker opens",
                    "select the folder",
                    "wait(very_slow)  # sync begins",
                ],
            ),
        ],
    ),
    AreaConfig(
        key="DATA_SOURCES",
        title="Data Sources",
        when_to_read="External data source search, web research",
        routes=[
            RouteConfig(
                "_app/data-sources/$source.tsx",
                "/data-sources/:source",
                "Data Source Search",
                "Search an external data source",
            ),
        ],
        component_dirs=["data-sources"],
        layout_notes="""\
- Page title: data source name (e.g., "Google Drive", "FRED", "SEC")
- Search bar with submit button
- Results list with pagination ("1 - 10 of 234 results")
- Each result clickable → detail panel with metadata, documents, notes

**Web Research** (`<domain>/data-sources/web-research`):
- Search input: placeholder `"Search web..."`
- Mode dropdown: "Snapshot" (fast) | "Deep Research" (3-5 min)
- Results: markdown content with numbered citation sources
- Each source: domain name, "Add to assistant" button, external link""",
        recipes=[
            RecipeConfig(
                "Search a data source",
                [
                    'navigate("<domain>/data-sources/<source-slug>")',
                    "wait(fast)",
                    "click the search input",
                    'type("search query")',
                    'press_key("Enter")',
                    "wait(slow)  # results load",
                    "take_snapshot()  # find result titles",
                ],
            ),
            RecipeConfig(
                "Web research",
                [
                    'navigate("<domain>/data-sources/web-research")',
                    'click the search input (placeholder "Search web...")',
                    'type("your research question")',
                    'press_key("Enter")',
                    "wait(very_slow)  # research takes time",
                    "take_screenshot()",
                ],
            ),
        ],
    ),
    AreaConfig(
        key="HOME",
        title="Home / Dashboard",
        when_to_read="Dashboard, tool cards, prompt suggestions, search",
        routes=[
            RouteConfig(
                "_app/home.tsx",
                "/home",
                "Home",
                "Welcome screen, tool cards, search, tag filters",
            ),
        ],
        component_dirs=["home"],
        layout_notes="""\
- Welcome heading: "Welcome back, {name}" or "Welcome"
- Subtitle: "Agentic AI for Real Estate"
- Search input (auto-focused): placeholder `"Search..."`
- Tag filter pills: "All" (selected) + dynamic tag buttons
- Tool cards grid (filtered by search + selected tag)
- Each card: icon/emoji, tool name, description (clickable)""",
        recipes=[
            RecipeConfig(
                "Search and launch a tool",
                [
                    'navigate("<domain>/home")',
                    "wait(fast)  # cards load",
                    'type("lease")  # search is auto-focused',
                    "wait(fast)  # cards filter",
                    "take_snapshot()  # find matching tools",
                    'click("<tool name>")',
                ],
            ),
            RecipeConfig(
                "Filter by tag",
                [
                    'navigate("<domain>/home")',
                    "wait(fast)",
                    'click("<tag name>")  # e.g., a category tag',
                    "take_snapshot()  # see filtered tools",
                ],
            ),
        ],
    ),
    AreaConfig(
        key="TOOLKIT",
        title="Toolkit",
        when_to_read="Workflow launcher, team selector, recent executions",
        routes=[
            RouteConfig(
                "_app/toolkit.tsx",
                "/toolkit",
                "Toolkit",
                "Team workflows with Launch Now cards",
            ),
        ],
        component_dirs=["toolkit"],
        layout_notes="""\
- Welcome heading: "Welcome back, {name}"
- Subtitle: "Agentic AI for Real Estate."
- Team selector dropdown (underlined link)
- Workflow cards grid:
  - Each: icon, name, "CUSTOM WORKFLOW" badge, description
  - "Recently Used" orange badge (if applicable)
  - Usage stats: "Used X times this month", "~Y min"
  - "Launch Now" button (blue/primary with play icon)
- Last card: "Ask {assistantName}" with "Start a Conversation" button""",
        recipes=[
            RecipeConfig(
                "Launch a workflow",
                [
                    'navigate("<domain>/toolkit")',
                    "wait(slow)  # cards load",
                    "take_snapshot()  # find workflow names",
                    'click("Launch Now")  # on the desired card',
                    "wait(slow)  # thread created, redirected",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Switch team",
                [
                    'navigate("<domain>/toolkit")',
                    "click the team name link (underlined text near subtitle)",
                    'click("<team name>")  # select from dropdown',
                    "wait(fast)  # cards reload",
                ],
            ),
            RecipeConfig(
                "Start a freeform conversation",
                [
                    'navigate("<domain>/toolkit")',
                    'scroll to the "Ask {assistantName}" card',
                    'click("Start a Conversation")',
                    "wait(slow)  # new thread opens",
                ],
            ),
        ],
    ),
    AreaConfig(
        key="SIDEBAR",
        title="Sidebar",
        when_to_read="Navigation sidebar, switching pages, sign out",
        routes=[],
        component_dirs=["app-sidebar"],
        layout_notes="""\
The sidebar is visible on ALL authenticated pages (left side).

**Sections (top to bottom):**
1. Header: "Fifth Dimension" logo + text
2. Main nav: "Home" (house icon), "Toolkit" (package icon)
3. Skills: "Skills" (layers icon) — has orange "New" badge
4. Threads: collapsible, shows recent thread list (each clickable)
5. Data Rooms: collapsible, lists data rooms
6. Data Sources: expandable groups with sub-items
7. Footer: "Contact Support" link, user profile dropdown

**States:** Expanded (full labels) | Collapsed (icons only, toggle via hamburger)

**User dropdown (click avatar at bottom):** avatar, full name, org name, "Sign out\"""",
        recipes=[
            RecipeConfig(
                "Navigate via sidebar",
                [
                    "take_snapshot()  # find sidebar items",
                    'click("Home")  # or "Toolkit", "Skills", etc.',
                    "wait(fast)",
                    "take_screenshot()",
                ],
            ),
            RecipeConfig(
                "Open a thread from sidebar",
                [
                    "take_snapshot()  # find thread subjects in sidebar",
                    'click("<thread subject>")',
                    "wait(slow)",
                ],
            ),
            RecipeConfig(
                "Collapse/expand sidebar",
                [
                    "click the sidebar trigger (hamburger icon in header)",
                ],
            ),
            RecipeConfig(
                "Sign out",
                [
                    "click the user avatar at bottom of sidebar",
                    'click("Sign out")',
                ],
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# SKILL.md updater
# ---------------------------------------------------------------------------

SITE_MAP_START = "<!-- AUTO:SITE_MAP_START -->"
SITE_MAP_END = "<!-- AUTO:SITE_MAP_END -->"
AREA_TABLE_START = "<!-- AUTO:AREA_TABLE_START -->"
AREA_TABLE_END = "<!-- AUTO:AREA_TABLE_END -->"


def _generate_site_map() -> str:
    """Generate the site map tables for SKILL.md."""
    lines: list[str] = []

    # Public pages
    public_routes = [r for a in AREAS for r in a.routes if r.public]
    if public_routes:
        lines.append("### Public pages (no auth required)\n")
        lines.append("| URL | Page | Description |")
        lines.append("|-----|------|-------------|")
        for r in public_routes:
            lines.append(f"| `{r.url_path}` | {r.label} | {r.description} |")
        lines.append("")

    # Authenticated pages
    auth_routes = [r for a in AREAS for r in a.routes if not r.public]
    if auth_routes:
        lines.append("### Authenticated pages (redirect to /sign-in if not logged in)\n")
        lines.append("| URL | Page | Description |")
        lines.append("|-----|------|-------------|")
        for r in auth_routes:
            lines.append(f"| `{r.url_path}` | {r.label} | {r.description} |")
        lines.append("")

    # Global layout
    lines.append("### Global layout (present on all authenticated pages)\n")
    lines.append("- **Left sidebar**: collapsible — Home, Toolkit, Skills, Threads, Data Rooms, Data Sources")
    lines.append('- **Header bar**: sidebar toggle (hamburger), "Ask Ellie" button (top-right)')
    lines.append('- **User dropdown**: bottom of sidebar — avatar, name, org, "Sign out"')
    lines.append('- **Support**: "Contact Support" link in sidebar footer')

    return "\n".join(lines)


def _generate_area_table() -> str:
    """Generate the area files table for SKILL.md."""
    lines: list[str] = []
    lines.append("| File | When to read |")
    lines.append("|------|-------------|")
    for area in AREAS:
        lines.append(
            f"| [`{area.key}.md`](./pages/{area.key}.md) | {area.when_to_read} |"
        )
    return "\n".join(lines)


def update_skill_md(skill_md_path: Path) -> None:
    """Update auto-generated sections in SKILL.md."""
    text = read_text(skill_md_path)
    if not text:
        print(f"  WARNING: SKILL.md not found at {skill_md_path}")
        return

    # Update site map
    if SITE_MAP_START in text and SITE_MAP_END in text:
        before = text[: text.index(SITE_MAP_START) + len(SITE_MAP_START)]
        after = text[text.index(SITE_MAP_END) :]
        text = before + "\n\n" + _generate_site_map() + "\n\n" + after

    # Update area table
    if AREA_TABLE_START in text and AREA_TABLE_END in text:
        before = text[: text.index(AREA_TABLE_START) + len(AREA_TABLE_START)]
        after = text[text.index(AREA_TABLE_END) :]
        text = before + "\n\n" + _generate_area_table() + "\n\n" + after

    skill_md_path.write_text(text, encoding="utf-8")
    print(f"  updated {skill_md_path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate fe-nav browser navigation files")
    parser.add_argument(
        "--src",
        required=True,
        help="Path to access-ui/src directory",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output directory for pages/*.md (default: pages/ next to this script's parent)",
    )
    args = parser.parse_args()

    src = Path(args.src).resolve()
    if not src.exists():
        print(f"ERROR: Source directory not found: {src}")
        raise SystemExit(1)

    # Default output: pages/ directory next to scripts/
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent  # skills/fe-nav/
    out_dir = Path(args.out).resolve() if args.out else skill_dir / "pages"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Source: {src}")
    print(f"Output: {out_dir}")
    print()

    for area in AREAS:
        # Scan component directories
        scans = [scan_component_dir(src, d) for d in area.component_dirs]
        scan = merge_scan_data(*scans) if scans else ScanData()

        # Render and write
        content = render_area(area, scan)
        path = out_dir / f"{area.key}.md"
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {path.name}")

    # Update SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        update_skill_md(skill_md)
    else:
        print(f"  SKILL.md not found at {skill_md}, skipping update")

    print(f"\nDone. {len(AREAS)} area files written to {out_dir}/")


if __name__ == "__main__":
    main()
