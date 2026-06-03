import sqlite3

conn = sqlite3.connect("company_brain.db")
conn.row_factory = sqlite3.Row

print("=== Knowledge breakdown ===")
rows = conn.execute(
    "SELECT type, COUNT(*) as count FROM knowledge GROUP BY type ORDER BY count DESC"
).fetchall()
for row in rows:
    print(f"  {row['type']}: {row['count']} items")

print("\n=== All knowledge items ===")
rows = conn.execute(
    "SELECT type, person_mentioned, summary, confidence, source_space FROM knowledge ORDER BY type"
).fetchall()
for row in rows:
    print(f"\n[{row['type']}] Person: {row['person_mentioned'] or 'N/A'}")
    print(f"  Summary: {row['summary']}")
    print(f"  Confidence: {row['confidence']}")
    print(f"  Source: {row['source_space']}")

print("\n=== Ingestion log ===")
rows = conn.execute(
    "SELECT space_name, messages_processed, knowledge_extracted, timestamp FROM ingestion_log"
).fetchall()
for row in rows:
    print(f"  {row['space_name']}: {row['messages_processed']} messages, {row['knowledge_extracted']} items extracted")

conn.close()