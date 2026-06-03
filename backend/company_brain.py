# gives the script the ability to talk to the operating system, read files, and access
# environment variables like the API key you stored in the .env file
import os

# lets the script read and write structured labelled data. Gemini sends its answer back
# as JSON and this is what lets you actually understand and use that answer
import json

# a simple database that lives as a single file on your computer. no separate
# database server needed, it just sits in the project folder like any other file
import sqlite3

# imports just the one function we need from the dotenv library. this function opens
# your .env file and loads things like GEMINI_API_KEY into memory for the rest of the script
from dotenv import load_dotenv

# Google's Gemini AI library. the new google-genai package replaced the deprecated
# google.generativeai package, and this is the updated import style
from google import genai

# handles the saved login token from a previous run of the script
from google.oauth2.credentials import Credentials

# runs the browser login flow when there is no saved token and the user needs to sign in
from google_auth_oauthlib.flow import InstalledAppFlow

# handles quietly refreshing an expired token in the background without opening a browser
from google.auth.transport.requests import Request

# the "build" function creates a connection object to a specific Google API.
# later you use it like build("chat", "v1") to get a live connection to Google Chat
from googleapiclient.discovery import build

# actually runs the load_dotenv function imported above. opens your .env file and puts
# GEMINI_API_KEY into memory so the rest of the script can read it with os.environ
load_dotenv()

SCOPES = [
    # these three scopes tell Google exactly what this app is allowed to do.
    # the word "readonly" at the end of each one means the script can never
    # write, delete, or change anything in Google Chat, only read it
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/chat.memberships.readonly",
]

# store the database filename in one variable so if you ever want to rename it
# you only have to change it here, not in every place it gets used below
DB_FILE = "company_brain.db"

# creates the Gemini client with your API key. the new library uses a Client object
# instead of configuring a global state, which is cleaner and easier to reason about.
# every request to Gemini goes through this client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def get_google_creds():
    # reusable login function. whenever the script needs to talk to Google it calls this.
    # it figures out whether to use a saved token, refresh an expired one, or open a browser login.
    # the empty parentheses mean it takes no inputs, it figures everything out on its own

    # start with empty credentials. the script will try to fill this in from a saved file next
    creds = None

    if os.path.exists("token.json"):
        # if a saved login token exists from a previous run, load it so we skip the browser entirely.
        # like checking your pocket for a train ticket before going to buy a new one
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # token exists but has expired. quietly renew it in the background without opening a browser
            creds.refresh(Request())
        else:
            # no saved token at all. open a browser window so the user can sign in to Google
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # save the new or refreshed token to disk so the next run can skip all of this
        with open("token.json", "w") as f:
            f.write(creds.to_json())

    # send the credentials back to whoever called this function so they can make authenticated requests
    return creds


def fetch_all_spaces(service):
    # asks Google Chat what spaces this user belongs to (group chats, direct messages, channels).
    # Google only returns 100 at a time so we loop and use a page_token as a bookmark.
    # each loop asks for the next batch. when there is no token left, we are done
    spaces = []
    page_token = None
    while True:
        result = service.spaces().list(pageSize=100, pageToken=page_token).execute()
        spaces.extend(result.get("spaces", []))
        # Google hands back a token to get the next page. if there is no token, we have everything
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return spaces


def fetch_messages(service, space_name, max_messages=100):
    # same pagination idea as fetch_all_spaces but for messages inside one specific space.
    # max_messages=100 is a safety cap so we do not accidentally pull thousands of messages
    # and hit API rate limits on the free tier
    messages = []
    page_token = None
    while len(messages) < max_messages:
        result = (
            service.spaces()
            .messages()
            .list(
                parent=space_name,
                pageSize=min(100, max_messages - len(messages)),  # never ask for more than we still need
                pageToken=page_token,
            )
            .execute()
        )
        messages.extend(result.get("messages", []))
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return messages


def extract_knowledge(messages_text, space_name):
    # the brain of the brain. takes a block of raw chat messages and sends them to Gemini.
    # gets back structured knowledge items about consultants, projects, and availability

    # the instruction we send to Gemini. the f-string means {space_name} and {messages_text}
    # get replaced with their actual values before the text is sent.
    # this is like writing a job brief: "read these conversations, find these specific things,
    # write them up in exactly this format"
    prompt = f"""You are a knowledge extraction agent for a consulting firm company brain.

Below are messages from the Google Chat space: {space_name}

Extract useful information about:
1. CONSULTANT SKILLS: technical or domain skills mentioned
2. PROJECT CONTEXT: project names, clients, timelines, requirements
3. ALLOCATION SIGNALS: who should work on what and why
4. PERFORMANCE SIGNALS: how a consultant performed
5. AVAILABILITY: who is free or finishing a project
6. PREFERENCES: what someone wants to work on

Return a JSON array of objects. Each object must have:
- type: "skill" | "project" | "allocation" | "performance" | "availability" | "preference"
- person_mentioned: name of the person being discussed
- summary: one sentence describing what you found
- detail: more context if available
- confidence: "high" | "medium" | "low"
- source_space: "{space_name}"

Rules:
- Return ONLY the JSON array. No markdown. No backticks. No explanation.
- If nothing relevant is found, return exactly: []
- Skip greetings, logistics, and small talk.

MESSAGES:
{messages_text}"""

    # this is where the actual internet request to Google's AI servers happens.
    # everything before this line was just preparation
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    # get just the text part of the response object and remove any leading or trailing whitespace
    response_text = response.text.strip()

    # safety net: even though the prompt says "no markdown, no backticks", Gemini sometimes
    # wraps its answer in triple backticks anyway. this detects that and strips them out
    # so we are left with clean JSON. like opening an envelope you did not ask for
    if "```" in response_text:
        parts = response_text.split("```")
        response_text = parts[1] if len(parts) > 1 else parts[0]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    response_text = response_text.strip()

    try:
        # convert the text Gemini returned into a real Python list that the rest of the code can use
        return json.loads(response_text)
    except json.JSONDecodeError:
        # if Gemini returned something we cannot parse, print a warning and return an empty list.
        # this stops one bad response from crashing the entire pipeline
        print(f"  Could not parse response for {space_name}")
        print(f"  Raw: {response_text[:300]}")
        return []


