import os
import json
import sqlite3
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

DB_FILE = "company_brain.db"
HUBSPOT_TOKEN = os.environ["HUBSPOT_TOKEN"]

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def fetch_deals():
    """Pull all deals (project cards) from HubSpot."""
    url = "https://api.hubapi.com/crm/v3/objects/deals"
    headers = {"Authorization": f"Bearer {HUBSPOT_TOKEN}"}
    # Ask for useful properties on each deal
    params = {
        "limit": 100,
        "properties": "dealname,amount,dealstage,closedate,pipeline,description,industry",
    }

    deals = []
    after = None
    while True:
        if after:
            params["after"] = after
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        deals.extend(data.get("results", []))
        paging = data.get("paging", {})
        if "next" in paging:
            after = paging["next"]["after"]
        else:
            break
    return deals


def extract_knowledge(deals_text):
    """Send deal data to Gemini for structured knowledge extraction."""
    prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

Below are deal/project records from HubSpot CRM.

Extract useful information about:
1. PROJECT CONTEXT: project name, client, value, stage, timeline, industry
2. PROJECT REQUIREMENTS: what kind of work or skills the project likely needs

Return a JSON array of objects. Each object must have:
- type: "project" | "requirement"
- person_mentioned: null (deals do not name consultants, leave this empty)
- summary: one sentence describing the project
- detail: more context like value, stage, industry
- confidence: "high" | "medium" | "low"
- source_space: "HubSpot Deals"

Return ONLY the JSON array. No markdown. No backticks.
If nothing relevant, return: []

DEALS:
{deals_text}"""

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
        print(f"  Raw: {response_text[:300]}")
        return []


def store_knowledge(conn, items):
    for item in items:
        conn.execute(
            """INSERT INTO knowledge
               (type, person_mentioned, summary, detail, confidence, source_space)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                item.get("type"),
                item.get("person_mentioned"),
                item.get("summary"),
                item.get("detail"),
                item.get("confidence"),
                item.get("source_space"),
            ),
        )
    conn.commit()


def run():
    print("Vallocate Brain - HubSpot Ingestion")
    print("=" * 45)

    print("\n1. Fetching deals from HubSpot...")
    deals = fetch_deals()
    print(f"   Found {len(deals)} deals")

    if not deals:
        print("   No deals found. Create some test deals in HubSpot first.")
        return

    # Format deals into readable text for Gemini
    deals_text = ""
    for deal in deals:
        props = deal.get("properties", {})
        deals_text += f"Deal: {props.get('dealname', 'Unnamed')}\n"
        deals_text += f"  Amount: {props.get('amount', 'N/A')}\n"
        deals_text += f"  Stage: {props.get('dealstage', 'N/A')}\n"
        deals_text += f"  Close date: {props.get('closedate', 'N/A')}\n"
        deals_text += f"  Industry: {props.get('industry', 'N/A')}\n"
        deals_text += f"  Description: {props.get('description', 'N/A')}\n\n"

    print("\n2. Extracting knowledge via Gemini...")
    items = extract_knowledge(deals_text)
    print(f"   Extracted {len(items)} knowledge items")

    print("\n3. Storing in database...")
    conn = sqlite3.connect(DB_FILE)
    store_knowledge(conn, items)
    conn.execute(
        "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (?, ?, ?)",
        ("HubSpot Deals", len(deals), len(items)),
    )
    conn.commit()
    conn.close()

    print(f"\n{'=' * 45}")
    print(f"Done. Extracted {len(items)} items from {len(deals)} deals.")


if __name__ == "__main__":
    run()