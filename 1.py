import streamlit as st
from itertools import chain
import sac  # Assuming sac is a valid library/module

# Initialize session state
if "selected_columns" not in st.session_state:
    st.session_state.selected_columns = []
if "default_selection" not in st.session_state:
    st.session_state.default_selection = []

# Multiselect dropdown
st.session_state.selected_columns = st.multiselect(
    "Select features", 
    [col for col in trade_view_columns], 
    default=st.session_state.selected_columns  # Retain previous selections
)

# Prepare tree structure with checkboxes checked based on selected_columns
items_category_tree = {
    col: {"label": col, "checked": col in st.session_state.selected_columns} 
    for col in trade_view_columns
}

# Render sac.tree with checkboxes reflecting selected columns
new_selection = sac.tree(
    items=items_category_tree, 
    label="Features", 
    open_all=False, 
    checkbox=True, 
    key="feature_selector"
)

# Convert selection to a list
new_selection = list(chain(st.session_state.default_selection, new_selection))

# Update session state only if selection changes
if new_selection != st.session_state.selected_columns:
    st.session_state.selected_columns = new_selection
    print(st.session_state.selected_columns)  # Debugging output