def init_db():
    # open (or create if it does not exist yet) the database file
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            person_mentioned TEXT,
            summary TEXT,
            detail TEXT,
            confidence TEXT,
            source_space TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # "IF NOT EXISTS" on both tables means running the script multiple times
    # will not wipe existing data, it just skips creating them if they are already there
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            space_name TEXT,
            messages_processed INTEGER,
            knowledge_extracted INTEGER,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # save the table structure to disk
    conn.commit()

    # return the open connection so the rest of the script can keep writing to the database
    return conn


def store_knowledge(conn, items):
    # loop through every knowledge item Gemini extracted and write each one as a new row
    for item in items:
        conn.execute(
            """INSERT INTO knowledge
               (type, person_mentioned, summary, detail, confidence, source_space)
               VALUES (?, ?, ?, ?, ?, ?)""",
            # the question marks are safe placeholders. SQLite fills them in with the real values.
            # this prevents a security issue called SQL injection where malicious text in a message
            # could otherwise manipulate the database query itself
            (
                item.get("type"),
                item.get("person_mentioned"),
                item.get("summary"),
                item.get("detail"),
                item.get("confidence"),
                item.get("source_space"),
            ),
        )
    # save everything to disk once all items for this space are inserted
    conn.commit()


def run_pipeline():
    # the conductor function. calls all the other functions in the right order.
    # the print statements show you what is happening at each step so you can follow progress in the terminal
    print("Vallocate Brain - Ingestion Pipeline")
    print("=" * 45)

    print("\n1. Authenticating with Google...")
    creds = get_google_creds()
    # use those credentials to build an actual Google Chat connection object.
    # every API call to Google Chat after this point goes through chat_service
    chat_service = build("chat", "v1", credentials=creds)
    print("   Done.")

    print("\n2. Testing Gemini connection...")
    test = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents="Reply with just the word: ready"
    )
    print(f"   Gemini says: {test.text.strip()}")

    print("\n3. Setting up database...")
    conn = init_db()
    print(f"   Database ready: {DB_FILE}")

    print("\n4. Fetching Google Chat spaces...")
    spaces = fetch_all_spaces(chat_service)
    print(f"   Found {len(spaces)} spaces")

    total_knowledge = 0

    for space in spaces:
        space_name = space["name"]
        display_name = space.get("displayName", space_name)
        space_type = space.get("spaceType", "")

        print(f"\n   Processing: {display_name} ({space_type})")

        messages = fetch_messages(chat_service, space_name, max_messages=100)
        if not messages:
            print("   No messages found. Skipping.")
            continue

        print(f"   Fetched {len(messages)} messages")

        # Google returns each message as a complex dictionary with many fields.
        # we pull out only three things: who sent it, what they said, and when.
        # then format them into a readable block of text like "[2026-05-01] Sarah: Can we discuss the project?"
        # that block of text is what gets sent to Gemini
        messages_text = ""
        for msg in messages:
            sender = msg.get("sender", {}).get("displayName", "Unknown")
            text = msg.get("text", "")
            time = msg.get("createTime", "")
            if text.strip():
                messages_text += f"[{time}] {sender}: {text}\n"

        if not messages_text.strip():
            print("   No text content found. Skipping.")
            continue

        print("   Extracting knowledge via Gemini...")
        items = extract_knowledge(messages_text, display_name)
        print(f"   Extracted {len(items)} knowledge items")

        if items:
            store_knowledge(conn, items)
            total_knowledge += len(items)

        conn.execute(
            "INSERT INTO ingestion_log (space_name, messages_processed, knowledge_extracted) VALUES (?, ?, ?)",
            (display_name, len(messages), len(items)),
        )
        conn.commit()

    print(f"\n{'=' * 45}")
    print(f"Pipeline complete.")
    print(f"Total knowledge items extracted: {total_knowledge}")
    print(f"Stored in: {DB_FILE}")
    conn.close()


# only run the pipeline when this file is executed directly with "python company_brain.py".
# if another script imported this file as a module, the pipeline would NOT run automatically.
# this is a standard Python pattern to keep a file usable both as a script and as a module
if __name__ == "__main__":
    run_pipeline()
