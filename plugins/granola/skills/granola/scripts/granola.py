#!/usr/bin/env python3
"""Granola AI meeting notes CLI helper.

Usage:
    python3 granola.py auth              # Test auth / show current user
    python3 granola.py workspaces        # List workspaces
    python3 granola.py folders           # List all folders
    python3 granola.py docs <folder_id>  # List documents in a folder
    python3 granola.py transcript <doc_id>              # Get raw transcript
    python3 granola.py chat <prompt> --doc <doc_id>     # Chat with one doc
    python3 granola.py chat <prompt> --folder <fid>     # Chat with all docs in folder
    python3 granola.py recent [limit]                   # List recent documents
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


CRED_PATH = Path.home() / "Library" / "Application Support" / "Granola" / "supabase.json"
API_BASE = "https://api.granola.ai"
STREAM_BASE = "https://stream.api.granola.ai"
WORKOS_AUTH_URL = "https://api.workos.com/user_management/authenticate"


def load_credentials() -> dict[str, str]:
    """Load and return access_token, refresh_token, workspace_id from local Granola app storage."""
    if not CRED_PATH.exists():
        print(f"ERROR: Granola credentials not found at {CRED_PATH}", file=sys.stderr)
        print("Make sure the Granola desktop app is installed and you are signed in.", file=sys.stderr)
        sys.exit(1)

    with open(CRED_PATH) as f:
        data = json.load(f)

    tokens = json.loads(data["workos_tokens"])
    access_token = tokens["access_token"]
    obtained_at = tokens.get("obtained_at", 0)
    expires_in = tokens.get("expires_in", 3600)

    # Check if token is expired (obtained_at is in ms)
    now_ms = int(time.time() * 1000)
    expires_at_ms = obtained_at + (expires_in * 1000)
    if now_ms > expires_at_ms:
        print("Access token expired. Attempting refresh...", file=sys.stderr)
        access_token = refresh_access_token(tokens)

    return {"access_token": access_token}


def refresh_access_token(tokens: dict) -> str:
    """Refresh the access token using the refresh token via WorkOS."""
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        print("ERROR: No refresh token available. Please sign in to the Granola app.", file=sys.stderr)
        sys.exit(1)

    # We need the client_id from the JWT issuer
    # Extract from current access token JWT payload
    import base64
    payload_b64 = tokens["access_token"].split(".")[1]
    payload_b64 += "=" * (4 - len(payload_b64) % 4)
    jwt_payload = json.loads(base64.urlsafe_b64decode(payload_b64))
    # issuer format: https://auth.granola.ai/user_management/<client_id>
    client_id = jwt_payload["iss"].split("/")[-1]

    result = subprocess.run([
        "curl", "-s",
        WORKOS_AUTH_URL,
        "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }),
    ], capture_output=True, text=True, timeout=15)

    resp = json.loads(result.stdout)
    if "access_token" not in resp:
        print(f"ERROR: Token refresh failed: {resp}", file=sys.stderr)
        sys.exit(1)

    # Update the stored credentials (refresh tokens are single-use)
    new_tokens = {**tokens}
    new_tokens["access_token"] = resp["access_token"]
    new_tokens["refresh_token"] = resp["refresh_token"]
    new_tokens["expires_in"] = resp.get("expires_in", 3600)
    new_tokens["obtained_at"] = int(time.time() * 1000)

    with open(CRED_PATH) as f:
        cred_data = json.load(f)
    cred_data["workos_tokens"] = json.dumps(new_tokens)
    with open(CRED_PATH, "w") as f:
        json.dump(cred_data, f)

    print("Token refreshed successfully.", file=sys.stderr)
    return resp["access_token"]


def get_workspace_id(creds: dict[str, str]) -> str:
    """Get the first workspace ID."""
    resp = api_post(creds, "/v1/get-workspaces", {})
    workspaces = resp.get("workspaces", [])
    if not workspaces:
        print("ERROR: No workspaces found.", file=sys.stderr)
        sys.exit(1)
    return workspaces[0]["workspace"]["workspace_id"]


def api_post(creds: dict[str, str], path: str, body: dict, base: str = API_BASE) -> dict:
    """Make an authenticated POST request to the Granola API."""
    result = subprocess.run([
        "curl", "-s", "--compressed",
        f"{base}{path}",
        "-X", "POST",
        "-H", f"authorization: Bearer {creds['access_token']}",
        "-H", "content-type: application/json",
        "-H", "accept: */*",
        "-H", "origin: https://notes.granola.ai",
        "-H", "x-client-version: 0.0.0.web",
        "-H", f"x-granola-workspace-id: {creds.get('workspace_id', '')}",
        "-d", json.dumps(body),
    ], capture_output=True, text=True, timeout=30)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"ERROR: Failed to parse API response from {path}", file=sys.stderr)
        print(f"Raw: {result.stdout[:500]}", file=sys.stderr)
        sys.exit(1)


def api_stream(creds: dict[str, str], path: str, body: dict) -> str:
    """Make a streaming POST request and return the final accumulated text."""
    result = subprocess.run([
        "curl", "-s", "--compressed",
        f"{STREAM_BASE}{path}",
        "-H", f"authorization: Bearer {creds['access_token']}",
        "-H", "content-type: application/json",
        "-H", "accept: */*",
        "-H", "origin: https://notes.granola.ai",
        "-H", "x-client-version: 0.0.0.web",
        "-H", f"x-granola-workspace-id: {creds.get('workspace_id', '')}",
        "--data-raw", json.dumps(body),
    ], capture_output=True, text=True, timeout=120)

    raw = result.stdout
    chunks = raw.split("-----CHUNK_BOUNDARY-----")
    for chunk in reversed(chunks):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            parsed = json.loads(chunk)
            for out in parsed.get("outputs", []):
                if out.get("type") == "text" and out.get("text"):
                    return out["text"]
        except json.JSONDecodeError:
            continue
    return ""


# ── Commands ──────────────────────────────────────────────────────────────────


def cmd_auth(creds: dict[str, str]) -> None:
    """Test authentication and show current user info."""
    with open(CRED_PATH) as f:
        data = json.load(f)
    user_info = json.loads(data["user_info"])

    ws = api_post(creds, "/v1/get-workspaces", {})
    workspaces = ws.get("workspaces", [])

    print(json.dumps({
        "status": "authenticated",
        "email": user_info.get("email"),
        "user_id": user_info.get("id"),
        "workspaces": [
            {
                "id": w["workspace"]["workspace_id"],
                "name": w["workspace"]["display_name"],
                "slug": w["workspace"]["slug"],
                "role": w["role"],
                "plan": w["plan_type"],
            }
            for w in workspaces
        ],
    }, indent=2))


def cmd_workspaces(creds: dict[str, str]) -> None:
    """List all workspaces."""
    ws = api_post(creds, "/v1/get-workspaces", {})
    for w in ws.get("workspaces", []):
        info = w["workspace"]
        print(f'{info["workspace_id"]}: {info["display_name"]} ({info["slug"]}) [{w["plan_type"]}]')


def cmd_folders(creds: dict[str, str]) -> None:
    """List all folders with document counts."""
    resp = api_post(creds, "/v2/get-document-lists", {})

    if isinstance(resp, list):
        folders = resp
    elif isinstance(resp, dict):
        folders = resp.get("document_lists", resp.get("lists", []))
    else:
        folders = []

    output = []
    for folder in folders:
        fid = folder.get("id", "")
        name = folder.get("name", folder.get("title", "untitled"))
        doc_ids = folder.get("document_ids", folder.get("documents", []))
        doc_count = len(doc_ids)
        is_fav = folder.get("is_favourite", False)
        output.append({
            "id": fid,
            "name": name,
            "document_count": doc_count,
            "is_favourite": is_fav,
        })

    print(json.dumps(output, indent=2))


def cmd_docs(creds: dict[str, str], folder_id: str) -> None:
    """List documents in a folder."""
    # Get folder to find document IDs
    resp = api_post(creds, "/v2/get-document-lists", {})
    folders = resp if isinstance(resp, list) else resp.get("document_lists", resp.get("lists", []))

    doc_ids: list[str] = []
    folder_name = ""
    for folder in folders:
        if folder.get("id") == folder_id:
            folder_name = folder.get("name", folder.get("title", ""))
            raw_ids = folder.get("document_ids", folder.get("documents", []))
            doc_ids = [d if isinstance(d, str) else d.get("id", "") for d in raw_ids]
            break

    if not doc_ids:
        print(f"ERROR: Folder {folder_id} not found or empty.", file=sys.stderr)
        sys.exit(1)

    # Get document details
    batch = api_post(creds, "/v1/get-documents-batch", {
        "document_ids": doc_ids,
        "include_last_viewed_panel": False,
    })
    docs = batch.get("documents", batch.get("docs", batch if isinstance(batch, list) else []))

    output = {"folder": folder_name, "folder_id": folder_id, "documents": []}
    for doc in docs:
        output["documents"].append({
            "id": doc.get("id"),
            "title": doc.get("title", "untitled"),
            "created_at": doc.get("created_at", ""),
            "updated_at": doc.get("updated_at", ""),
        })

    # Sort by created_at
    output["documents"].sort(key=lambda d: d.get("created_at", ""))
    print(json.dumps(output, indent=2))


def cmd_recent(creds: dict[str, str], limit: int = 20) -> None:
    """List recent documents."""
    resp = api_post(creds, "/v2/get-documents", {
        "limit": limit,
        "offset": 0,
        "include_last_viewed_panel": False,
    })
    docs = resp.get("docs", resp.get("documents", resp if isinstance(resp, list) else []))

    output = []
    for doc in docs:
        output.append({
            "id": doc.get("id"),
            "title": doc.get("title", "untitled"),
            "created_at": doc.get("created_at", ""),
        })
    print(json.dumps(output, indent=2))


def cmd_transcript(creds: dict[str, str], doc_id: str) -> None:
    """Get full transcript for a document."""
    resp = api_post(creds, "/v1/get-document-transcript", {"document_id": doc_id})

    entries = resp if isinstance(resp, list) else resp.get("transcript", resp.get("entries", []))

    lines: list[str] = []
    for entry in entries:
        source = entry.get("source", entry.get("speaker", "Unknown"))
        text = entry.get("text", entry.get("content", ""))
        start = entry.get("start_timestamp", "")
        end = entry.get("end_timestamp", "")

        ts = f" [{start} - {end}]" if start and end else (f" [{start}]" if start else "")
        lines.append(f"**{source}**{ts}: {text}")

    print("\n".join(lines))


def cmd_chat(creds: dict[str, str], prompt: str, doc_id: Optional[str], folder_id: Optional[str]) -> None:
    """Chat with document(s) using Granola's AI."""
    doc_ids: list[str] = []

    if doc_id:
        doc_ids = [doc_id]
    elif folder_id:
        resp = api_post(creds, "/v2/get-document-lists", {})
        folders = resp if isinstance(resp, list) else resp.get("document_lists", resp.get("lists", []))
        for folder in folders:
            if folder.get("id") == folder_id:
                raw_ids = folder.get("document_ids", folder.get("documents", []))
                doc_ids = [d if isinstance(d, str) else d.get("id", "") for d in raw_ids]
                break
        if not doc_ids:
            print(f"ERROR: Folder {folder_id} not found or empty.", file=sys.stderr)
            sys.exit(1)
    else:
        print("ERROR: Must specify --doc or --folder", file=sys.stderr)
        sys.exit(1)

    # Determine context view
    if len(doc_ids) == 1:
        view_context = {"view": "meeting", "meetingId": doc_ids[0], "userSelectedText": None}
        chat_context = "meeting"
    else:
        view_context = {"view": "folder", "folderId": folder_id, "userSelectedText": None}
        chat_context = "meeting"

    body = {
        "chat_history": [{
            "role": "USER",
            "text": prompt,
            "messageContext": {
                "mode": "all",
                "currentViewContext": view_context,
                "includeTranscripts": False,
                "additionalContext": {},
            },
        }],
        "document_ids": doc_ids,
        "chat_context": chat_context,
        "prompt_config": {
            "input_values": {},
            "model": "auto",
        },
        "exclude_transcripts": True,
        "transcripts": False,
        "deepdive": False,
        "fts_search": False,
        "web_search": False,
        "meeting_chat_date_range": {},
        "num_total_documents": len(doc_ids),
        "user_timezone": "Europe/London",
    }

    text = api_stream(creds, "/v1/chat-with-documents-web", body)
    if text:
        print(text)
    else:
        print("ERROR: No response received from chat API.", file=sys.stderr)
        sys.exit(1)


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Granola AI meeting notes helper")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("auth", help="Test authentication")
    sub.add_parser("workspaces", help="List workspaces")
    sub.add_parser("folders", help="List folders")

    docs_p = sub.add_parser("docs", help="List documents in a folder")
    docs_p.add_argument("folder_id", help="Folder ID")

    recent_p = sub.add_parser("recent", help="List recent documents")
    recent_p.add_argument("limit", nargs="?", type=int, default=20, help="Number of documents")

    transcript_p = sub.add_parser("transcript", help="Get document transcript")
    transcript_p.add_argument("doc_id", help="Document ID")

    chat_p = sub.add_parser("chat", help="Chat with document(s)")
    chat_p.add_argument("prompt", help="Chat prompt")
    chat_g = chat_p.add_mutually_exclusive_group(required=True)
    chat_g.add_argument("--doc", dest="doc_id", help="Document ID")
    chat_g.add_argument("--folder", dest="folder_id", help="Folder ID")

    args = parser.parse_args()

    creds = load_credentials()
    creds["workspace_id"] = get_workspace_id(creds)

    if args.command == "auth":
        cmd_auth(creds)
    elif args.command == "workspaces":
        cmd_workspaces(creds)
    elif args.command == "folders":
        cmd_folders(creds)
    elif args.command == "docs":
        cmd_docs(creds, args.folder_id)
    elif args.command == "recent":
        cmd_recent(creds, args.limit)
    elif args.command == "transcript":
        cmd_transcript(creds, args.doc_id)
    elif args.command == "chat":
        cmd_chat(creds, args.prompt, args.doc_id, args.folder_id)


if __name__ == "__main__":
    main()
