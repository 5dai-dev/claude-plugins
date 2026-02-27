# Data Rooms — Browser Navigation

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/data-rooms` | Data Rooms Index | Redirects to first data room |
| `<domain>/data-rooms/:id/entries/:path` | Data Room Browser | File/folder table, upload, search |

## What you see

- Search bar at top: placeholder `"Search Data Room..."`
- Breadcrumb navigation (clickable path segments, e.g., "Home")
- Drag-and-drop file upload zone: "Upload documents" / "Drag & drop or click to browse"
  - Privacy notice (varies by room type):
    - Private rooms: "Documents will only be visible to you"
    - Shared rooms: "Documents will be immediately visible to all team members"
- Toolbar: path name heading, item count (e.g., "0 ITEM(S)"), "New Folder" button
- File/folder table with sortable columns: checkbox, NAME, SIZE, STATUS, LAST MODIFIED
- Footer bar: "X DOCUMENTS(S) SELECTED."
- Empty state: "Empty folder"
- Search: `<domain>/data-rooms/:id/entries/:path?query=searchterm`

## UI Elements

**Buttons**: `"Create"`, `"Cancel"`, `"Upload {files.length} File{files.length !== 1 ? "s" : ""}"`
**Inputs**: `"Enter your folder’s name"`, `"Search Data Room..."`
**Dialogs**: `"Stop uploading?"`
**Aria labels**: `"Select row"`

## Recipes

### Recipe: Navigate to Data Rooms Index

```
1. navigate("<domain>/data-rooms")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Navigate to Data Room Browser

```
1. navigate("<domain>/data-rooms/:id/entries/:path")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Search

```
1. click the search input (placeholder "Search Data Room...")
2. type("your search query")
3. press_key("Enter")
4. wait(slow)
5. take_snapshot()
```

### Recipe: Browse a data room

```
1. navigate("<domain>/data-rooms")
2. wait(slow)  # redirects to first data room
3. take_screenshot()
4. take_snapshot()  # get file/folder names
```

### Recipe: Navigate into a folder

```
1. (on data room page)
2. take_snapshot()  # find folder names
3. click("<folder name>")
4. wait(fast)
5. take_screenshot()
```

### Recipe: Upload a file

```
1. (on data room page — writable room)
2. drag files onto the drop zone, or use file selector
3. confirm upload in the dialog
4. wait(slow)  # upload progress
5. take_screenshot()
```

### Recipe: Search a data room

```
1. (on data room page)
2. click the search input
3. type("search query")
4. press_key("Enter")
5. wait(slow)
6. take_snapshot()  # find results
```

### Recipe: Create a new folder

```
1. (on data room page)
2. click("New Folder")
3. type("My Folder Name")
4. press_key("Enter")
```
