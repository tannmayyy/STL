import streamlit as st
from streamlit_condition_tree import condition_tree

# Example columns for filtering
trade_view_columns_for_filter = ["BUSINESS_DATE", "TRADE_ID", "COUNTRY", "STATUS"]

# Define categories for different types of filters
free_input = ["TRADE_ID", "STATUS"]  # Text input fields
date_columns = ["BUSINESS_DATE"]  # Date input fields
list_columns = ["COUNTRY"]  # Columns where "in" and "not in" will be used

# Allow users to select filters dynamically
st.session_state.filter_columns = st.multiselect(
    "Select Filters",
    [col for col in trade_view_columns_for_filter if col != 'BUSINESS_DATE']
)

# Initialize the config dictionary
config = {'fields': {}}

# Loop through selected filters and assign configurations
for column in st.session_state.filter_columns:
    if column in free_input:
        # Free text input for specific columns
        config['fields'][column] = {
            'label': column,
            'type': 'text',
            'mainWidgetProps': {
                'valuePlaceholder': f"Enter value for {column}"
            }
        }
    elif column in date_columns:
        # Date filter with multiple operators
        config['fields'][column] = {
            'label': column,
            'type': 'date',
            'operators': ['less', 'equal', 'between', 'not_between'],
            'mainWidgetProps': {
                'start_date': {
                    'type': 'date',
                    'label': f"Start date for {column}",
                    'operators': ['less', 'less_equal', 'greater', 'greater_equal', 'equal', 'between', 'not_between']
                },
                'end_date': {
                    'type': 'date',
                    'label': f"End date for {column}"
                }
            }
        }
    elif column in list_columns:
        # Dropdown selection with "in" and "not in"
        config['fields'][column] = {
            'label': column,
            'type': 'select',
            'operators': ['in', 'not_in'],
            'fieldSettings': {
                'listValues': [
                    {'value': 'USA', 'title': 'USA'},
                    {'value': 'UK', 'title': 'UK'},
                    {'value': 'India', 'title': 'India'},
                    {'value': 'Germany', 'title': 'Germany'}
                ]
            },
            'mainWidgetProps': {
                'customInput': True,  # Allows users to enter values manually
                'valuePlaceholder': 'Enter multiple values separated by commas'
            }
        }
    else:
        # Default input for other columns
        config['fields'][column] = {
            'label': column,
            'type': 'text',
            'mainWidgetProps': {
                'valuePlaceholder': f"Enter value for {column}"
            }
        }

# Generate condition tree only if filters are selected
if config['fields']:
    condition_tree_query = condition_tree(
        config,
        return_type='sql',
        placeholder='Build your query conditions'
    )
    st.write("Generated SQL Query:")
    st.code(condition_tree_query)
else:
    st.write("Please select at least one filter.")
