# import streamlit as st
# # import sqlite3
# import db
# import json
# import os
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# load_dotenv()

# DB_FILE = "company_brain.db"
# client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# def get_db():
#     conn = sqlite3.connect(DB_FILE)
#     conn.row_factory = sqlite3.Row
#     return conn


# # ==================== TOOL FUNCTIONS ====================
# # These are the tools the agentic brain can call

# def search_by_skill(skill: str) -> str:
#     conn = get_db()
#     rows = conn.execute(
#         "SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type IN ('skill', 'performance') AND (summary LIKE ? OR detail LIKE ?) ORDER BY confidence DESC",
#         (f"%{skill}%", f"%{skill}%"),
#     ).fetchall()
#     conn.close()
#     if not rows:
#         return json.dumps({"results": [], "message": f"No skill data found for '{skill}'"})
#     results = [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# def check_availability(start_date: str, end_date: str) -> str:
#     conn = get_db()
#     rows = conn.execute(
#         "SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type = 'availability' ORDER BY confidence DESC",
#     ).fetchall()
#     conn.close()
#     if not rows:
#         return json.dumps({"results": [], "message": "No availability data found"})
#     results = [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"]} for r in rows]
#     return json.dumps({"results": results})


# def get_project_history(person: str) -> str:
#     conn = get_db()
#     rows = conn.execute(
#         "SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned LIKE ? AND type IN ('project', 'allocation') ORDER BY created_at DESC",
#         (f"%{person}%",),
#     ).fetchall()
#     conn.close()
#     if not rows:
#         return json.dumps({"results": [], "message": f"No project history found for '{person}'"})
#     results = [{"type": r["type"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# def get_performance_signals(person: str) -> str:
#     conn = get_db()
#     rows = conn.execute(
#         "SELECT summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned LIKE ? AND type IN ('performance', 'workload', 'preference') ORDER BY created_at DESC",
#         (f"%{person}%",),
#     ).fetchall()
#     conn.close()
#     if not rows:
#         return json.dumps({"results": [], "message": f"No performance data found for '{person}'"})
#     results = [{"summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# def search_all_knowledge(query: str) -> str:
#     conn = get_db()
#     rows = conn.execute(
#         "SELECT type, person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE summary LIKE ? OR detail LIKE ? ORDER BY confidence DESC LIMIT 20",
#         (f"%{query}%", f"%{query}%"),
#     ).fetchall()
#     conn.close()
#     if not rows:
#         return json.dumps({"results": [], "message": f"No knowledge found for '{query}'"})
#     results = [{"type": r["type"], "person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# # Map function names to actual functions
# TOOL_FUNCTIONS = {
#     "search_by_skill": search_by_skill,
#     "check_availability": check_availability,
#     "get_project_history": get_project_history,
#     "get_performance_signals": get_performance_signals,
#     "search_all_knowledge": search_all_knowledge,
# }


# # ==================== AGENTIC REASONING ====================

# def run_agent(question):
#     """Run the agentic brain with tool use."""

#     tool_declarations = [
#         {
#             "name": "search_by_skill",
#             "description": "Search the company brain for consultants with a specific skill or domain experience",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"skill": {"type": "string", "description": "The skill or domain to search for"}},
#                 "required": ["skill"],
#             },
#         },
#         {
#             "name": "check_availability",
#             "description": "Check which consultants are available in a date range",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "start_date": {"type": "string", "description": "Start date"},
#                     "end_date": {"type": "string", "description": "End date"},
#                 },
#                 "required": ["start_date", "end_date"],
#             },
#         },
#         {
#             "name": "get_project_history",
#             "description": "Get a consultant's past project assignments",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"person": {"type": "string", "description": "Consultant name"}},
#                 "required": ["person"],
#             },
#         },
#         {
#             "name": "get_performance_signals",
#             "description": "Get performance, workload, and preference signals about a consultant",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"person": {"type": "string", "description": "Consultant name"}},
#                 "required": ["person"],
#             },
#         },
#         {
#             "name": "search_all_knowledge",
#             "description": "General search across all knowledge in the brain",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"query": {"type": "string", "description": "Search query"}},
#                 "required": ["query"],
#             },
#         },
#     ]

#     tools = types.Tool(function_declarations=tool_declarations)

#     system_prompt = """You are the Vallocate Company Brain, an intelligent allocation assistant for a consulting firm.

# When asked about consultants, projects, or allocation, use the available tools to search the knowledge base.
# Call multiple tools if needed. Check skills, then availability, then performance.
# Always explain your reasoning. If data is missing, say so rather than guessing.
# After gathering enough information, provide a ranked recommendation with clear explanations."""

#     messages = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]
#     thinking_steps = []

#     # Agentic loop: keep calling tools until Gemini gives a final answer
#     for iteration in range(10):  # max 10 iterations to prevent infinite loops
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=messages,
#             config=types.GenerateContentConfig(
#                 tools=[tools],
#                 system_instruction=system_prompt,
#             ),
#         )

#         # Check if Gemini wants to call tools
#         has_function_call = False
#         function_responses = []

#         for part in response.candidates[0].content.parts:
#             if part.function_call:
#                 has_function_call = True
#                 fn_name = part.function_call.name
#                 fn_args = dict(part.function_call.args) if part.function_call.args else {}

#                 thinking_steps.append(f"Calling: {fn_name}({fn_args})")

#                 # Execute the tool
#                 if fn_name in TOOL_FUNCTIONS:
#                     result = TOOL_FUNCTIONS[fn_name](**fn_args)
#                 else:
#                     result = json.dumps({"error": f"Unknown tool: {fn_name}"})

