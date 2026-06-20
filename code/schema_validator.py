def validate_schema_relevance(tables_used):

    if not tables_used:
        return False

    known_tables = {
        "customers",
        "sales",
        "employees",
        "products"
    }

    return any(
        table.lower() in known_tables
        for table in tables_used
    )