import sqlite3
import os

def get_db_path():
    # Look for the SQLite database in standard locations
    if os.path.exists("sparkline_demo.db"):
        return "sparkline_demo.db"
    if os.path.exists("../sparkline_demo.db"):
        return "../sparkline_demo.db"
    return r"c:\Users\Admin\OneDrive\Desktop\LLM_Kaashvi_Gupta\sparkline_demo.db"

def get_schema() -> str:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Retrieve all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = ""
    for table in tables:
        table_name = table[0]
        # Retrieve column info for each table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        schema += f"\nTable: {table_name}\n"
        for col in columns:
            schema += f"- {col[1]} ({col[2]})\n"
            
    conn.close()
    return schema