#                 function_responses.append(
#                     types.Part.from_function_response(
#                         name=fn_name,
#                         response=json.loads(result),
#                     )
#                 )

#         if has_function_call:
#             # Add Gemini's response (with function calls) to message history
#             messages.append(response.candidates[0].content)
#             # Add tool results to message history
#             messages.append(types.Content(role="user", parts=function_responses))
#         else:
#             # No more tool calls, Gemini has a final answer
#             final_text = ""
#             for part in response.candidates[0].content.parts:
#                 if part.text:
#                     final_text += part.text
#             return final_text, thinking_steps

#     return "Agent reached maximum iterations without a final answer.", thinking_steps


# # ==================== STREAMLIT UI ====================

# st.set_page_config(page_title="Vallocate Brain", page_icon="🧠", layout="wide")
# st.title("🧠 Vallocate Company Brain")

# # Sidebar navigation
# page = st.sidebar.radio("Navigate", ["Dashboard", "Consultant Search", "Allocation Assistant", "Knowledge Feed"])

# conn = get_db()

# if page == "Dashboard":
#     st.header("Brain Dashboard")

#     # Overall stats
#     total = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
#     st.metric("Total knowledge items", total)

#     # By source
#     st.subheader("By source")
#     source_rows = conn.execute(
#         "SELECT source_space, COUNT(*) as count FROM knowledge GROUP BY source_space ORDER BY count DESC"
#     ).fetchall()
#     for row in source_rows:
#         st.write(f"**{row['source_space']}**: {row['count']} items")

#     # By type
#     st.subheader("By type")
#     type_rows = conn.execute(
#         "SELECT type, COUNT(*) as count FROM knowledge GROUP BY type ORDER BY count DESC"
#     ).fetchall()
#     cols = st.columns(len(type_rows) if type_rows else 1)
#     for i, row in enumerate(type_rows):
#         cols[i % len(cols)].metric(row["type"], row["count"])

#     # Last ingestion times
#     st.subheader("Ingestion log")
#     log_rows = conn.execute(
#         "SELECT space_name, messages_processed, knowledge_extracted, timestamp FROM ingestion_log ORDER BY timestamp DESC LIMIT 10"
#     ).fetchall()
#     for row in log_rows:
#         st.write(f"**{row['space_name']}**: {row['messages_processed']} processed, {row['knowledge_extracted']} extracted — {row['timestamp']}")


# elif page == "Consultant Search":
#     st.header("Consultant Profile Search")
#     name = st.text_input("Enter consultant name")

#     if name:
#         rows = conn.execute(
#             "SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned LIKE ? ORDER BY type",
#             (f"%{name}%",),
#         ).fetchall()

#         if rows:
#             st.success(f"Found {len(rows)} knowledge items about {name}")
#             current_type = ""
#             for row in rows:
#                 if row["type"] != current_type:
#                     current_type = row["type"]
#                     st.subheader(current_type.upper())
#                 st.write(f"• {row['summary']}")
#                 if row["detail"]:
#                     st.caption(f"Detail: {row['detail']}")
#                 st.caption(f"Confidence: {row['confidence']} | Source: {row['source_space']}")
#         else:
#             st.warning(f"No knowledge found about '{name}'")


# elif page == "Allocation Assistant":
#     st.header("Allocation Assistant")
#     st.write("Enter a project brief and the brain will recommend consultants.")

#     brief = st.text_area(
#         "Project brief",
#         placeholder="Example: 3-week banking project starting June 20, need financial modelling and stakeholder management skills, team of 2 consultants",
#         height=100,
#     )

#     if st.button("Ask the brain", type="primary"):
#         if brief:
#             with st.spinner("Brain is thinking..."):
#                 thinking_container = st.container()
#                 answer, steps = run_agent(brief)

#                 # Show thinking steps
#                 if steps:
#                     with thinking_container:
#                         with st.expander("See brain reasoning steps", expanded=False):
#                             for step in steps:
#                                 st.code(step)

#                 # Show final answer
#                 st.markdown("### Recommendation")
#                 st.markdown(answer)
#         else:
#             st.warning("Please enter a project brief first.")


# elif page == "Knowledge Feed":
#     st.header("Knowledge Feed")

#     # Filters
#     col1, col2 = st.columns(2)
#     with col1:
#         types_available = conn.execute("SELECT DISTINCT type FROM knowledge").fetchall()
#         type_filter = st.selectbox("Filter by type", ["All"] + [r["type"] for r in types_available])
#     with col2:
#         sources_available = conn.execute("SELECT DISTINCT source_space FROM knowledge").fetchall()
#         source_filter = st.selectbox("Filter by source", ["All"] + [r["source_space"] for r in sources_available])

#     # Build query
#     query = "SELECT type, person_mentioned, summary, detail, confidence, source_space, created_at FROM knowledge WHERE 1=1"
#     params = []
#     if type_filter != "All":
#         query += " AND type = ?"
#         params.append(type_filter)
#     if source_filter != "All":
#         query += " AND source_space = ?"
#         params.append(source_filter)
#     query += " ORDER BY created_at DESC"

#     rows = conn.execute(query, params).fetchall()

#     st.write(f"Showing {len(rows)} items")
#     for row in rows:
#         with st.container():
#             st.write(f"**[{row['type']}]** {row['summary']}")
#             meta = f"Person: {row['person_mentioned'] or 'N/A'} | Confidence: {row['confidence']} | Source: {row['source_space']}"
#             st.caption(meta)
#             st.divider()

