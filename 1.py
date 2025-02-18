import streamlit as st
from streamlit_condition_tree import condition_tree

# Example columns (Replace these with your actual column lists)
trade_view_columns_for_filter = ["column1", "column2", "BUSINESS_DATE", "column3"]
free_input = ["column1", "column2"]
date_columns = ["BUSINESS_DATE"]
config = {"fields": {}}

st.session_state.filter_columns = st.multiselect(
    "Select Filters",
    [col for col in trade_view_columns_for_filter if col != "BUSINESS_DATE"]
)

for column in st.session_state.filter_columns:
    if column in free_input:
        config["fields"][column] = {
            "label": column,
            "type": "text",
            "mainwidgetProps": {
                "valuePlaceholder": f"Enter value for {column}"
            },
            "operators": ["equal", "not_equal", "inlist", "not_inlist"]
        }
    
    elif column in date_columns:
        config["fields"][column] = {
            "label": column,
            "type": "date",
            "operators": ["less", "equal", "greater", "between", "not_between"],
            "mainwidgetProps": {
                "start_date": {"type": "date", "label": f"Start date for {column}"},
                "end_date": {"type": "date", "label": f"End date for {column}"}
            }
        }
    
    else:
        config["fields"][column] = {
            "label": column,
            "type": "text",
            "operators": ["equal", "not_equal", "inlist", "not_inlist"],
            "mainwidgetProps": {
                "valuePlaceholder": f"Enter values for {column} (comma-separated)"
            }
        }

# Display Condition Tree if filters are selected
if config["fields"]:
    condition_tree_query = condition_tree(
        config,
        return_type="sql",
        placeholder="Build your query conditions"
    )
else:
    condition_tree_query = None

st.write(condition_tree_query)
