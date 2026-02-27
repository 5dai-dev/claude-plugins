# Regenerating Navigation Files

The `pages/*.md` files and the site map in `SKILL.md` are generated from the access-ui source code.

## Script location

```
skills/fe-nav/scripts/generate.py
```

## Usage

```bash
python scripts/generate.py --src <path-to-access-ui/src>
```

Example from the skill directory:

```bash
cd skills/fe-nav
python scripts/generate.py --src ~/workspace/m5/application/access-ui/src
```

By default, output goes to `pages/` and `SKILL.md` is updated in place (next to the script's parent). Override with `--out`:

```bash
python scripts/generate.py --src ~/workspace/m5/application/access-ui/src --out ./pages
```

## What it does

1. Scans route files and component directories under `src/`
2. Extracts UI elements: button labels, input placeholders, dialog titles, dropdown items, tab labels, aria labels
3. Generates one `pages/<AREA>.md` file per area
4. Updates the site map and area file table in `SKILL.md` (between `<!-- AUTO:` markers)

## How to add a new area

Add an `AreaConfig` entry to the `AREAS` list in `generate.py`:

```python
AreaConfig(
    key="MY_AREA",
    title="My Area",
    when_to_read="When to read this file",
    routes=[
        RouteConfig("_app/my-page.tsx", "/my-page", "My Page", "What this page does"),
    ],
    component_dirs=["my-component-dir"],
    layout_notes="- Key layout detail 1\n- Key layout detail 2",
    recipes=[
        RecipeConfig("Do something", [
            'navigate("<domain>/my-page")',
            'wait(slow)',
            'take_screenshot()',
        ]),
    ],
)
```

## What is auto vs manual

| Content | Source |
|---------|--------|
| UI element lists (buttons, inputs, dialogs, etc.) | **Auto** — extracted from component source code |
| Simple recipes (navigate-to, search) | **Auto** — generated from route and placeholder data |
| Layout notes | **Manual** — written in `AreaConfig.layout_notes` |
| Complex recipes (multi-step workflows) | **Manual** — written in `AreaConfig.recipes` |
| Site map tables in SKILL.md | **Auto** — generated from all area configs |
