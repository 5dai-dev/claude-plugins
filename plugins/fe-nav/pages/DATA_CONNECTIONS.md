# Data Connections — Browser Navigation

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/data-rooms/new` | New Data Room | Connect SharePoint or Box |

## What you see

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

**Usage indicator:** file count + size progress bars (green/yellow/red)

## UI Elements

**Buttons**: `"Sync a new Box folder"`, `"OK"`, `"Settings"`
**Inputs**: `"Search SharePoint sites"`
**Dialogs**: `"Sync Folder from Box"`, `"Link New Account"`, `"Unlink Account"`, `"Disconnect folder"`, `"Sync drive from SharePoint/OneDrive"`, `"Disconnect drive"`

## Recipes

### Recipe: Navigate to New Data Room

```
1. navigate("<domain>/data-rooms/new")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Search

```
1. click the search input (placeholder "Search SharePoint sites")
2. type("your search query")
3. press_key("Enter")
4. wait(slow)
5. take_snapshot()
```

### Recipe: Connect a SharePoint drive

```
1. navigate("<domain>/data-rooms/new")
2. wait(slow)
3. click("Link Microsoft Account")  # opens OAuth popup
4. (complete OAuth in popup)
5. wait(slow)  # drives list loads
6. take_snapshot()  # find drive names
7. click("Connect")  # next to desired drive
8. wait(very_slow)  # sync begins
```

### Recipe: Sync a Box folder

```
1. navigate("<domain>/data-rooms/new")
2. wait(slow)
3. click("Sync a new Box folder")
4. wait(fast)  # folder picker opens
5. select the folder
6. wait(very_slow)  # sync begins
```
