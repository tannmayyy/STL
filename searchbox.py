import streamlit as st
from condition_tree import condition_tree  # Correct import name

# Build a proper configuration structure
config = {
    "fields": [
        {
            "name": "name",
            "label": "Name",
            "type": "string",
            "operators": ["equal", "not_equal", "in", "not_in"]  # Added operators
        },
        {
            "name": "age",
            "label": "Age",
            "type": "number",
            "operators": ["equal", "not_equal", "in", "not_in", "less", "less_or_equal", "greater", "greater_or_equal"],
            "fieldSettings": {
                "min": 0
            },
        },
        {
            "name": "like_tomatoes",
            "label": "Likes tomatoes",
            "type": "boolean",
            "operators": ["equal"]  # Typically only need 'equal' for booleans
        }
    ]
}

# Render the condition tree with proper configuration
conditions = condition_tree(
    config=config,
    key="my_condition_tree"  # Add unique key for session state
)

# Generate SQL from the conditions
if conditions:
    sql_parts = []
    for condition in conditions:
        field = condition["field"]
        operator = condition["operator"].upper()
        value = condition["value"]

        # Handle different value types
        if operator in ["IN", "NOT IN"]:
            # Format array values
            values = [f"'{v.strip()}'" if isinstance(v, str) else str(v) 
                     for v in value.split(",")]
            sql_part = f"{field} {operator} ({', '.join(values)})"
        elif condition["type"] == "boolean":
            # Handle boolean values without quotes
            sql_part = f"{field} = {value}"
        elif condition["type"] == "number":
            # Handle numbers without quotes
            sql_part = f"{field} {operator} {value}"
        else:
            # Handle strings with quotes
            sql_part = f"{field} {operator} '{value}'"

        sql_parts.append(sql_part)

    full_sql = "SELECT * FROM table\nWHERE " + " AND ".join(sql_parts)
    st.code(full_sql)