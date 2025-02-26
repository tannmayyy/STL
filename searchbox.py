import re

def modify_sql_query(query):
    if not query or not isinstance(query, str):
        return ""  # Return empty string if query is None or not a string

    # Replace `==` with `IN` when comma-separated values are present
    query = re.sub(r"(\w+)\s*=\s*'([^']*,[^']*)'", r"\1 IN (\2)", query)

    # Replace `!=` (or `< >`) with `NOT IN` when comma-separated values are present
    query = re.sub(r"(\w+)\s*<>?\s*'([^']*,[^']*)'", r"\1 NOT IN (\2)", query)

    return query
