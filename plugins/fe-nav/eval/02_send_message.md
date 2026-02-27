# Eval: Send a Message in a Thread

## Goal

Open an existing thread, send a message, and verify the AI response appears.

## Context files to read

- SKILL.md (for domain, timing, tools reference)
- pages/THREADS.md (for thread recipes and UI elements)

## Preconditions

- Logged in (auth token in browser)
- At least one existing thread in the Threads list

## Steps

1. Follow "Navigate to Threads List" recipe from THREADS.md
2. Take snapshot — identify the first thread subject in the list
3. Click the first thread card (use subject text from snapshot)
4. Wait(slow) — thread detail loads
5. Take screenshot — verify chat messages visible

6. Follow "Send a message in existing thread" recipe:
   - Click the textarea (placeholder "Type your message...")
   - Type "Hello, this is an eval test message"
   - Click "Send"
   - Wait(very_slow) — AI response

7. Take screenshot — verify the sent message and AI response

## Pass criteria

- Thread list page loaded (snapshot shows thread cards)
- Thread detail page loaded (screenshot shows chat messages)
- Message was sent (visible in chat as a user message bubble)
- AI response appeared (new assistant message bubble after the sent message)
