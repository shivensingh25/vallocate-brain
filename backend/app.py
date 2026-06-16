import streamlit as st
import sqlite3
import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DB_FILE = "company_brain.db"
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# ==================== TOOL FUNCTIONS ====================
# These are the tools the agentic brain can call

def search_by_skill(skill: str) -> str:
    conn = get_db()
    rows = conn.execute(
        "SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type IN ('skill', 'performance') AND (summary LIKE ? OR detail LIKE ?) ORDER BY confidence DESC",
        (f"%{skill}%", f"%{skill}%"),
    ).fetchall()
    conn.close()
    if not rows:
        return json.dumps({"results": [], "message": f"No skill data found for '{skill}'"})
    results = [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]
    return json.dumps({"results": results})


def check_availability(start_date: str, end_date: str) -> str:
    conn = get_db()
    rows = conn.execute(
        "SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type = 'availability' ORDER BY confidence DESC",
    ).fetchall()
    conn.close()
    if not rows:
        return json.dumps({"results": [], "message": "No availability data found"})
    results = [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"]} for r in rows]
    return json.dumps({"results": results})


def get_project_history(person: str) -> str:
    conn = get_db()
    rows = conn.execute(
        "SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned LIKE ? AND type IN ('project', 'allocation') ORDER BY created_at DESC",
        (f"%{person}%",),
    ).fetchall()
    conn.close()
    if not rows:
        return json.dumps({"results": [], "message": f"No project history found for '{person}'"})
    results = [{"type": r["type"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]
    return json.dumps({"results": results})


def get_performance_signals(person: str) -> str:
    conn = get_db()
    rows = conn.execute(
        "SELECT summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned LIKE ? AND type IN ('performance', 'workload', 'preference') ORDER BY created_at DESC",
        (f"%{person}%",),
    ).fetchall()
    conn.close()
    if not rows:
        return json.dumps({"results": [], "message": f"No performance data found for '{person}'"})
    results = [{"summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]
    return json.dumps({"results": results})


def search_all_knowledge(query: str) -> str:
    conn = get_db()
    rows = conn.execute(
        "SELECT type, person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE summary LIKE ? OR detail LIKE ? ORDER BY confidence DESC LIMIT 20",
        (f"%{query}%", f"%{query}%"),
    ).fetchall()
    conn.close()
    if not rows:
        return json.dumps({"results": [], "message": f"No knowledge found for '{query}'"})
    results = [{"type": r["type"], "person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]
    return json.dumps({"results": results})


# Map function names to actual functions
TOOL_FUNCTIONS = {
    "search_by_skill": search_by_skill,
    "check_availability": check_availability,
    "get_project_history": get_project_history,
    "get_performance_signals": get_performance_signals,
    "search_all_knowledge": search_all_knowledge,
}


# ==================== AGENTIC REASONING ====================

def run_agent(question):
    """Run the agentic brain with tool use."""

    tool_declarations = [
        {
            "name": "search_by_skill",
            "description": "Search the company brain for consultants with a specific skill or domain experience",
            "parameters": {
                "type": "object",
                "properties": {"skill": {"type": "string", "description": "The skill or domain to search for"}},
                "required": ["skill"],
            },
        },
        {
            "name": "check_availability",
            "description": "Check which consultants are available in a date range",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date"},
                    "end_date": {"type": "string", "description": "End date"},
                },
                "required": ["start_date", "end_date"],
            },
        },
        {
            "name": "get_project_history",
            "description": "Get a consultant's past project assignments",
            "parameters": {
                "type": "object",
                "properties": {"person": {"type": "string", "description": "Consultant name"}},
                "required": ["person"],
            },
        },
        {
            "name": "get_performance_signals",
            "description": "Get performance, workload, and preference signals about a consultant",
            "parameters": {
                "type": "object",
                "properties": {"person": {"type": "string", "description": "Consultant name"}},
                "required": ["person"],
            },
        },
        {
            "name": "search_all_knowledge",
            "description": "General search across all knowledge in the brain",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search query"}},
                "required": ["query"],
            },
        },
    ]

    tools = types.Tool(function_declarations=tool_declarations)

    system_prompt = """You are the Vallocate Company Brain, an intelligent allocation assistant for a consulting firm.

When asked about consultants, projects, or allocation, use the available tools to search the knowledge base.
Call multiple tools if needed. Check skills, then availability, then performance.
Always explain your reasoning. If data is missing, say so rather than guessing.
After gathering enough information, provide a ranked recommendation with clear explanations."""

    messages = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]
    thinking_steps = []

    # Agentic loop: keep calling tools until Gemini gives a final answer
    for iteration in range(10):  # max 10 iterations to prevent infinite loops
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[tools],
                system_instruction=system_prompt,
            ),
        )

        # Check if Gemini wants to call tools
        has_function_call = False
        function_responses = []

        for part in response.candidates[0].content.parts:
            if part.function_call:
                has_function_call = True
                fn_name = part.function_call.name
                fn_args = dict(part.function_call.args) if part.function_call.args else {}

                thinking_steps.append(f"Calling: {fn_name}({fn_args})")

                # Execute the tool
                if fn_name in TOOL_FUNCTIONS:
                    result = TOOL_FUNCTIONS[fn_name](**fn_args)
                else:
                    result = json.dumps({"error": f"Unknown tool: {fn_name}"})

                function_responses.append(
                    types.Part.from_function_response(
                        name=fn_name,
                        response=json.loads(result),
                    )
                )

        if has_function_call:
            # Add Gemini's response (with function calls) to message history
            messages.append(response.candidates[0].content)
            # Add tool results to message history
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            # No more tool calls, Gemini has a final answer
            final_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    final_text += part.text
            return final_text, thinking_steps

    return "Agent reached maximum iterations without a final answer.", thinking_steps


# ==================== STREAMLIT UI ====================

st.set_page_config(page_title="Vallocate Brain", page_icon="🧠", layout="wide")
st.title("🧠 Vallocate Company Brain")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Dashboard", "Consultant Search", "Allocation Assistant", "Knowledge Feed"])

conn = get_db()

if page == "Dashboard":
    st.header("Brain Dashboard")

    # Overall stats
    total = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
    st.metric("Total knowledge items", total)

    # By source
    st.subheader("By source")
    source_rows = conn.execute(
        "SELECT source_space, COUNT(*) as count FROM knowledge GROUP BY source_space ORDER BY count DESC"
    ).fetchall()
    for row in source_rows:
        st.write(f"**{row['source_space']}**: {row['count']} items")

    # By type
    st.subheader("By type")
    type_rows = conn.execute(
        "SELECT type, COUNT(*) as count FROM knowledge GROUP BY type ORDER BY count DESC"
    ).fetchall()
    cols = st.columns(len(type_rows) if type_rows else 1)
    for i, row in enumerate(type_rows):
        cols[i % len(cols)].metric(row["type"], row["count"])

    # Last ingestion times
    st.subheader("Ingestion log")
    log_rows = conn.execute(
        "SELECT space_name, messages_processed, knowledge_extracted, timestamp FROM ingestion_log ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()
    for row in log_rows:
        st.write(f"**{row['space_name']}**: {row['messages_processed']} processed, {row['knowledge_extracted']} extracted — {row['timestamp']}")


elif page == "Consultant Search":
    st.header("Consultant Profile Search")
    name = st.text_input("Enter consultant name")

    if name:
        rows = conn.execute(
            "SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned LIKE ? ORDER BY type",
            (f"%{name}%",),
        ).fetchall()

        if rows:
            st.success(f"Found {len(rows)} knowledge items about {name}")
            current_type = ""
            for row in rows:
                if row["type"] != current_type:
                    current_type = row["type"]
                    st.subheader(current_type.upper())
                st.write(f"• {row['summary']}")
                if row["detail"]:
                    st.caption(f"Detail: {row['detail']}")
                st.caption(f"Confidence: {row['confidence']} | Source: {row['source_space']}")
        else:
            st.warning(f"No knowledge found about '{name}'")


elif page == "Allocation Assistant":
    st.header("Allocation Assistant")
    st.write("Enter a project brief and the brain will recommend consultants.")

    brief = st.text_area(
        "Project brief",
        placeholder="Example: 3-week banking project starting June 20, need financial modelling and stakeholder management skills, team of 2 consultants",
        height=100,
    )

    if st.button("Ask the brain", type="primary"):
        if brief:
            with st.spinner("Brain is thinking..."):
                thinking_container = st.container()
                answer, steps = run_agent(brief)

                # Show thinking steps
                if steps:
                    with thinking_container:
                        with st.expander("See brain reasoning steps", expanded=False):
                            for step in steps:
                                st.code(step)

                # Show final answer
                st.markdown("### Recommendation")
                st.markdown(answer)
        else:
            st.warning("Please enter a project brief first.")


elif page == "Knowledge Feed":
    st.header("Knowledge Feed")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        types_available = conn.execute("SELECT DISTINCT type FROM knowledge").fetchall()
        type_filter = st.selectbox("Filter by type", ["All"] + [r["type"] for r in types_available])
    with col2:
        sources_available = conn.execute("SELECT DISTINCT source_space FROM knowledge").fetchall()
        source_filter = st.selectbox("Filter by source", ["All"] + [r["source_space"] for r in sources_available])

    # Build query
    query = "SELECT type, person_mentioned, summary, detail, confidence, source_space, created_at FROM knowledge WHERE 1=1"
    params = []
    if type_filter != "All":
        query += " AND type = ?"
        params.append(type_filter)
    if source_filter != "All":
        query += " AND source_space = ?"
        params.append(source_filter)
    query += " ORDER BY created_at DESC"

    rows = conn.execute(query, params).fetchall()

    st.write(f"Showing {len(rows)} items")
    for row in rows:
        with st.container():
            st.write(f"**[{row['type']}]** {row['summary']}")
            meta = f"Person: {row['person_mentioned'] or 'N/A'} | Confidence: {row['confidence']} | Source: {row['source_space']}"
            st.caption(meta)
            st.divider()

conn.close()