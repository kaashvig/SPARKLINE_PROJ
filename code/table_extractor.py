import re

def extract_tables(sql_query: str) -> list:
    # List of known tables in the database
    known_tables = {"customers", "products", "sales", "employees"}
    
    # Extract words/tokens from the query
    tokens = set(re.findall(r'\b\w+\b', sql_query.lower()))
    
    # Match against known tables
    used_tables = list(known_tables.intersection(tokens))
    return sorted(used_tables)
