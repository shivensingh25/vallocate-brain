# # import os
# # import json
# # import sqlite3
# # import requests
# # from dotenv import load_dotenv
# # from google import genai

# # load_dotenv()

# # DB_FILE = "company_brain.db"
# # CLOCKIFY_KEY = os.environ["CLOCKIFY_API_KEY"]
# # BASE_URL = "https://api.clockify.me/api/v1"
# # HEADERS = {
# #     "X-Api-Key": CLOCKIFY_KEY,
# #     "Content-Type": "application/json",
# # }

# # client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# # def get_workspace_id():
# #     """Get the first workspace ID (free accounts have one workspace)."""
# #     response = requests.get(f"{BASE_URL}/workspaces", headers=HEADERS)
# #     response.raise_for_status()
# #     workspaces = response.json()
# #     if not workspaces:
# #         print("No workspaces found.")
# #         return None
# #     return workspaces[0]["id"]


# # def get_user_id():
# #     """Get the current user's ID."""
# #     response = requests.get(f"{BASE_URL}/user", headers=HEADERS)
# #     response.raise_for_status()
# #     return response.json()["id"]


# # def fetch_projects(workspace_id):
# #     """Get all projects in the workspace."""
# #     response = requests.get(
# #         f"{BASE_URL}/workspaces/{workspace_id}/projects",
# #         headers=HEADERS,
# #         params={"page-size": 100},
# #     )
# #     response.raise_for_status()
# #     return response.json()


# # def fetch_time_entries(workspace_id, user_id):
# #     """Get all time entries for the current user."""
# #     response = requests.get(
# #         f"{BASE_URL}/workspaces/{workspace_id}/user/{user_id}/time-entries",
# #         headers=HEADERS,
# #         params={"page-size": 200},
# #     )
# #     response.raise_for_status()
# #     return response.json()


# # def extract_knowledge(timesheet_text):
# #     prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

# # Below is timesheet data from Clockify showing hours logged by consultants on projects.

# # Extract useful information about:
# # 1. SKILL SIGNALS: what skills does the work description suggest the person has
# # 2. PROJECT CONTEXT: project names, types of work being done, time invested
# # 3. WORKLOAD SIGNALS: how many hours someone is working, overwork patterns
# # 4. AVAILABILITY: if someone logged few hours, they may have capacity

# # Return a JSON array of objects with:
# # - type: "skill" | "project" | "workload" | "availability"
# # - person_mentioned: name of person (or null)
# # - summary: one sentence description
# # - detail: more context like hours, project, dates
# # - confidence: "high" | "medium" | "low"
# # - source_space: "Clockify Timesheets"

# # Return ONLY the JSON array. No markdown. No backticks.
# # If nothing relevant, return: []

# # TIMESHEET DATA:
# # {timesheet_text}"""

# #     response = client.models.generate_content(
# #         model="gemini-3.1-flash-lite",
# #         contents=prompt
# #     )
# #     response_text = response.text.strip()

# #     if "```" in response_text:
# #         parts = response_text.split("```")
# #         response_text = parts[1] if len(parts) > 1 else parts[0]
# #         if response_text.startswith("json"):
# #             response_text = response_text[4:]
# #     response_text = response_text.strip()

# #     try:
# #         return json.loads(response_text)
# #     except json.JSONDecodeError:
# #         print(f"  Could not parse Gemini response")
# #         return []


# # def store_knowledge(conn, items):
# #     for item in items:
# #         conn.execute(
# #             """INSERT INTO knowledge
# #                (type, person_mentioned, summary, detail, confidence, source_space)
# #                VALUES (?, ?, ?, ?, ?, ?)""",
# #             (
# #                 item.get("type"),
# #                 item.get("person_mentioned"),
# #                 item.get("summary"),
# #                 item.get("detail"),
# #                 item.get("confidence"),
# #                 item.get("source_space"),
# #             ),
# #         )
# #     conn.commit()


