import re

def modify_sql_query(query):
    if not query or not isinstance(query, str):
        return ""  # Return empty string if query is None or not a string

    # Replace `==` with `IN`, ensuring each value is quoted
    query = re.sub(r"(\w+)\s*=\s*'([^']*,[^']*)'", lambda m: f"{m.group(1)} IN ({', '.join([f'\'{v.strip()}\'' for v in m.group(2).split(',')])})", query)

    # Replace `!=` (or `< >`) with `NOT IN`, ensuring each value is quoted
    query = re.sub(r"(\w+)\s*<>?\s*'([^']*,[^']*)'", lambda m: f"{m.group(1)} NOT IN ({', '.join([f'\'{v.strip()}\'' for v in m.group(2).split(',')])})", query)

    return query
