import streamlit as st

# Define lists for columns
text_columns = ["name", "department", "hire_date", "city", "email", "phone_number"]  # Add all 100 text columns
integer_columns = ["salary", "age", "experience_years", "project_count", "bonus", "rating"]  # Add all 100 integer columns

# Generate columns dictionary
columns = {col: {"type": "TEXT"} for col in text_columns}
columns.update({col: {"type": "INTEGER"} for col in integer_columns})

# Operator mappings
OPERATORS = {
    "TEXT": ["=", "!=", "IN", "NOT IN", "LIKE", "IS NULL"],
    "INTEGER": ["=", "!=", ">", "<", ">=", "<=", "BETWEEN", "IN", "NOT IN", "IS NULL"]
}

# Initialize session state for conditions
if "conditions" not in st.session_state:
    st.session_state.conditions = []

st.title("Advanced SQL Query Builder")
st.subheader("Build Complex Filters")


def add_condition():
    st.session_state.conditions.append(
        {"column": None, "operator": None, "value": None, "logic": "AND"}
    )


def remove_condition(index):
    del st.session_state.conditions[index]


def get_value_input(i, col_type: str, operator: str):
    """Helper function to generate correct value input field based on type and operator."""
    if operator in ["IN", "NOT IN"]:
        return st.text_input("Enter comma-separated values", key=f"value_{i}")
    elif operator == "BETWEEN":
        return st.text_input("Enter two values separated by comma", key=f"value_{i}")
    elif operator == "IS NULL":
        return None
    else:
        if col_type == "TEXT":
            return st.text_input("Value", key=f"value_{i}")
        else:
            return st.number_input("Value", key=f"value_{i}")


# UI for condition builder
with st.expander("➕ Add Condition Group", expanded=True):
    for i, condition in enumerate(st.session_state.conditions):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 2, 1])

        with col1:
            condition["column"] = st.selectbox(
                "Column",
                list(columns.keys()),
                index=list(columns.keys()).index(condition["column"])
                if condition["column"] else 0,
                key=f"col_{i}",
            )

        with col2:
            condition["operator"] = st.selectbox(
                "Operator",
                OPERATORS[columns[condition['column']]['type']],
                key=f"op_{i}",
            )

        with col3:
            condition["value"] = get_value_input(i, columns[condition["column"]]["type"], condition["operator"])

        with col4:
            if i > 0:
                condition["logic"] = st.selectbox("Logic", ["AND", "OR"], key=f"logic_{i}")

        with col5:
            st.button("❌", on_click=remove_condition, args=(i,), key=f"del_{i}")

    st.button("Add Condition", on_click=add_condition)


def build_where_clause():
    """Constructs the WHERE clause from conditions."""
    clauses = []
    for i, condition in enumerate(st.session_state.conditions):
        col = condition.get("column")
        op = condition.get("operator")
        val = condition.get("value")
        logic = condition.get("logic", "") if i > 0 else ""

        if not col or not op or (val is None and op != "IS NULL"):
            continue

        # Handling special cases
        if op == "IS NULL":
            clauses.append(f"{logic} {col} IS NULL")
            continue

        # Handling IN and NOT IN operators
        if op in ["IN", "NOT IN"]:
            values = [f"'{v.strip()}'" if columns[col]["type"] == "TEXT" else v.strip()
                      for v in val.split(",")]
            val_str = f"({', '.join(values)})"
        elif op == "BETWEEN":
            values = val.split(",")
            if len(values) == 2:
                val_str = f"{values[0].strip()} AND {values[1].strip()}"
        else:
            val_str = f"'{val}'" if columns[col]["type"] == "TEXT" else val

        clauses.append(f"{logic} {col} {op} {val_str}")

    return "WHERE " + " ".join(clauses) if clauses else ""


# Button to build query
if st.button("Build Query"):
    where_clause = build_where_clause()
    query = f"SELECT * FROM Employees {where_clause}"
    
    st.code(query)  # Display final query
