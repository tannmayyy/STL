import streamlit as st

def build_sql_query(table_name, filters):
    query = f"SELECT * FROM {table_name}"
    
    conditions = []
    for column, condition in filters.items():
        if condition["operator"] == "IN":
            values = "', '".join(map(str, condition["values"]))
            conditions.append(f"{column} IN ('{values}')")
        elif condition["operator"] == "NOT IN":
            values = "', '".join(map(str, condition["values"]))
            conditions.append(f"{column} NOT IN ('{values}')")
        elif condition["operator"] in [">", "<", "=", "!="]:
            numeric_values = ", ".join(map(str, condition["values"]))
            conditions.append(f"{column} {condition['operator']} {numeric_values}")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    return query

st.title("SQL Query Builder")

table_name = st.text_input("Enter Table Name", "Employees")

string_columns = ["department", "city"]
numeric_columns = ["salary", "age"]

selected_column = st.selectbox("Select Column", string_columns + numeric_columns)

if selected_column in string_columns:
    operator = st.selectbox("Select Operator", ["IN", "NOT IN"])
else:
    operator = st.selectbox("Select Operator", [">", "<", "=", "!="])

values_input = st.text_area("Enter Values (comma separated)")

if st.button("Generate Query"):
    values = [v.strip() for v in values_input.split(",") if v.strip()]
    
    if selected_column in numeric_columns:
        values = [int(v) for v in values if v.isdigit()]

    filters = {selected_column: {"operator": operator, "values": values}}

    query = build_sql_query(table_name, filters)
    st.code(query, language="sql")
