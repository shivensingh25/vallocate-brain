# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.environ["DATABASE_URL"]


# def get_conn():
#     """Get a database connection."""
#     return psycopg2.connect(DATABASE_URL)


# def get_dict_conn():
#     """Get a connection that returns rows as dictionaries (like sqlite3.Row)."""
#     conn = psycopg2.connect(DATABASE_URL)
#     conn.autocommit = False
#     return conn


# def query(sql, params=None):
#     """Run a SELECT query and return all rows as dictionaries."""
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute(sql, params or ())
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return rows


# def execute(sql, params=None):
#     """Run an INSERT/UPDATE/DELETE query."""
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor()
#     cur.execute(sql, params or ())
#     conn.commit()
#     cur.close()
#     conn.close()


# def execute_many(sql, params_list):
#     """Run the same query with multiple sets of parameters."""
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor()
#     for params in params_list:
#         cur.execute(sql, params)
#     conn.commit()
#     cur.close()
#     conn.close()



import os
import psycopg2
from psycopg2.extras import RealDictCursor

# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.environ["DATABASE_URL"]

try:
    import streamlit as st
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_URL = os.environ["DATABASE_URL"]



def get_conn():
    """Get a database connection."""
    return psycopg2.connect(DATABASE_URL)


def query(sql, params=None):
    """Run a SELECT query and return all rows as dictionaries."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def execute(sql, params=None):
    """Run an INSERT/UPDATE/DELETE query."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    cur.close()
    conn.close()
