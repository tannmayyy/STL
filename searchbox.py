import streamlit as st
from condition_tree import condition_tree
import re

# Define configuration for the condition tree
config = {
    'fields': {
        'name': {
            'label': 'Name',
            'type': 'string',
            'operators': ["equal", "not_equal", "in", "not_in"]
        },
        'age': {
            'label': 'Age',
            'type': 'number',
            'operators': ["equal", "not_equal", "less", "less_or_equal", "greater", "greater_or_equal", "in", "not_in"]
        }
    }
}

# Render condition tree
generated_sql = condition_tree(config=config, return_type='sql', key='condition_tree')

# Function to modify SQL query safely
def modify_sql_query(query):
    if not query or not isinstance(query, str):
        return ""  # Return empty string if query is None or not a string

    # Replace `==` with `ANY` when comma-separated values are present
    query = re.sub(r"(\w+)\s*=\s*'([^']*,[^']*)'", r"\1 ANY ('\2')", query)

    # Replace `!=` with `NOT IN` when comma-separated values are present
    query = re.sub(r"(\w+)\s*!=\s*'([^']*,[^']*)'", r"\1 NOT IN ('\2')", query)

    return query

# Modify and display the updated SQL query
if generated_sql:
    modified_sql = modify_sql_query(generated_sql)
    st.code(modified_sql)
else:
    st.warning("No SQL query generated yet.")
