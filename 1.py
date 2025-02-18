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
            'operators': ['less', 'equal', 'between', 'not_between']
        }
    elif column in list_columns:
        # Dropdown selection for operators
        selected_operator = st.selectbox(
            f"Select operator for {column}",
            ["=", "in", "not in"]
        )

        config['fields'][column] = {
            'label': column,
            'type': 'select',
            'operators': ['=', 'in', 'not in'],
            'mainWidgetProps': {
                'valuePlaceholder': 'Select values'
            }
        }

        # Show text input **only if "in" or "not in" is selected**
        if selected_operator in ["in", "not in"]:
            user_input = st.text_area(
                f"Enter values for {column} (comma-separated)", ""
            )
            list_values = [value.strip() for value in user_input.split(",") if value.strip()]

            if list_values:
                config['fields'][column]['fieldSettings'] = {
                    'listValues': [{'value': val, 'title': val} for val in list_values]
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
