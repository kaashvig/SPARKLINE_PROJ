import sqlite3
import os

def get_db_path():
    # Look for the SQLite database in standard locations
    if os.path.exists("sparkline_demo.db"):
        return "sparkline_demo.db"
    if os.path.exists("../sparkline_demo.db"):
        return "../sparkline_demo.db"
    return r"c:\Users\Admin\OneDrive\Desktop\LLM_Kaashvi_Gupta\sparkline_demo.db"

def execute_query(sql_query: str) -> list:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    # Row factory allows fetching rows as dictionary-like objects
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        return result
    except sqlite3.Error as e:
        raise ValueError(f"Database execution error: {str(e)}")
    finally:
        conn.close()
