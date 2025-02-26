import re

def modify_sql_query(query):
    if not query or not isinstance(query, str):
        return ""

    # Replace `=` with `IN`, ensuring values are quoted
    query = re.sub(r"(\w+)\s*=\s*'([^']*,[^']*)'", lambda m: f"{m.group(1)} IN ({', '.join([f'\'{v.strip()}\'' for v in m.group(2).split(',')])})", query)

    # Replace `!=` or `<>` with `NOT IN`, ensuring values are quoted
    query = re.sub(r"(\w+)\s*<>?\s*'([^']*,[^']*)'", lambda m: f"{m.group(1)} NOT IN ({', '.join([f'\'{v.strip()}\'' for v in m.group(2).split(',')])})", query)

    return query
