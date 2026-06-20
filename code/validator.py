import sqlite3
import os

def get_db_path():
    # Look for the SQLite database in standard locations
    if os.path.exists("sparkline_demo.db"):
        return "sparkline_demo.db"
    if os.path.exists("../sparkline_demo.db"):
        return "../sparkline_demo.db"
    return r"c:\Users\Admin\OneDrive\Desktop\LLM_Kaashvi_Gupta\sparkline_demo.db"

def validate_sql(sql_query: str):
    cleaned_query = sql_query.strip().strip(';').strip()
    
    # Force uppercase starting word validation
    if not cleaned_query.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")
        
    # Prevent multi-statement query injections
    if ";" in cleaned_query:
        statements = [s.strip() for s in cleaned_query.split(";") if s.strip()]
        if len(statements) > 1:
            raise ValueError("Multiple SQL statements are not allowed.")
            
    # Validate against SQLite schema using EXPLAIN command
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN {cleaned_query}")
    except sqlite3.Error as e:
        raise ValueError(f"SQL Validation Error: {str(e)}")
    finally:
        conn.close()