# # def run():
# #     print("Vallocate Brain - Clockify Timesheet Ingestion")
# #     print("=" * 50)

# #     print("\n1. Connecting to Clockify...")
# #     workspace_id = get_workspace_id()
# #     if not workspace_id:
# #         return
# #     user_id = get_user_id()
# #     print(f"   Workspace: {workspace_id}")
# #     print(f"   User: {user_id}")

# #     print("\n2. Fetching projects...")
# #     projects = fetch_projects(workspace_id)
# #     print(f"   Found {len(projects)} projects")

# #     # Build a project ID to name map
# #     project_map = {p["id"]: p["name"] for p in projects}

# #     print("\n3. Fetching time entries...")
# #     entries = fetch_time_entries(workspace_id, user_id)
# #     print(f"   Found {len(entries)} time entries")

# #     if not entries:
# #         print("   No time entries found. Add some in Clockify first.")
# #         return

# #     # Format entries into readable text for Gemini
# #     timesheet_text = ""
# #     for entry in entries:
# #         project_name = project_map.get(entry.get("projectId"), "No project")
# #         description = entry.get("description", "No description")
# #         start = entry.get("timeInterval", {}).get("start", "")
# #         end = entry.get("timeInterval", {}).get("end", "")
# #         duration = entry.get("timeInterval", {}).get("duration", "")

# #         timesheet_text += f"Project: {project_name}\n"
# #         timesheet_text += f"  Task: {description}\n"
# #         timesheet_text += f"  Start: {start}\n"
# #         timesheet_text += f"  End: {end}\n"
# #         timesheet_text += f"  Duration: {duration}\n\n"

# #     print("\n4. Extracting knowledge via Gemini...")
# #     items = extract_knowledge(timesheet_text)
# #     print(f"   Extracted {len(items)} knowledge items")

# #     print("\n5. Storing in database...")
# #     conn = sqlite3.connect(DB_FILE)
# #     if items:
# #         store_knowledge(conn, items)

# #     conn.execute(
# #         "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (?, ?, ?)",
# #         ("Clockify Timesheets", len(entries), len(items)),
# #     )
# #     conn.commit()
# #     conn.close()

# #     print(f"\n{'=' * 50}")
# #     print(f"Done. Extracted {len(items)} items from {len(entries)} time entries.")


# # if __name__ == "__main__":
# #     run()



# import os
# import json
# import sqlite3
# import requests
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# DB_FILE = "company_brain.db"
# CLOCKIFY_KEY = os.environ["CLOCKIFY_API_KEY"]
# BASE_URL = "https://api.clockify.me/api/v1"
# HEADERS = {
#     "X-Api-Key": CLOCKIFY_KEY,
#     "Content-Type": "application/json",
# }

# client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# def get_workspace_id():
#     """Get the first workspace ID."""
#     response = requests.get(f"{BASE_URL}/workspaces", headers=HEADERS)
#     response.raise_for_status()
#     workspaces = response.json()
#     if not workspaces:
#         print("No workspaces found.")
#         return None
#     return workspaces[0]["id"]


# def fetch_all_users(workspace_id):
#     """Get all users in the workspace with their names and IDs."""
#     response = requests.get(
#         f"{BASE_URL}/workspaces/{workspace_id}/users",
#         headers=HEADERS,
#         params={"page-size": 100},
#     )
#     response.raise_for_status()
#     users = response.json()
#     return [{"id": u["id"], "name": u["name"]} for u in users]


# def fetch_projects(workspace_id):
#     """Get all projects in the workspace."""
#     response = requests.get(
#         f"{BASE_URL}/workspaces/{workspace_id}/projects",
#         headers=HEADERS,
#         params={"page-size": 100},
#     )
#     response.raise_for_status()
#     return response.json()


# def fetch_time_entries(workspace_id, user_id):
#     """Get all time entries for a specific user."""
#     response = requests.get(
#         f"{BASE_URL}/workspaces/{workspace_id}/user/{user_id}/time-entries",
#         headers=HEADERS,
#         params={"page-size": 200},
#     )
#     response.raise_for_status()
#     return response.json()