# conn.close()

#----------------V2--------------------------------------------

# import streamlit as st
# import db
# import json
# import os
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# load_dotenv()

# client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# # ==================== TOOL FUNCTIONS ====================

# def search_by_skill(skill: str) -> str:
#     rows = db.query(
#         "SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type IN ('skill', 'performance') AND (summary ILIKE %s OR detail ILIKE %s) ORDER BY confidence DESC",
#         (f"%{skill}%", f"%{skill}%"),
#     )
#     if not rows:
#         return json.dumps({"results": [], "message": f"No skill data found for '{skill}'"})
#     results = [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# def check_availability(start_date: str, end_date: str) -> str:
#     rows = db.query(
#         "SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type = 'availability' ORDER BY confidence DESC"
#     )
#     if not rows:
#         return json.dumps({"results": [], "message": "No availability data found"})
#     results = [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"]} for r in rows]
#     return json.dumps({"results": results})


# def get_project_history(person: str) -> str:
#     rows = db.query(
#         "SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned ILIKE %s AND type IN ('project', 'allocation') ORDER BY created_at DESC",
#         (f"%{person}%",),
#     )
#     if not rows:
#         return json.dumps({"results": [], "message": f"No project history found for '{person}'"})
#     results = [{"type": r["type"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# def get_performance_signals(person: str) -> str:
#     rows = db.query(
#         "SELECT summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned ILIKE %s AND type IN ('performance', 'workload', 'preference') ORDER BY created_at DESC",
#         (f"%{person}%",),
#     )
#     if not rows:
#         return json.dumps({"results": [], "message": f"No performance data found for '{person}'"})
#     results = [{"summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# def search_all_knowledge(query_text: str) -> str:
#     rows = db.query(
#         "SELECT type, person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE summary ILIKE %s OR detail ILIKE %s ORDER BY confidence DESC LIMIT 20",
#         (f"%{query_text}%", f"%{query_text}%"),
#     )
#     if not rows:
#         return json.dumps({"results": [], "message": f"No knowledge found for '{query_text}'"})
#     results = [{"type": r["type"], "person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]
#     return json.dumps({"results": results})


# TOOL_FUNCTIONS = {
#     "search_by_skill": search_by_skill,
#     "check_availability": check_availability,
#     "get_project_history": get_project_history,
#     "get_performance_signals": get_performance_signals,
#     "search_all_knowledge": search_all_knowledge,
# }


# # ==================== AGENTIC REASONING ====================

# def run_agent(question):
#     tool_declarations = [
#         {
#             "name": "search_by_skill",
#             "description": "Search the company brain for consultants with a specific skill or domain experience",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"skill": {"type": "string", "description": "The skill or domain to search for"}},
#                 "required": ["skill"],
#             },
#         },
#         {
#             "name": "check_availability",
#             "description": "Check which consultants are available in a date range",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "start_date": {"type": "string", "description": "Start date"},
#                     "end_date": {"type": "string", "description": "End date"},
#                 },
#                 "required": ["start_date", "end_date"],
#             },
#         },
#         {
#             "name": "get_project_history",
#             "description": "Get a consultant's past project assignments",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"person": {"type": "string", "description": "Consultant name"}},
#                 "required": ["person"],
#             },
#         },
#         {
#             "name": "get_performance_signals",
#             "description": "Get performance, workload, and preference signals about a consultant",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"person": {"type": "string", "description": "Consultant name"}},
#                 "required": ["person"],
#             },
#         },
#         {
#             "name": "search_all_knowledge",
#             "description": "General search across all knowledge in the brain",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"query": {"type": "string", "description": "Search query"}},
#                 "required": ["query"],
#             },
#         },
#     ]

#     tools = types.Tool(function_declarations=tool_declarations)

#     system_prompt = """You are the Vallocate Company Brain, an intelligent allocation assistant for a consulting firm.

# When asked about consultants, projects, or allocation, use the available tools to search the knowledge base.
# Call multiple tools if needed. Check skills, then availability, then performance.
# Always explain your reasoning. If data is missing, say so rather than guessing.
# After gathering enough information, provide a ranked recommendation with clear explanations."""

#     messages = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]
#     thinking_steps = []

#     for iteration in range(10):
#         response = client.models.generate_content(
#             model="gemini-3.1-flash-lite",
#             contents=messages,
#             config=types.GenerateContentConfig(
#                 tools=[tools],
#                 system_instruction=system_prompt,
#             ),
#         )

#         has_function_call = False
#         function_responses = []

#         for part in response.candidates[0].content.parts:
#             if part.function_call:
#                 has_function_call = True
#                 fn_name = part.function_call.name
#                 fn_args = dict(part.function_call.args) if part.function_call.args else {}

#                 thinking_steps.append(f"Calling: {fn_name}({fn_args})")

#                 if fn_name in TOOL_FUNCTIONS:
#                     result = TOOL_FUNCTIONS[fn_name](**fn_args)
#                 else:
#                     result = json.dumps({"error": f"Unknown tool: {fn_name}"})

#                 function_responses.append(
#                     types.Part.from_function_response(
#                         name=fn_name,
#                         response=json.loads(result),
#                     )
#                 )

#         if has_function_call:
#             messages.append(response.candidates[0].content)
#             messages.append(types.Content(role="user", parts=function_responses))
#         else:
#             final_text = ""
#             for part in response.candidates[0].content.parts:
#                 if part.text:
#                     final_text += part.text
#             return final_text, thinking_steps

#     return "Agent reached maximum iterations without a final answer.", thinking_steps


