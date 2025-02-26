import re

def modify_sql_query(query):
    if not query or not isinstance(query, str):
        return ""

    # Replace `=` with `ANY (ARRAY[...])` and properly format values
    query = re.sub(
        r"(\w+)\s*=\s*'([^']*,[^']*)'",
        lambda m: f"{m.group(1)} = ANY (ARRAY[{', '.join([f'\'{v.strip()}\'' for v in m.group(2).split(',')])}])",
        query
    )

    # Replace `!=` or `<>` with `NOT IN (...)` and properly format values
    query = re.sub(
        r"(\w+)\s*<>?\s*'([^']*,[^']*)'",
        lambda m: f"{m.group(1)} NOT IN ({', '.join([f'\'{v.strip()}\'' for v in m.group(2).split(',')])})",
        query
    )

    return query
