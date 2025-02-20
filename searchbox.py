import streamlit as st
import sqlite3
from sqlite3 import Error
from typing import List, Dict, Union

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
    'TEXT': ['=', '!=', 'IN', 'NOT IN', 'LIKE', 'IS NULL'],
    'INTEGER': ['=', '!=', '>', '<', '>=', '<=', 'BETWEEN', 'IN', 'NOT IN', 'IS NULL'],
    'NUMERIC': ['=', '!=', '>', '<', '>=', '<=', 'BETWEEN', 'IN', 'NOT IN', 'IS NULL']
}

# Initialize session state
if 'conditions' not in st.session_state:
    st.session_state.conditions = []

st.title("Advanced SQL Query Builder")
st.subheader("Build Complex Filters")

def add_condition():
    st.session_state.conditions.append({
        'column': None,
        'operator': None,
        'value': None,
        'logic': 'AND'
    })

def remove_condition(index):
    del st.session_state.conditions[index]

def get_value_input(col_type: str, operator: str) -> Union[str, float, tuple]:
    if operator in ['IN', 'NOT IN']:
        return st.text_input("Enter comma-separated values", key=f"value_{i}")
    elif operator == 'BETWEEN':
        return st.text_input("Enter two values separated by comma", key=f"value_{i}")
    elif operator == 'IS NULL':
        return None
    else:
        if col_type == 'TEXT':
            return st.text_input("Value", key=f"value_{i}")
        else:
            return st.number_input("Value", key=f"value_{i}")

# Condition builder UI
with st.expander("➕ Add Condition Group", expanded=True):
    for i, condition in enumerate(st.session_state.conditions):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 2, 1])
        
        with col1:
            column = st.selectbox(
                "Column",
                options=list(columns.keys()),
                key=f"col_{i}"
            )
        
        with col2:
            operator = st.selectbox(
                "Operator",
                options=OPERATORS[columns[column]['type']],
                key=f"op_{i}"
            )
        
        with col3:
            value = get_value_input(columns[column]['type'], operator)
        
        with col4:
            if i > 0:
                logic = st.selectbox(
                    "Logic",
                    ['AND', 'OR'],
                    key=f"logic_{i}"
                )
        
        with col5:
            st.button("❌", on_click=remove_condition, args=(i,), key=f"del_{i}")

    st.button("Add Condition", on_click=add_condition)

# Query construction
def build_where_clause():
    clauses = []
    for i, condition in enumerate(st.session_state.conditions):
        col = condition['column']
        op = condition['operator']
        val = condition['value']
        logic = condition['logic'] if i > 0 else ''

        if not col or not op:
            continue

        # Handle NULL values
        if op == 'IS NULL':
            clauses.append(f"{logic} {col} IS NULL")
            continue

        # Handle value formatting
        if val:
            if op in ['IN', 'NOT IN']:
                values = [f"'{v.strip()}'" if columns[col]['type'] == 'TEXT' else v.strip() 
                         for v in val.split(',')]
                val_str = f"({', '.join(values)})"
            elif op == 'BETWEEN':
                values = val.split(',')
                if len(values) == 2:
                    val_str = f"{values[0].strip()} AND {values[1].strip()}"
            else:
                val_str = f"'{val}'" if columns[col]['type'] == 'TEXT' else val

            clauses.append(f"{logic} {col} {op} {val_str}")

    return 'WHERE ' + ' '.join(clauses) if clauses else ''

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