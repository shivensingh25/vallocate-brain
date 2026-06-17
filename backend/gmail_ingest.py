# import os
# import json
# import sqlite3
# import base64
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


# def fetch_emails(gmail_service, max_results=50):
#     """Fetch recent emails from Gmail inbox."""
#     results = gmail_service.users().messages().list(
#         userId="me",
#         maxResults=max_results,
#         q="newer_than:30d"  # only emails from last 30 days
#     ).execute()

#     messages = results.get("messages", [])
#     emails = []

#     for msg in messages:
#         full = gmail_service.users().messages().get(
#             userId="me",
#             id=msg["id"],
#             format="full"
#         ).execute()

#         headers = full.get("payload", {}).get("headers", [])
#         subject = ""
#         sender = ""
#         date = ""
#         for h in headers:
#             if h["name"] == "Subject":
#                 subject = h["value"]
#             elif h["name"] == "From":
#                 sender = h["value"]
#             elif h["name"] == "Date":
#                 date = h["value"]

#         # Get email body text
#         body = ""
#         payload = full.get("payload", {})
#         if "parts" in payload:
#             for part in payload["parts"]:
#                 if part.get("mimeType") == "text/plain":
#                     data = part.get("body", {}).get("data", "")
#                     if data:
#                         body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
#                     break
#         elif "body" in payload:
#             data = payload["body"].get("data", "")
#             if data:
#                 body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

#         # Trim body to first 1000 chars to stay within token limits
#         body = body[:1000] if body else ""

#         emails.append({
#             "subject": subject,
#             "from": sender,
#             "date": date,
#             "body": body,
#         })

#     return emails


# def extract_knowledge(emails_text):
#     prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

# Below are emails from a Gmail inbox.

# Extract useful information about:
# 1. CONSULTANT SKILLS: any mention of skills or expertise
# 2. PROJECT CONTEXT: project names, clients, timelines, requirements
# 3. ALLOCATION SIGNALS: who should work on what and why
# 4. PERFORMANCE SIGNALS: how someone performed
# 5. AVAILABILITY: who is free, on leave, or finishing a project
# 6. PREFERENCES: what someone wants to work on
# 7. CLIENT CONTEXT: client expectations, relationship signals

# Return a JSON array of objects with:
# - type: "skill" | "project" | "allocation" | "performance" | "availability" | "preference" | "client"
# - person_mentioned: name of person discussed (or null)
# - summary: one sentence description
# - detail: more context if available
# - confidence: "high" | "medium" | "low"
# - source_space: "Gmail"

# Return ONLY the JSON array. No markdown. No backticks.
# If nothing relevant, return: []
# Skip newsletters, marketing emails, and automated notifications.

# EMAILS:
# {emails_text}"""

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
#         print(f"  Could not parse response")
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
#     print("Vallocate Brain - Gmail Ingestion")
#     print("=" * 45)

#     print("\n1. Authenticating with Google...")
#     creds = get_google_creds()
#     gmail_service = build("gmail", "v1", credentials=creds)
#     print("   Done.")

#     print("\n2. Fetching emails (last 30 days)...")
#     emails = fetch_emails(gmail_service, max_results=50)
#     print(f"   Found {len(emails)} emails")

#     if not emails:
#         print("   No emails found.")
#         return

#     # Format emails for Gemini
#     # Process in batches of 10 to stay within token limits
#     conn = sqlite3.connect(DB_FILE)
#     total_items = 0

#     batch_size = 10
#     for i in range(0, len(emails), batch_size):
#         batch = emails[i:i + batch_size]
#         emails_text = ""
#         for email in batch:
#             emails_text += f"Subject: {email['subject']}\n"
#             emails_text += f"From: {email['from']}\n"
#             emails_text += f"Date: {email['date']}\n"
#             emails_text += f"Body: {email['body']}\n\n---\n\n"

#         print(f"\n3. Extracting knowledge from emails {i+1}-{i+len(batch)}...")
#         items = extract_knowledge(emails_text)
#         print(f"   Extracted {len(items)} items")

#         if items:
#             store_knowledge(conn, items)
#             total_items += len(items)

#     conn.execute(
#         "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (?, ?, ?)",
#         ("Gmail", len(emails), total_items),
#     )
#     conn.commit()
#     conn.close()

#     print(f"\n{'=' * 45}")
#     print(f"Done. Extracted {total_items} items from {len(emails)} emails.")


# if __name__ == "__main__":
#     run()

import os
import json
import db
import base64
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


def fetch_emails(gmail_service, max_results=50):
    results = gmail_service.users().messages().list(
        userId="me",
        maxResults=max_results,
        q="newer_than:30d"
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        full = gmail_service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = full.get("payload", {}).get("headers", [])
        subject = ""
        sender = ""
        date = ""
        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            elif h["name"] == "From":
                sender = h["value"]
            elif h["name"] == "Date":
                date = h["value"]

        body = ""
        payload = full.get("payload", {})
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break
        elif "body" in payload:
            data = payload["body"].get("data", "")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        body = body[:1000] if body else ""

        emails.append({
            "subject": subject,
            "from": sender,
            "date": date,
            "body": body,
        })

    return emails


def extract_knowledge(emails_text):
    prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

Below are emails from a Gmail inbox.

Extract useful information about:
1. CONSULTANT SKILLS: any mention of skills or expertise
2. PROJECT CONTEXT: project names, clients, timelines, requirements
3. ALLOCATION SIGNALS: who should work on what and why
4. PERFORMANCE SIGNALS: how someone performed
5. AVAILABILITY: who is free, on leave, or finishing a project
6. PREFERENCES: what someone wants to work on
7. CLIENT CONTEXT: client expectations, relationship signals

Return a JSON array of objects with:
- type: "skill" | "project" | "allocation" | "performance" | "availability" | "preference" | "client"
- person_mentioned: name of person discussed (or null)
- summary: one sentence description
- detail: more context if available
- confidence: "high" | "medium" | "low"
- source_space: "Gmail"

Return ONLY the JSON array. No markdown. No backticks.
If nothing relevant, return: []
Skip newsletters, marketing emails, and automated notifications.

EMAILS:
{emails_text}"""

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
        print(f"  Could not parse response")
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
    print("Vallocate Brain - Gmail Ingestion")
    print("=" * 45)

    print("\n1. Authenticating with Google...")
    creds = get_google_creds()
    gmail_service = build("gmail", "v1", credentials=creds)
    print("   Done.")

    print("\n2. Fetching emails (last 30 days)...")
    emails = fetch_emails(gmail_service, max_results=50)
    print(f"   Found {len(emails)} emails")

    if not emails:
        print("   No emails found.")
        return

    total_items = 0

    batch_size = 10
    for i in range(0, len(emails), batch_size):
        batch = emails[i:i + batch_size]
        emails_text = ""
        for email in batch:
            emails_text += f"Subject: {email['subject']}\n"
            emails_text += f"From: {email['from']}\n"
            emails_text += f"Date: {email['date']}\n"
            emails_text += f"Body: {email['body']}\n\n---\n\n"

        print(f"\n3. Extracting knowledge from emails {i+1}-{i+len(batch)}...")
        items = extract_knowledge(emails_text)
        print(f"   Extracted {len(items)} items")

        if items:
            store_knowledge(items)
            total_items += len(items)

    db.execute(
        "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (%s, %s, %s)",
        ("Gmail", len(emails), total_items),
    )

    print(f"\n{'=' * 45}")
    print(f"Done. Extracted {total_items} items from {len(emails)} emails.")


if __name__ == "__main__":
    run()
