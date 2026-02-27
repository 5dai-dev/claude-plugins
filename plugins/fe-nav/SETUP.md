# Chrome MCP Setup

Prerequisites for using the fe-nav skill to automate the access-ui browser.

## 1. Install Chrome extension

Install the **Claude Code Chrome Connector** (v1.0.36+) from the Chrome Web Store.

This extension bridges Claude Code and your Chrome browser, allowing MCP tools to control the page.

## 2. Enable in Claude Code

Run the `/chrome` command in Claude Code to activate the Chrome MCP connection.

## 3. Verify

```
take_screenshot()
```

If you see a screenshot of your current Chrome tab, the connection is working.

## 4. Gmail MCP (for login automation)

The automated login flow requires **Gmail MCP** (`claude.ai Gmail`) to read
OTP emails sent during sign-in.

**Setup:**
1. Gmail MCP is available as a built-in Claude Code integration — no install needed.
2. The connected Gmail account must match the email used to sign in (e.g., `douglas.hindson@fifthdimensionai.com`).
3. On first use, you may be prompted to authorize Gmail access.

**Verify:**
```
gmail_get_profile()
```

If you see your email address and mailbox stats, Gmail MCP is working.

**Without Gmail MCP:** You can still use the manual sign-in recipe in
[AUTH.md](./pages/AUTH.md) — you'll need to manually retrieve the OTP link
from your email and provide it to the agent.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Extension not found" | Open Chrome, verify the extension is installed and enabled |
| "Chrome not running" | Launch Chrome before running `/chrome` |
| Screenshot is blank or wrong tab | Click the desired Chrome tab to focus it, then retry |
| "Connection refused" | Restart Chrome, re-enable the extension, run `/chrome` again |
| Tools hang or timeout | Close other DevTools panels — only one debugger can attach at a time |
| Gmail search returns no results | Check the connected Gmail account matches the login email |

## Notes

- Chrome must be running with the extension active before you start.
- The MCP connection targets the **active tab**. Switch tabs in Chrome to change the target.
- If Chrome crashes or the tab navigates away unexpectedly, run `/chrome` again to reconnect.
