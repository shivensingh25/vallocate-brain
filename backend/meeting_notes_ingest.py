# import os
# import json
# import sqlite3
# from dotenv import load_dotenv
# from google import genai
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build

# load_dotenv()

# DB_FILE = "company_brain.db"

# SCOPES = [
#     "https://www.googleapis.com/auth/chat.spaces.readonly",
#     "https://www.googleapis.com/auth/chat.messages.readonly",
#     "https://www.googleapis.com/auth/chat.memberships.readonly",
#     "https://www.googleapis.com/auth/gmail.readonly",
#     "https://www.googleapis.com/auth/drive.readonly",
#     "https://www.googleapis.com/auth/documents.readonly",
# ]

# client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# def get_google_creds():
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as f:
#             f.write(creds.to_json())
#     return creds


# def find_meeting_notes(drive_service):
#     """Search Google Drive for Gemini meeting notes."""
#     query = "name contains 'Notes by Gemini' and mimeType='application/vnd.google-apps.document'"
#     results = drive_service.files().list(
#         q=query,
#         pageSize=50,
#         fields="files(id, name, createdTime, modifiedTime)",
#         orderBy="modifiedTime desc",
#     ).execute()
#     return results.get("files", [])


# def read_document(docs_service, doc_id):
#     """Read the full text content of a Google Doc."""
#     doc = docs_service.documents().get(documentId=doc_id).execute()
#     content = doc.get("body", {}).get("content", [])

#     text = ""
#     for element in content:
#         if "paragraph" in element:
#             for elem in element["paragraph"].get("elements", []):
#                 if "textRun" in elem:
#                     text += elem["textRun"]["content"]
#     return text


# def extract_knowledge(doc_text, doc_name):
#     # Trim to first 5000 chars to stay within token limits
#     doc_text = doc_text[:5000]

#     prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

# Below is a meeting transcript/notes document: {doc_name}

# Extract useful information about:
# 1. CONSULTANT SKILLS: any mention of skills, expertise, or capabilities
# 2. PROJECT CONTEXT: project names, clients, timelines, requirements, budgets
# 3. ALLOCATION SIGNALS: who should work on what project and why
# 4. PERFORMANCE SIGNALS: how a consultant performed, client feedback
# 5. AVAILABILITY: who is free, finishing a project, on leave
# 6. PREFERENCES: what a consultant wants to work on
# 7. DECISIONS: any decisions made about staffing, projects, or processes

# Return a JSON array of objects with:
# - type: "skill" | "project" | "allocation" | "performance" | "availability" | "preference" | "decision"
# - person_mentioned: name of person discussed (or null)
# - summary: one sentence description
# - detail: more context if available
# - confidence: "high" | "medium" | "low"
# - source_space: "Meeting Notes: {doc_name}"

# Return ONLY the JSON array. No markdown. No backticks.
# If nothing relevant, return: []

# DOCUMENT:
# {doc_text}"""

#     response = client.models.generate_content(
#         model="gemini-3.1-flash-lite",
#         contents=prompt
#     )
#     response_text = response.text.strip()

#     if "```" in response_text:
#         parts = response_text.split("```")
#         response_text = parts[1] if len(parts) > 1 else parts[0]
#         if response_text.startswith("json"):
#             response_text = response_text[4:]
#     response_text = response_text.strip()

#     try:
#         return json.loads(response_text)
#     except json.JSONDecodeError:
#         print(f"  Could not parse response for {doc_name}")
#         return []


# def store_knowledge(conn, items):
#     for item in items:
#         conn.execute(
#             """INSERT INTO knowledge
#                (type, person_mentioned, summary, detail, confidence, source_space)
#                VALUES (?, ?, ?, ?, ?, ?)""",
#             (
#                 item.get("type"),
#                 item.get("person_mentioned"),
#                 item.get("summary"),
#                 item.get("detail"),
#                 item.get("confidence"),
#                 item.get("source_space"),
#             ),
#         )
#     conn.commit()


# def run():
#     print("Vallocate Brain - Meeting Notes Ingestion")
#     print("=" * 45)

#     print("\n1. Authenticating with Google...")
#     creds = get_google_creds()
#     drive_service = build("drive", "v3", credentials=creds)
#     docs_service = build("docs", "v1", credentials=creds)
#     print("   Done.")

#     print("\n2. Searching for meeting notes in Google Drive...")
#     files = find_meeting_notes(drive_service)
#     print(f"   Found {len(files)} meeting notes documents")

#     if not files:
#         print("   No meeting notes found. Looking for docs with 'Notes by Gemini' in the name.")
#         return

#     conn = sqlite3.connect(DB_FILE)
#     total_items = 0

