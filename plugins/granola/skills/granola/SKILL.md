---
name: granola
description: >
  This skill should be used when the user wants to interact with Granola AI meeting notes.
  Triggers: accessing meeting transcripts, searching meeting notes, listing Granola folders,
  chatting with meeting documents, getting transcript quotes, exploring Granola workspaces,
  or any reference to "granola" in the context of meetings or notes.
---

# Granola Meeting Notes Skill

Interact with the user's Granola AI meeting notes — browse folders, read transcripts, and ask questions about meetings using Granola's AI chat.

## Authentication

Authentication is automatic. The skill reads credentials from the local Granola desktop app at `~/Library/Application Support/Granola/supabase.json`. The user must have the Granola app installed and be signed in. Tokens are auto-refreshed when expired.

If auth fails, tell the user to open the Granola app and sign in.

## Available Commands

The helper script is at `scripts/granola.py` relative to this skill's directory.

To find the script path, locate this SKILL.md file and resolve `scripts/granola.py` next to it. For example:
```
SKILL_DIR="$(dirname "$(find ~/.claude -path '*/skills/granola/SKILL.md' -print -quit 2>/dev/null)")"
GRANOLA="$SKILL_DIR/scripts/granola.py"
```

In all examples below, `GRANOLA` refers to the resolved script path.

### Test Authentication
```bash
python3 $GRANOLA auth
```
Shows current user email, workspaces, and confirms auth is working.

### List Workspaces
```bash
python3 $GRANOLA workspaces
```

### List All Folders
```bash
python3 $GRANOLA folders
```
Returns JSON array of folders with `id`, `name`, `document_count`, `is_favourite`.

### List Documents in a Folder
```bash
python3 $GRANOLA docs <folder_id>
```
Returns JSON with folder name and array of documents with `id`, `title`, `created_at`.

### List Recent Documents
```bash
python3 $GRANOLA recent [limit]
```
Lists the most recent documents (default 20).

### Get Full Transcript
```bash
python3 $GRANOLA transcript <document_id>
```
Returns the full meeting transcript with speaker names and timestamps in markdown format.

### Chat with a Single Document
```bash
python3 $GRANOLA chat "your question here" --doc <document_id>
```
Asks Granola's AI a question about a specific meeting. Returns the AI-generated response with transcript quotes.

### Chat with an Entire Folder
```bash
python3 $GRANOLA chat "your question here" --folder <folder_id>
```
Asks Granola's AI a question across all documents in a folder.

## Workflow Patterns

### Browse and explore
1. Run `folders` to see all available folders
2. Run `docs <folder_id>` to see meetings in a folder
3. Run `transcript <doc_id>` for the full raw transcript
4. Run `chat "question" --doc <doc_id>` to ask about a specific meeting

### Extract information across meetings
1. Run `folders` to find the target folder
2. Run `chat "question" --folder <folder_id>` to query across all meetings in the folder

### Save transcripts or chat results to files
After getting results, use the Write tool to save output to the user's desired location. When saving multiple transcripts, name files with the date prefix from `created_at` followed by the sanitized title (e.g., `2025-09-24_Meeting_Title.md`).

## Notes
- The chat API uses Granola's server-side AI which has access to full transcript context even when transcripts aren't sent in the request payload.
- Folder-level chat passes all document IDs in the folder to the chat API.
- Transcripts include speaker attribution and timestamps.
- The Granola web UI for any document is at: `https://notes.granola.ai/d/<document_id>`
- The Granola web UI for any folder is at: `https://notes.granola.ai/f/<folder_id>`
