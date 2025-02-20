import streamlit as st

# Define columns and their types
columns = {"department": "TEXT", "salary": "INTEGER", "age": "INTEGER", "city": "TEXT"}

# Operator mappings
OPERATORS = {
    "TEXT": ["IN", "NOT IN"],
    "INTEGER": ["IN", "NOT IN"]
}

# Initialize session state
if 'conditions' not in st.session_state:
    st.session_state.conditions = []

def add_condition():
    st.session_state.conditions.append({
        'column': None,
        'operator': None,
        'value': None
    })

def remove_condition(index):
    del st.session_state.conditions[index]

def get_value_input(col_type: str, operator: str, index: int):
    return st.text_input("Enter comma-separated values", key=f"value_{index}")

st.title("SQL Query Builder")
st.subheader("Add Filters")

with st.expander("➕ Add Condition", expanded=True):
    for i, condition in enumerate(st.session_state.conditions):
        col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
        
        with col1:
            column = st.selectbox("Column", options=list(columns.keys()), key=f"col_{i}")
        
        with col2:
            operator = st.selectbox("Operator", options=OPERATORS[columns[column]], key=f"op_{i}")
        
        with col3:
            value = get_value_input(columns[column], operator, i)
        
        with col4:
            st.button("❌", on_click=remove_condition, args=(i,), key=f"del_{i}")
    
    st.button("Add Condition", on_click=add_condition)

def build_where_clause():
    clauses = []
    for i, condition in enumerate(st.session_state.conditions):
        col = condition['column']
        op = condition['operator']
        val = condition['value']
        
        if not col or not op or not val:
            continue
        
        values = [f"'{v.strip()}'" if columns[col] == 'TEXT' else v.strip() for v in val.split(',')]
        val_str = f"({', '.join(values)})"
        
        clauses.append(f"{col} {op} {val_str}")
    
    return 'WHERE ' + ' AND '.join(clauses) if clauses else ''

if st.button("Build Query"):
    where_clause = build_where_clause()
    query = f"SELECT * FROM Employees {where_clause}"
    st.code(query)