# def extract_knowledge(timesheet_text):
#     prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

# Below is timesheet data from Clockify showing hours logged by consultants on projects.

# Extract useful information about:
# 1. SKILL SIGNALS: what skills does the work description suggest the person has
# 2. PROJECT CONTEXT: project names, types of work being done, time invested
# 3. WORKLOAD SIGNALS: how many hours someone is working, overwork patterns
# 4. AVAILABILITY: if someone logged few hours, they may have capacity

# Return a JSON array of objects with:
# - type: "skill" | "project" | "workload" | "availability"
# - person_mentioned: name of person (or null)
# - summary: one sentence description
# - detail: more context like hours, project, dates
# - confidence: "high" | "medium" | "low"
# - source_space: "Clockify Timesheets"

# Return ONLY the JSON array. No markdown. No backticks.
# If nothing relevant, return: []

# TIMESHEET DATA:
# {timesheet_text}"""

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
#         print(f"  Could not parse Gemini response")
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
#     print("Vallocate Brain - Clockify Timesheet Ingestion")
#     print("=" * 50)

#     print("\n1. Connecting to Clockify...")
#     workspace_id = get_workspace_id()
#     if not workspace_id:
#         return

#     print("\n2. Fetching all users in workspace...")
#     users = fetch_all_users(workspace_id)
#     print(f"   Found {len(users)} users:")
#     for u in users:
#         print(f"     - {u['name']}")

#     print("\n3. Fetching projects...")
#     projects = fetch_projects(workspace_id)
#     print(f"   Found {len(projects)} projects")
#     project_map = {p["id"]: p["name"] for p in projects}

#     conn = sqlite3.connect(DB_FILE)
#     total_entries = 0
#     total_items = 0

#     for user in users:
#         user_name = user["name"]
#         user_id = user["id"]

#         print(f"\n4. Fetching time entries for {user_name}...")
#         entries = fetch_time_entries(workspace_id, user_id)
#         print(f"   Found {len(entries)} entries")

#         if not entries:
#             print(f"   No entries for {user_name}. Skipping.")
#             continue

#         total_entries += len(entries)

#         timesheet_text = ""
#         for entry in entries:
#             project_name = project_map.get(entry.get("projectId"), "No project")
#             description = entry.get("description", "No description")
#             start = entry.get("timeInterval", {}).get("start", "")
#             duration = entry.get("timeInterval", {}).get("duration", "")

#             timesheet_text += f"Consultant: {user_name}\n"
#             timesheet_text += f"  Project: {project_name}\n"
#             timesheet_text += f"  Task: {description}\n"
#             timesheet_text += f"  Date: {start}\n"
#             timesheet_text += f"  Duration: {duration}\n\n"

#         print(f"   Extracting knowledge via Gemini...")
#         items = extract_knowledge(timesheet_text)
#         print(f"   Extracted {len(items)} knowledge items for {user_name}")

#         if items:
#             store_knowledge(conn, items)
#             total_items += len(items)

#     conn.execute(
#         "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (?, ?, ?)",
#         ("Clockify Timesheets", total_entries, total_items),
#     )
#     conn.commit()
#     conn.close()

#     print(f"\n{'=' * 50}")
#     print(f"Done. Extracted {total_items} items from {total_entries} entries across {len(users)} users.")


# if __name__ == "__main__":
#     run()

import os
import json
import db
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

CLOCKIFY_KEY = os.environ["CLOCKIFY_API_KEY"]
BASE_URL = "https://api.clockify.me/api/v1"
HEADERS = {
    "X-Api-Key": CLOCKIFY_KEY,
    "Content-Type": "application/json",
}

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def get_workspace_id():
    response = requests.get(f"{BASE_URL}/workspaces", headers=HEADERS)
    response.raise_for_status()
    workspaces = response.json()
    if not workspaces:
        print("No workspaces found.")
        return None
    return workspaces[0]["id"]


