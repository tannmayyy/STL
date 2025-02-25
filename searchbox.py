import streamlit as st
from condition_tree import condition_tree

# Correct dictionary-based field configuration
config = {
    'fields': {
        'name': {
            'label': 'Name',
            'type': 'string',
            'operators': ["equal", "not_equal", "in", "not_in"]  # Required
        },
        'age': {
            'label': 'Age',
            'type': 'number',
            'operators': ["equal", "not_equal", "less", "less_or_equal", "greater", "greater_or_equal", "in", "not_in"],
            'fieldSettings': {
                'min': 0
            }
        },
        'like_tomatoes': {
            'label': 'Likes tomatoes',
            'type': 'boolean',
            'operators': ["equal"]  # Required
        }
    }
}

# Render condition tree with proper config
return_val = condition_tree(
    config=config,
    return_type='sql',
    key='my_unique_key'
)

# Display generated SQL
if return_val:
    st.code(return_val)