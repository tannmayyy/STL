import streamlit as st
from streamlit_condition_tree import condition_tree

# Sample configuration with 'in' and 'not_in' operators
config = {
    'fields': {
        'First Name': {
            'label': 'First Name',
            'type': 'text',
            'operators': ['equal', 'not_equal', 'in', 'not_in'],
            'mainWidgetProps': {
                'valuePlaceholder': 'Enter name(s)',
            },
        },
        'Age': {
            'label': 'Age',
            'type': 'number',
            'operators': ['equal', 'not_equal', 'in', 'not_in', 'less', 'greater'],
            'mainWidgetProps': {
                'valuePlaceholder': 'Enter age(s)',
            },
        },
        # Add other fields as needed
    }
}

# Render the condition tree component
query = condition_tree(
    config=config,
    return_type='sql',  # Returns the query as an SQL string
    placeholder='Build your query conditions',
    key='condition_tree'
)

# Display the generated query
st.write("Generated Query:", query)