#     for file in files:
#         doc_id = file["id"]
#         doc_name = file["name"]
#         print(f"\n   Processing: {doc_name}")

#         text = read_document(docs_service, doc_id)
#         if not text.strip():
#             print("   Empty document. Skipping.")
#             continue

#         print(f"   Read {len(text)} characters")
#         print("   Extracting knowledge via Gemini...")
#         items = extract_knowledge(text, doc_name)
#         print(f"   Extracted {len(items)} items")

#         if items:
#             store_knowledge(conn, items)
#             total_items += len(items)

#         conn.execute(
#             "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (?, ?, ?)",
#             (f"Meeting Notes: {doc_name}", 1, len(items)),
#         )
#         conn.commit()

#     conn.close()

#     print(f"\n{'=' * 45}")
#     print(f"Done. Extracted {total_items} items from {len(files)} meeting notes.")


# if __name__ == "__main__":
#     run()

import os
import json
import db
from dotenv import load_dotenv
from google import genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/chat.memberships.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def get_google_creds():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return creds


def find_meeting_notes(drive_service):
    query = "(name contains 'Notes by Gemini' or name contains 'Transcript' or name contains 'Meeting') and mimeType='application/vnd.google-apps.document'"
    results = drive_service.files().list(
        q=query,
        pageSize=50,
        fields="files(id, name, createdTime, modifiedTime)",
        orderBy="modifiedTime desc",
    ).execute()
    return results.get("files", [])


def read_document(docs_service, doc_id):
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content = doc.get("body", {}).get("content", [])

    text = ""
    for element in content:
        if "paragraph" in element:
            for elem in element["paragraph"].get("elements", []):
                if "textRun" in elem:
                    text += elem["textRun"]["content"]
    return text


def extract_knowledge(doc_text, doc_name):
    doc_text = doc_text[:5000]

    prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

Below is a meeting transcript/notes document: {doc_name}

Extract useful information about:
1. CONSULTANT SKILLS: any mention of skills, expertise, or capabilities
2. PROJECT CONTEXT: project names, clients, timelines, requirements, budgets
3. ALLOCATION SIGNALS: who should work on what project and why
4. PERFORMANCE SIGNALS: how a consultant performed, client feedback
5. AVAILABILITY: who is free, finishing a project, on leave
6. PREFERENCES: what a consultant wants to work on
7. DECISIONS: any decisions made about staffing, projects, or processes

Return a JSON array of objects with:
- type: "skill" | "project" | "allocation" | "performance" | "availability" | "preference" | "decision"
- person_mentioned: name of person discussed (or null)
- summary: one sentence description
- detail: more context if available
- confidence: "high" | "medium" | "low"
- source_space: "Meeting Notes: {doc_name}"

Return ONLY the JSON array. No markdown. No backticks.
If nothing relevant, return: []

DOCUMENT:
{doc_text}"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    response_text = response.text.strip()

    if "```" in response_text:
        parts = response_text.split("```")
        response_text = parts[1] if len(parts) > 1 else parts[0]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    response_text = response_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        print(f"  Could not parse response for {doc_name}")
        return []


def store_knowledge(items):
    for item in items:
        db.execute(
            """INSERT INTO knowledge
               (type, person_mentioned, summary, detail, confidence, source_space)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                item.get("type"),
                item.get("person_mentioned"),
                item.get("summary"),
                item.get("detail"),
                item.get("confidence"),
                item.get("source_space"),
            ),
        )


def run():
    print("Vallocate Brain - Meeting Notes Ingestion")
    print("=" * 45)

    print("\n1. Authenticating with Google...")
    creds = get_google_creds()
    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)
    print("   Done.")

    print("\n2. Searching for meeting notes in Google Drive...")
    files = find_meeting_notes(drive_service)
    print(f"   Found {len(files)} meeting notes documents")

    if not files:
        print("   No meeting notes found.")
        return

    total_items = 0

    for file in files:
        doc_id = file["id"]
        doc_name = file["name"]
        print(f"\n   Processing: {doc_name}")

        text = read_document(docs_service, doc_id)
        if not text.strip():
            print("   Empty document. Skipping.")
            continue

        print(f"   Read {len(text)} characters")
        print("   Extracting knowledge via Gemini...")
        items = extract_knowledge(text, doc_name)
        print(f"   Extracted {len(items)} items")

        if items:
            store_knowledge(items)
            total_items += len(items)

        db.execute(
            "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (%s, %s, %s)",
            (f"Meeting Notes: {doc_name}", 1, len(items)),
        )

    print(f"\n{'=' * 45}")
    print(f"Done. Extracted {total_items} items from {len(files)} meeting notes.")


if __name__ == "__main__":
    run()