def fetch_all_users(workspace_id):
    response = requests.get(
        f"{BASE_URL}/workspaces/{workspace_id}/users",
        headers=HEADERS,
        params={"page-size": 100},
    )
    response.raise_for_status()
    users = response.json()
    return [{"id": u["id"], "name": u["name"]} for u in users]


def fetch_projects(workspace_id):
    response = requests.get(
        f"{BASE_URL}/workspaces/{workspace_id}/projects",
        headers=HEADERS,
        params={"page-size": 100},
    )
    response.raise_for_status()
    return response.json()


def fetch_time_entries(workspace_id, user_id):
    response = requests.get(
        f"{BASE_URL}/workspaces/{workspace_id}/user/{user_id}/time-entries",
        headers=HEADERS,
        params={"page-size": 200},
    )
    response.raise_for_status()
    return response.json()


def extract_knowledge(timesheet_text):
    prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

Below is timesheet data from Clockify showing hours logged by consultants on projects.

Extract useful information about:
1. SKILL SIGNALS: what skills does the work description suggest the person has
2. PROJECT CONTEXT: project names, types of work being done, time invested
3. WORKLOAD SIGNALS: how many hours someone is working, overwork patterns
4. AVAILABILITY: if someone logged few hours, they may have capacity

Return a JSON array of objects with:
- type: "skill" | "project" | "workload" | "availability"
- person_mentioned: name of person (or null)
- summary: one sentence description
- detail: more context like hours, project, dates
- confidence: "high" | "medium" | "low"
- source_space: "Clockify Timesheets"

Return ONLY the JSON array. No markdown. No backticks.
If nothing relevant, return: []

TIMESHEET DATA:
{timesheet_text}"""

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
        print(f"  Could not parse Gemini response")
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
    print("Vallocate Brain - Clockify Timesheet Ingestion")
    print("=" * 50)

    print("\n1. Connecting to Clockify...")
    workspace_id = get_workspace_id()
    if not workspace_id:
        return

    print("\n2. Fetching all users in workspace...")
    users = fetch_all_users(workspace_id)
    print(f"   Found {len(users)} users:")
    for u in users:
        print(f"     - {u['name']}")

    print("\n3. Fetching projects...")
    projects = fetch_projects(workspace_id)
    print(f"   Found {len(projects)} projects")
    project_map = {p["id"]: p["name"] for p in projects}

    total_entries = 0
    total_items = 0

    for user in users:
        user_name = user["name"]
        user_id = user["id"]

        print(f"\n4. Fetching time entries for {user_name}...")
        entries = fetch_time_entries(workspace_id, user_id)
        print(f"   Found {len(entries)} entries")

        if not entries:
            print(f"   No entries for {user_name}. Skipping.")
            continue

        total_entries += len(entries)

        timesheet_text = ""
        for entry in entries:
            project_name = project_map.get(entry.get("projectId"), "No project")
            description = entry.get("description", "No description")
            start = entry.get("timeInterval", {}).get("start", "")
            duration = entry.get("timeInterval", {}).get("duration", "")

            timesheet_text += f"Consultant: {user_name}\n"
            timesheet_text += f"  Project: {project_name}\n"
            timesheet_text += f"  Task: {description}\n"
            timesheet_text += f"  Date: {start}\n"
            timesheet_text += f"  Duration: {duration}\n\n"

        print(f"   Extracting knowledge via Gemini...")
        items = extract_knowledge(timesheet_text)
        print(f"   Extracted {len(items)} knowledge items for {user_name}")

        if items:
            store_knowledge(items)
            total_items += len(items)

    db.execute(
        "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (%s, %s, %s)",
        ("Clockify Timesheets", total_entries, total_items),
    )

    print(f"\n{'=' * 50}")
    print(f"Done. Extracted {total_items} items from {total_entries} entries across {len(users)} users.")


if __name__ == "__main__":
    run()
