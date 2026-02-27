# Auth — Browser Navigation

## Prerequisites

- **Chrome MCP**: See [SETUP.md](../SETUP.md) for browser automation setup.
- **Gmail MCP**: Required for the automated login flow. The Gmail MCP server
  (`claude.ai Gmail`) must be connected so the agent can read OTP emails.
  The connected Gmail account must match the login email.

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `<domain>/sign-in` | Sign In | Email input, magic link sent |
| `<domain>/auth?token=...` | Token Verify | Validates magic link token |
| `<domain>/otp?token=...` | OTP Exchange | "Confirm Your Sign In" + "Complete Sign In" button |
| `<domain>/sso-callback` | SSO Callback | Handles SAML SSO response |

## What you see

### Sign In page (`/sign-in`)
- Centered card: "Sign in to Fifth Dimension"
- Email input (auto-focused), placeholder `"you@example.com"`
- "Sign In" button (full width, black, shows `"Checking your details..."` + spinner while loading)
- If email is `@fifthdimensionai.com`: a "Customer ID" field appears (placeholder `"Enter Customer ID"`)
- Error state: `"Something went wrong. Try again."` (red, below button)

### Check your email screen (after submit)
- "Check your email" heading
- "We've sent a magic link."
- "To continue, click the link sent to **{email}**"
- "Not seeing the email in your inbox? Try sending again"

### OTP page (`/otp?token=...`)
- "Confirm Your Sign In" heading
- "Click the button below to complete your sign in."
- "Complete Sign In" button (full width, black)

## UI Elements

**Buttons**: `"Sign In"`, `"Complete Sign In"`, `"Try sending again"`
**Inputs**: `"you@example.com"`, `"Enter Customer ID"`

## Customer ID

The Customer ID field only appears for `@fifthdimensionai.com` email addresses.
It selects which customer tenant to log into. Leave it blank for the default
tenant. Common values:

| Customer ID | Tenant |
|-------------|--------|
| *(blank)* | Default (5DAI internal) |
| `MadisonInt` | Madison International Realty |

## Recipes

### Recipe: Full automated sign-in (with Gmail MCP)

This is the primary login recipe. It uses Chrome MCP to fill the sign-in form
and Gmail MCP to retrieve the OTP token from email.

```
1. navigate("<domain>/sign-in")
2. wait(slow)
3. find the email input (placeholder "you@example.com")
4. form_input(ref, "<your-email>")  # use form_input, not type — input may detach
5. # If @fifthdimensionai.com and a specific customer is needed:
   #   click the Customer ID input (placeholder "Enter Customer ID")
   #   type("<customer-id>")
6. click("Sign In")
7. wait(slow)                              # "Check your email" screen appears
8. take_screenshot()                       # verify confirmation screen
9. # Use Gmail MCP to find the OTP email:
   gmail_search_messages(q='from:fifthdimensionai.com subject:"Secure link to sign in to Fifth Dimension" newer_than:1d', maxResults=1)
10. gmail_read_message(messageId=<id from step 9>)
11. # Extract the OTP URL from the email body — look for: <domain>/otp?token=<hex>
12. navigate("<otp-url-from-email>")       # e.g., <domain>/otp?token=797f58e1...
13. wait(slow)
14. click("Complete Sign In")
15. wait(slow)                             # redirects to authenticated app
16. take_screenshot()                      # verify logged in (threads list or home)
```

### Recipe: Sign in (manual — no Gmail MCP)

```
1. navigate("<domain>/sign-in")
2. click the email input (placeholder "you@example.com")
3. type("<your-email>")
4. click("Sign In")
5. wait(slow)                              # "Check your email" screen
6. take_screenshot()
7. # Ask the user to check their email and provide the OTP URL
```

### Recipe: Sign out

```
1. click the user profile at bottom-left of sidebar
2. click("Sign out")
```