# # ==================== STREAMLIT UI ====================

# st.set_page_config(page_title="Vallocate Brain", page_icon="🧠", layout="wide")
# st.title("🧠 Vallocate Company Brain")

# page = st.sidebar.radio("Navigate", ["Dashboard", "Consultant Search", "Allocation Assistant", "Knowledge Feed"])

# if page == "Dashboard":
#     st.header("Brain Dashboard")

#     total = db.query("SELECT COUNT(*) as count FROM knowledge")[0]["count"]
#     st.metric("Total knowledge items", total)

#     st.subheader("By source")
#     source_rows = db.query(
#         "SELECT source_space, COUNT(*) as count FROM knowledge GROUP BY source_space ORDER BY count DESC"
#     )
#     for row in source_rows:
#         st.write(f"**{row['source_space']}**: {row['count']} items")

#     st.subheader("By type")
#     type_rows = db.query(
#         "SELECT type, COUNT(*) as count FROM knowledge GROUP BY type ORDER BY count DESC"
#     )
#     if type_rows:
#         cols = st.columns(len(type_rows))
#         for i, row in enumerate(type_rows):
#             cols[i % len(cols)].metric(row["type"], row["count"])

#     st.subheader("Ingestion log")
#     log_rows = db.query(
#         "SELECT space_name, messages_processed, knowledge_extracted, timestamp FROM ingestion_log ORDER BY timestamp DESC LIMIT 10"
#     )
#     for row in log_rows:
#         st.write(f"**{row['space_name']}**: {row['messages_processed']} processed, {row['knowledge_extracted']} extracted")


# elif page == "Consultant Search":
#     st.header("Consultant Profile Search")
#     name = st.text_input("Enter consultant name")

#     if name:
#         # Show synthesized profile if available
#         profile_rows = db.query(
#             "SELECT profile_json FROM consultant_profiles WHERE consultant_name ILIKE %s ORDER BY last_updated DESC LIMIT 1",
#             (f"%{name}%",),
#         )

#         if profile_rows:
#             profile = json.loads(profile_rows[0]["profile_json"])
#             st.success(f"Unified profile for {profile.get('name', name)}")

#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("Skills")
#                 for skill in profile.get("skills", []):
#                     st.write(f"* {skill}")
#                 st.subheader("Domains")
#                 for domain in profile.get("domains", []):
#                     st.write(f"* {domain}")
#             with col2:
#                 st.subheader("Current status")
#                 st.write(profile.get("current_status", "Unknown"))
#                 st.subheader("Preferences")
#                 for pref in profile.get("preferences", []):
#                     st.write(f"* {pref}")

#             if profile.get("workload_signals"):
#                 st.subheader("Workload signals")
#                 for signal in profile["workload_signals"]:
#                     st.write(f"* {signal}")

#             if profile.get("performance_notes"):
#                 st.subheader("Performance notes")
#                 for note in profile["performance_notes"]:
#                     st.write(f"* {note}")

#             st.caption(f"Confidence: {profile.get('confidence_note', 'N/A')}")
#             st.divider()

#         # Show raw knowledge items
#         rows = db.query(
#             "SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned ILIKE %s ORDER BY type",
#             (f"%{name}%",),
#         )

#         if rows:
#             st.info(f"Found {len(rows)} raw knowledge items about {name}")
#             current_type = ""
#             for row in rows:
#                 if row["type"] != current_type:
#                     current_type = row["type"]
#                     st.subheader(current_type.upper())
#                 st.write(f"* {row['summary']}")
#                 if row["detail"]:
#                     st.caption(f"Detail: {row['detail']}")
#                 st.caption(f"Confidence: {row['confidence']} | Source: {row['source_space']}")
#         elif not profile_rows:
#             st.warning(f"No knowledge found about '{name}'")


# elif page == "Allocation Assistant":
#     st.header("Allocation Assistant")
#     st.write("Enter a project brief and the brain will recommend consultants.")

#     brief = st.text_area(
#         "Project brief",
#         placeholder="Example: 3-week banking project starting June 20, need financial modelling and stakeholder management skills, team of 2 consultants",
#         height=100,
#     )

#     if st.button("Ask the brain", type="primary"):
#         if brief:
#             with st.spinner("Brain is thinking..."):
#                 thinking_container = st.container()
#                 answer, steps = run_agent(brief)

#                 if steps:
#                     with thinking_container:
#                         with st.expander("See brain reasoning steps", expanded=False):
#                             for step in steps:
#                                 st.code(step)

#                 st.markdown("### Recommendation")
#                 st.markdown(answer)
#         else:
#             st.warning("Please enter a project brief first.")


# elif page == "Knowledge Feed":
#     st.header("Knowledge Feed")

#     col1, col2 = st.columns(2)
#     with col1:
#         types_available = db.query("SELECT DISTINCT type FROM knowledge")
#         type_filter = st.selectbox("Filter by type", ["All"] + [r["type"] for r in types_available])
#     with col2:
#         sources_available = db.query("SELECT DISTINCT source_space FROM knowledge")
#         source_filter = st.selectbox("Filter by source", ["All"] + [r["source_space"] for r in sources_available])

#     query_sql = "SELECT type, person_mentioned, summary, detail, confidence, source_space, created_at FROM knowledge WHERE 1=1"
#     params = []
#     if type_filter != "All":
#         query_sql += " AND type = %s"
#         params.append(type_filter)
#     if source_filter != "All":
#         query_sql += " AND source_space = %s"
#         params.append(source_filter)
#     query_sql += " ORDER BY created_at DESC"

