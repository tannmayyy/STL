import streamlit as st
import sqlite3
from sqlite3 import Error

# Create in-memory SQLite database
conn = sqlite3.connect(':memory:')
c = conn.cursor()

# Create sample table
c.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER,
        hire_date TEXT
    )
''')

# Insert sample data
employees = [
    (1, 'John Doe', 'HR', 50000, '2020-01-15'),
    (2, 'Jane Smith', 'IT', 65000, '2018-05-22'),
    (3, 'Mike Johnson', 'Finance', 70000, '2019-11-30'),
    (4, 'Sarah Williams', 'HR', 55000, '2021-03-10'),
    (5, 'James Brown', 'IT', 62000, '2022-07-05'),
]
c.executemany('INSERT INTO Employees VALUES (?,?,?,?,?)', employees)
conn.commit()

# Get column metadata
c.execute("PRAGMA table_info(Employees)")
columns = {col[1]: {'type': col[2]} for col in c.fetchall() if col[1] != 'id'}

# Operator mappings
OPERATORS = {
    'TEXT': ['IN', 'NOT IN'],
    'INTEGER': ['IN', 'NOT IN', '>', '<', '=', '!=']
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

# UI for conditions
with st.expander("➕ Add Condition Group", expanded=True):
    for i, condition in enumerate(st.session_state.conditions):
        col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
        
        with col1:
            column = st.selectbox(
                "Column", list(columns.keys()), key=f"col_{i}")
            condition['column'] = column
        
        with col2:
            operator = st.selectbox(
                "Operator", OPERATORS[columns[column]['type']], key=f"op_{i}")
            condition['operator'] = operator
        
        with col3:
            value = get_value_input(columns[column]['type'], operator, i)
            condition['value'] = value
        
        with col4:
            st.button("❌", on_click=remove_condition, args=(i,), key=f"del_{i}")

    st.button("Add Condition", on_click=add_condition)

# Query construction
def build_where_clause():
    clauses = []
    for condition in st.session_state.conditions:
        col = condition['column']
        op = condition['operator']
        val = condition['value']
        
        if not col or not op or not val:
            continue
        
        values = [v.strip() for v in val.split(',')]
        
        if op in ['IN', 'NOT IN']:
            if columns[col]['type'] == 'TEXT':
                val_str = f"({', '.join(f'\'{v}\'' for v in values)})"
            else:
                val_str = f"({', '.join(values)})"
        else:
            val_str = values[0]
        
        clauses.append(f"{col} {op} {val_str}")
    
    return 'WHERE ' + ' AND '.join(clauses) if clauses else ''

# Execute and display results
if st.button("Build Query"):
    try:
        where_clause = build_where_clause()
        query = f"SELECT * FROM Employees {where_clause}"
        
        st.code(query)
        c.execute(query)
        results = c.fetchall()
        
        if results:
            st.write(f"Found {len(results)} records:")
            st.table(results)
        else:
            st.write("No results found")
    except Error as e:
        st.error(f"Query error: {str(e)}")

conn.close()
