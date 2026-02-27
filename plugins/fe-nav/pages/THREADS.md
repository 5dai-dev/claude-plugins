# Threads — Browser Navigation

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/workspace/threads` | Threads List | All conversation threads with read/unread tabs |
| `<domain>/workspace/thread/new` | New Thread | Start a new conversation |
| `<domain>/workspace/thread/:id` | Thread Detail | Chat messages, document sidebar, preview panel |

## What you see

**Threads List:**
- Header "Threads" with "All" | "Unread" tabs (orange badge count)
- Scrollable list of thread cards: icon, subject, status badge, preview, timestamp
- Each card is clickable (navigates to thread detail)

**Thread Detail (3-panel):**
- Left/center: Chat column with message history + input area
- Right sidebar: Documents panel (Attached, Generated, References sections)
- Far right: Document preview panel (opens on demand)
- Chat input: textarea with paperclip (attach), `"My Prompts"` button
- Bottom-right: `"Agent Mode"` toggle switch (ON by default for new threads)
- Submit: `"Send"` button with dropdown chevron for "Send in Chat" / "Send via Email"
- While processing: "Processing..." button, then "Stop" to cancel

## UI Elements

**Buttons**: `"Try again"`, `"Almost ready..."`, `"Error!"`, `"Cancel"`, `"Attach Documents"`, `"Start a New Thread"`, `"Clear all"`
**Inputs**: `"user@example.com"`, `"Enter subject..."`, `"Tell us more about your experience..."`
**Dialogs**: `"Save to Data Room"`, `"Collapse panel"`, `"Download all files as zip"`, `"Set save location"`, `"Show documents"`, `"Your request has been received"`, `"Documents"`, `"No attachments"`, `"Close preview"`, `"Generated Documents"`, `"References"`, `"Send a copy"`, `"Delete Thread"`, `"Rename Thread"`, `"Rate this response"`, `"No additional feedback"`, `"More actions"`
**Tabs**: `"All"`
**Aria labels**: `"Collapse panel"`, `"Download all attached files as zip"`, `"Download all generated files as zip"`, `"Set save location"`, `"Download all reference files as zip"`, `"Show documents"`, `"Close preview"`, `"Upload files"`, `"Thread settings"`

## Recipes

### Recipe: Navigate to Threads List

```
1. navigate("<domain>/workspace/threads")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Navigate to New Thread

```
1. navigate("<domain>/workspace/thread/new")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Navigate to Thread Detail

```
1. navigate("<domain>/workspace/thread/:id")
2. wait(slow)
3. take_screenshot()
```

### Recipe: Send a message in existing thread

```
1. navigate("<domain>/workspace/thread/<threadId>")
2. wait(slow)  # messages load
3. click the textarea (placeholder "Type your message...")
4. type("Your message here")
5. click("Send")
6. wait(very_slow)  # AI response
7. take_screenshot()
```

### Recipe: Start a new thread

```
1. navigate("<domain>/workspace/thread/new")
2. wait(fast)
3. click the subject input (placeholder "Enter subject...")
4. type("My new thread subject")
5. click the textarea (placeholder "Start your conversation...")
6. type("Hello, I have a question about...")
7. click("Send")
8. wait(very_slow)  # AI response
9. take_screenshot()
```

### Recipe: Attach a document from data room

```
1. (on thread detail page)
2. click the paperclip icon (attach button, bottom-left of input)
3. wait(fast)  # attachment sheet opens
4. click the data room name in left sidebar of sheet
5. wait(fast)  # file list loads
6. click the checkbox next to desired file(s)
7. press_key("Escape")  # close sheet
```

### Recipe: Rename a thread

```
1. (on thread detail page)
2. click the gear icon (aria-label "Thread settings")
3. click("Rename Thread")
4. type("New thread name")
5. press_key("Enter")
```

### Recipe: Delete a thread

```
1. (on thread detail page)
2. click the gear icon (aria-label "Thread settings")
3. click("Delete Thread")
4. click the confirm button in the dialog
```