#     rows = db.query(query_sql, tuple(params) if params else None)

#     st.write(f"Showing {len(rows)} items")
#     for row in rows:
#         with st.container():
#             st.write(f"**[{row['type']}]** {row['summary']}")
#             meta = f"Person: {row['person_mentioned'] or 'N/A'} | Confidence: {row['confidence']} | Source: {row['source_space']}"
#             st.caption(meta)
#             st.divider()



import streamlit as st
import db
import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# load_dotenv()

# client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# ==================== CUSTOM CSS ====================

st.set_page_config(
    page_title="Vallocate Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
try:
    import streamlit as st
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_KEY)



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }

[data-testid="stSidebar"] { background-color: #00363D; border-right: none; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label { color: #F7F3F5 !important; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    color: #F7F3F5 !important;
    font-size: 0.95rem;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
}

.page-title { font-size: 1.6rem; font-weight: 600; color: #00363D; margin-bottom: 0.25rem; letter-spacing: -0.02em; }
.page-subtitle { font-size: 0.9rem; color: #939196; margin-bottom: 1.75rem; }
.section-divider { border: none; border-top: 1.5px solid #F0EDF1; margin: 1.5rem 0; }

.stat-card { background: #fff; border: 1px solid #EBE8EC; border-radius: 10px; padding: 1.1rem 1.4rem; }
.stat-value { font-size: 2rem; font-weight: 600; color: #00363D; line-height: 1.1; }
.stat-label { font-size: 0.75rem; color: #939196; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.25rem; font-weight: 500; }

.source-row { display: flex; align-items: center; justify-content: space-between; padding: 0.65rem 0; border-bottom: 1px solid #F0EDF1; }
.source-row:last-child { border-bottom: none; }
.source-name { font-size: 0.9rem; color: #0F515C; font-weight: 500; }
.source-count { background: #E8F5F3; color: #00A189; font-size: 0.78rem; font-weight: 600; padding: 0.2rem 0.65rem; border-radius: 20px; }

.badge { display: inline-block; font-size: 0.72rem; font-weight: 600; padding: 0.18rem 0.6rem; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; margin-right: 0.35rem; }
.badge-skill      { background: #E8F5F3; color: #0C7878; }
.badge-project    { background: #EAF0FB; color: #1A5CA8; }
.badge-allocation { background: #FEF3E2; color: #9A5A00; }
.badge-performance{ background: #F3E8F8; color: #7A2D9A; }
.badge-availability{background: #E8F5ED; color: #1A7A3A; }
.badge-preference { background: #FDEEED; color: #A02020; }
.badge-decision   { background: #F5F0E8; color: #7A5A00; }
.badge-workload   { background: #FDE8F2; color: #9A1A5A; }
.badge-client     { background: #E8EEF5; color: #1A4A7A; }
.badge-default    { background: #F0EDF1; color: #939196; }

.knowledge-card { background: #fff; border: 1px solid #EBE8EC; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 0.65rem; transition: border-color 0.15s; }
.knowledge-card:hover { border-color: #0C7878; }
.knowledge-summary { font-size: 0.92rem; color: #1a1a1a; margin: 0.3rem 0; line-height: 1.5; }
.knowledge-detail  { font-size: 0.82rem; color: #939196; margin-top: 0.25rem; }
.knowledge-meta    { font-size: 0.78rem; color: #C0BDC1; margin-top: 0.5rem; }

.profile-card { background: linear-gradient(135deg, #00363D 0%, #0F515C 100%); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.25rem; }
.profile-name  { font-size: 1.4rem; font-weight: 600; color: #fff; margin-bottom: 0.25rem; }
.profile-status{ font-size: 0.88rem; color: #A9FDAC; margin-bottom: 1rem; }
.profile-section-title { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #A9FDAC; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem; }
.skill-chip { display: inline-block; background: rgba(169,253,172,0.15); color: #A9FDAC; border: 1px solid rgba(169,253,172,0.3); border-radius: 20px; font-size: 0.8rem; padding: 0.2rem 0.65rem; margin: 0.15rem; }

.thinking-step { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.5rem 0; border-bottom: 1px solid #F0EDF1; }
.thinking-step:last-child { border-bottom: none; }
.thinking-dot  { width: 8px; height: 8px; min-width: 8px; border-radius: 50%; background: #00A189; margin-top: 0.35rem; }
.thinking-text { font-size: 0.85rem; color: #0F515C; font-family: monospace; }

[data-testid="stTextInput"] input { border: 1.5px solid #EBE8EC; border-radius: 8px; }
[data-testid="stTextInput"] input:focus { border-color: #00A189; box-shadow: 0 0 0 3px rgba(0,161,137,0.1); }
[data-testid="stTextArea"] textarea { border: 1.5px solid #EBE8EC; border-radius: 8px; }
[data-testid="stTextArea"] textarea:focus { border-color: #00A189; }

.stButton > button[kind="primary"] { background-color: #00A189; border: none; border-radius: 8px; color: white; font-weight: 500; transition: background 0.15s; }
.stButton > button[kind="primary"]:hover { background-color: #0C7878; }
.stButton > button { border-color: #EBE8EC; border-radius: 8px; }

.log-row { display: flex; align-items: center; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid #F0EDF1; gap: 1rem; }
.log-row:last-child { border-bottom: none; }
.log-source    { font-size: 0.88rem; color: #0F515C; font-weight: 500; flex: 1; }
.log-processed { font-size: 0.82rem; color: #939196; }
.log-extracted { font-size: 0.82rem; font-weight: 600; color: #00A189; }

.section-box       { background: #fff; border: 1px solid #EBE8EC; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.25rem; }
.section-box-title { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #939196; font-weight: 600; margin-bottom: 0.75rem; }

.answer-box { background: #F7FFFE; border: 1.5px solid #A9FDAC; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; }
.conf-high   { color: #1A7A3A; font-weight: 600; }
.conf-medium { color: #9A5A00; font-weight: 600; }
.conf-low    { color: #939196; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ==================== HELPERS ====================

BADGE_CLASSES = {
    "skill": "badge-skill", "project": "badge-project", "allocation": "badge-allocation",
    "performance": "badge-performance", "availability": "badge-availability",
    "preference": "badge-preference", "decision": "badge-decision",
    "workload": "badge-workload", "client": "badge-client",
}

def badge(type_str):
    cls = BADGE_CLASSES.get(type_str, "badge-default")
    return f'<span class="badge {cls}">{type_str}</span>'

def confidence_html(c):
    cls = {"high": "conf-high", "medium": "conf-medium", "low": "conf-low"}.get(c, "")
    return f'<span class="{cls}">{c or "?"}</span>'

def render_knowledge_card(row):
    b = badge(row.get("type", ""))
    conf = confidence_html(row.get("confidence", ""))
    source = row.get("source_space", "")
    person = row.get("person_mentioned") or ""
    detail = row.get("detail") or ""
    summary = row.get("summary") or ""
    person_str = f" · {person}" if person else ""
    detail_str = f'<div class="knowledge-detail">{detail}</div>' if detail else ""
    st.markdown(f"""
    <div class="knowledge-card">
        {b}
        <div class="knowledge-summary">{summary}</div>
        {detail_str}
        <div class="knowledge-meta">{conf} confidence{person_str} · {source}</div>
    </div>
    """, unsafe_allow_html=True)


# ==================== TOOL FUNCTIONS ====================

def search_by_skill(skill: str) -> str:
    rows = db.query(
        "SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type IN ('skill', 'performance') AND (summary ILIKE %s OR detail ILIKE %s) ORDER BY confidence DESC",
        (f"%{skill}%", f"%{skill}%"),
    )
    if not rows:
        return json.dumps({"results": [], "message": f"No skill data found for '{skill}'"})
    return json.dumps({"results": [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]})

def check_availability(start_date: str, end_date: str) -> str:
    rows = db.query("SELECT person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE type = 'availability' ORDER BY confidence DESC")
    if not rows:
        return json.dumps({"results": [], "message": "No availability data found"})
    return json.dumps({"results": [{"person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"]} for r in rows]})

def get_project_history(person: str) -> str:
    rows = db.query(
        "SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned ILIKE %s AND type IN ('project', 'allocation') ORDER BY created_at DESC",
        (f"%{person}%",),
    )
    if not rows:
        return json.dumps({"results": [], "message": f"No project history found for '{person}'"})
    return json.dumps({"results": [{"type": r["type"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]})

def get_performance_signals(person: str) -> str:
    rows = db.query(
        "SELECT summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned ILIKE %s AND type IN ('performance', 'workload', 'preference') ORDER BY created_at DESC",
        (f"%{person}%",),
    )
    if not rows:
        return json.dumps({"results": [], "message": f"No performance data found for '{person}'"})
    return json.dumps({"results": [{"summary": r["summary"], "detail": r["detail"], "confidence": r["confidence"], "source": r["source_space"]} for r in rows]})

def search_all_knowledge(query: str) -> str:
    rows = db.query(
        "SELECT type, person_mentioned, summary, detail, confidence, source_space FROM knowledge WHERE summary ILIKE %s OR detail ILIKE %s ORDER BY confidence DESC LIMIT 20",
        (f"%{query}%", f"%{query}%"),
    )
    if not rows:
        return json.dumps({"results": [], "message": f"No knowledge found for '{query}'"})
    return json.dumps({"results": [{"type": r["type"], "person": r["person_mentioned"], "summary": r["summary"], "detail": r["detail"], "source": r["source_space"]} for r in rows]})

TOOL_FUNCTIONS = {
    "search_by_skill": search_by_skill,
    "check_availability": check_availability,
    "get_project_history": get_project_history,
    "get_performance_signals": get_performance_signals,
    "search_all_knowledge": search_all_knowledge,
}


# ==================== AGENTIC REASONING ====================

def run_agent(question):
    tool_declarations = [
        {"name": "search_by_skill", "description": "Search for consultants with a specific skill or domain", "parameters": {"type": "object", "properties": {"skill": {"type": "string"}}, "required": ["skill"]}},
        {"name": "check_availability", "description": "Check consultant availability in a date range", "parameters": {"type": "object", "properties": {"start_date": {"type": "string"}, "end_date": {"type": "string"}}, "required": ["start_date", "end_date"]}},
        {"name": "get_project_history", "description": "Get a consultant's past project assignments", "parameters": {"type": "object", "properties": {"person": {"type": "string"}}, "required": ["person"]}},
        {"name": "get_performance_signals", "description": "Get performance, workload, and preference signals", "parameters": {"type": "object", "properties": {"person": {"type": "string"}}, "required": ["person"]}},
        {"name": "search_all_knowledge", "description": "General search across all knowledge in the brain", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    ]
    tools = types.Tool(function_declarations=tool_declarations)
    system_prompt = """You are the Vallocate Company Brain, an intelligent allocation assistant for a consulting firm.
Use tools to search the knowledge base. Check skills, availability, then performance.
Provide a ranked recommendation with clear, concise explanations. If data is missing, say so."""

    messages = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]
    thinking_steps = []

    for _ in range(10):
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=messages,
            config=types.GenerateContentConfig(tools=[tools], system_instruction=system_prompt),
        )
        has_function_call = False
        function_responses = []
        for part in response.candidates[0].content.parts:
            if part.function_call:
                has_function_call = True
                fn_name = part.function_call.name
                fn_args = dict(part.function_call.args) if part.function_call.args else {}
                thinking_steps.append(f"{fn_name}({json.dumps(fn_args)})")
                result = TOOL_FUNCTIONS[fn_name](**fn_args) if fn_name in TOOL_FUNCTIONS else json.dumps({"error": f"Unknown: {fn_name}"})
                function_responses.append(types.Part.from_function_response(name=fn_name, response=json.loads(result)))
        if has_function_call:
            messages.append(response.candidates[0].content)
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            final_text = "".join(p.text for p in response.candidates[0].content.parts if p.text)
            return final_text, thinking_steps
    return "Agent reached maximum iterations.", thinking_steps


# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem; border-bottom: 1px solid rgba(169,253,172,0.2); margin-bottom: 1.5rem;">
        <div style="font-size:1.1rem;font-weight:600;color:#F7F3F5;letter-spacing:-0.01em;">Vallocate Brain</div>
        <div style="font-size:0.72rem;color:rgba(169,253,172,0.7);text-transform:uppercase;letter-spacing:0.1em;margin-top:0.15rem;">Company Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", ["Dashboard", "Consultant Search", "Allocation Assistant", "Knowledge Feed"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    try:
        total = db.query("SELECT COUNT(*) as count FROM knowledge")[0]["count"]
        sources = db.query("SELECT COUNT(DISTINCT source_space) as c FROM knowledge")[0]["c"]
        st.markdown(f"""
        <div style="padding:1rem;background:rgba(169,253,172,0.08);border-radius:8px;border:1px solid rgba(169,253,172,0.2);">
            <div style="font-size:0.7rem;color:rgba(169,253,172,0.7);text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:0.4rem;">Brain status</div>
            <div style="font-size:1.6rem;font-weight:600;color:#A9FDAC;line-height:1.1;">{total:,}</div>
            <div style="font-size:0.78rem;color:rgba(247,243,245,0.6);margin-top:0.1rem;">items · {sources} sources</div>
        </div>
        """, unsafe_allow_html=True)
    except:
        pass


# ==================== PAGES ====================

if page == "Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Overview of all knowledge extracted from your connected sources.</div>', unsafe_allow_html=True)
    try:
        total = db.query("SELECT COUNT(*) as count FROM knowledge")[0]["count"]
        type_rows = db.query("SELECT type, COUNT(*) as count FROM knowledge GROUP BY type ORDER BY count DESC")
        source_rows = db.query("SELECT source_space, COUNT(*) as count FROM knowledge GROUP BY source_space ORDER BY count DESC")
        log_rows = db.query("SELECT space_name, messages_processed, knowledge_extracted, timestamp FROM ingestion_log ORDER BY timestamp DESC LIMIT 8")

        cols = st.columns([1.5] + [1] * min(len(type_rows), 4))
        with cols[0]:
            st.markdown(f'<div class="stat-card" style="border-top:3px solid #00A189;"><div class="stat-value">{total:,}</div><div class="stat-label">Total items</div></div>', unsafe_allow_html=True)
        for i, row in enumerate(type_rows[:4]):
            with cols[i + 1]:
                st.markdown(f'<div class="stat-card" style="border-top:3px solid #0C7878;"><div class="stat-value">{row["count"]}</div><div class="stat-label">{row["type"]}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_left, col_right = st.columns(2)

        with col_left:
            source_html = "".join(f'<div class="source-row"><span class="source-name">{r["source_space"]}</span><span class="source-count">{r["count"]}</span></div>' for r in source_rows)
            st.markdown(f'<div class="section-box"><div class="section-box-title">Knowledge by source</div>{source_html}</div>', unsafe_allow_html=True)

        with col_right:
            log_html = "".join(f'<div class="log-row"><span class="log-source">{r["space_name"]}</span><span class="log-processed">{r["messages_processed"]} processed</span><span class="log-extracted">{r["knowledge_extracted"]} extracted</span></div>' for r in log_rows)
            st.markdown(f'<div class="section-box"><div class="section-box-title">Ingestion history</div>{log_html}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load dashboard: {e}")


elif page == "Consultant Search":
    st.markdown('<div class="page-title">Consultant Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Search for everything the brain knows about a consultant across all sources.</div>', unsafe_allow_html=True)
    name = st.text_input("Consultant name", placeholder="e.g. Sarah, James, Karina...", label_visibility="collapsed")

    if name:
        profile_rows = db.query("SELECT profile_json FROM consultant_profiles WHERE consultant_name ILIKE %s ORDER BY last_updated DESC LIMIT 1", (f"%{name}%",))
        if profile_rows:
            profile = json.loads(profile_rows[0]["profile_json"])
            skills_html = "".join(f'<span class="skill-chip">{s}</span>' for s in profile.get("skills", []))
            domains_html = "".join(f'<span class="skill-chip">{d}</span>' for d in profile.get("domains", []))
            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-name">{profile.get("name", name)}</div>
                <div class="profile-status">{profile.get("current_status", "")}</div>
                <div class="profile-section-title">Skills</div><div>{skills_html}</div>
                <div class="profile-section-title">Domains</div><div>{domains_html}</div>
            </div>
            """, unsafe_allow_html=True)

            prefs = profile.get("preferences", [])
            workload = profile.get("workload_signals", [])
            perf = profile.get("performance_notes", [])
            if prefs or workload or perf:
                p1, p2, p3 = st.columns(3)
                def mini_section(col, title, items):
                    if items:
                        with col:
                            rows_html = "".join(f'<div style="font-size:0.88rem;color:#1a1a1a;padding:0.2rem 0;border-bottom:1px solid #F0EDF1;">{i}</div>' for i in items)
                            st.markdown(f'<div class="section-box"><div class="section-box-title">{title}</div>{rows_html}</div>', unsafe_allow_html=True)
                mini_section(p1, "Preferences", prefs)
                mini_section(p2, "Workload", workload)
                mini_section(p3, "Performance", perf)
            if profile.get("confidence_note"):
                st.caption(f"Profile confidence: {profile['confidence_note']}")
            st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

        rows = db.query("SELECT type, summary, detail, confidence, source_space FROM knowledge WHERE person_mentioned ILIKE %s ORDER BY type, confidence DESC", (f"%{name}%",))
        if rows:
            st.markdown(f'<div style="font-size:0.85rem;color:#939196;margin-bottom:1rem;">{len(rows)} raw knowledge items</div>', unsafe_allow_html=True)
            type_groups = {}
            for row in rows:
                type_groups.setdefault(row.get("type", "other"), []).append(row)
            for type_key, items in type_groups.items():
                st.markdown(f'<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#939196;font-weight:600;margin:1rem 0 0.5rem;">{type_key}</div>', unsafe_allow_html=True)
                for item in items:
                    render_knowledge_card(item)
        elif not profile_rows:
            st.markdown('<div style="text-align:center;padding:3rem;color:#939196;"><div style="font-size:2rem;margin-bottom:0.5rem;">🔍</div><div style="font-weight:500;color:#0F515C;">No results found</div><div style="font-size:0.88rem;margin-top:0.25rem;">Try a different name or run the ingestion pipeline first.</div></div>', unsafe_allow_html=True)


elif page == "Allocation Assistant":
    st.markdown('<div class="page-title">Allocation Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Describe a project brief. The brain reasons across all sources to recommend the best consultants.</div>', unsafe_allow_html=True)
    brief = st.text_area("Project brief", placeholder="e.g. 3-week banking project starting June 20, need financial modelling and stakeholder management, team of 2", height=110, label_visibility="collapsed")

    col_btn, col_hint = st.columns([1, 4])
    with col_btn:
        submit = st.button("Ask the brain", type="primary", use_container_width=True)
    with col_hint:
        st.markdown('<div style="padding-top:0.6rem;font-size:0.82rem;color:#939196;">Include: skills needed, start date, project type, team size</div>', unsafe_allow_html=True)

    if submit:
        if not brief.strip():
            st.warning("Please enter a project brief first.")
        else:
            with st.spinner("Reasoning across all sources..."):
                answer, steps = run_agent(brief)
            if steps:
                with st.expander(f"Reasoning trace — {len(steps)} tool calls", expanded=False):
                    steps_html = "".join(f'<div class="thinking-step"><div class="thinking-dot"></div><div class="thinking-text">{s}</div></div>' for s in steps)
                    st.markdown(f'<div style="padding:0.5rem 0;">{steps_html}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer-box"><div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#0C7878;font-weight:600;margin-bottom:0.75rem;">Recommendation</div><div style="font-size:0.95rem;color:#1a1a1a;line-height:1.7;">{answer}</div></div>', unsafe_allow_html=True)


elif page == "Knowledge Feed":
    st.markdown('<div class="page-title">Knowledge Feed</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Browse all extracted knowledge items. Filter by type, source, or confidence.</div>', unsafe_allow_html=True)
    try:
        types_available = db.query("SELECT DISTINCT type FROM knowledge ORDER BY type")
        sources_available = db.query("SELECT DISTINCT source_space FROM knowledge ORDER BY source_space")
        col1, col2, col3 = st.columns(3)
        with col1:
            type_filter = st.selectbox("Type", ["All types"] + [r["type"] for r in types_available])
        with col2:
            source_filter = st.selectbox("Source", ["All sources"] + [r["source_space"] for r in sources_available])
        with col3:
            conf_filter = st.selectbox("Confidence", ["Any confidence", "high", "medium", "low"])

        query_sql = "SELECT type, person_mentioned, summary, detail, confidence, source_space, created_at FROM knowledge WHERE 1=1"
        params = []
        if type_filter != "All types":
            query_sql += " AND type = %s"; params.append(type_filter)
        if source_filter != "All sources":
            query_sql += " AND source_space = %s"; params.append(source_filter)
        if conf_filter != "Any confidence":
            query_sql += " AND confidence = %s"; params.append(conf_filter)
        query_sql += " ORDER BY created_at DESC"

        rows = db.query(query_sql, tuple(params) if params else None)
        st.markdown(f'<div style="font-size:0.85rem;color:#939196;margin:0.75rem 0 1rem;">{len(rows)} items</div>', unsafe_allow_html=True)
        if not rows:
            st.markdown('<div style="text-align:center;padding:3rem;color:#939196;"><div style="font-size:2rem;margin-bottom:0.5rem;">📭</div><div style="font-weight:500;color:#0F515C;">No items match your filters</div></div>', unsafe_allow_html=True)
        else:
            for row in rows:
                render_knowledge_card(row)
    except Exception as e:
        st.error(f"Could not load knowledge feed: {e}")
