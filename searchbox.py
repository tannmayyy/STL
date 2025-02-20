import streamlit as st

def build_sql_query(table_name, filters):
    query = f"SELECT * FROM {table_name} WHERE 1=1"
    
    for column, condition in filters.items():
        if condition["operator"] == "IN":
            values = "', '".join(map(str, condition["values"]))
            query += f" AND {column} IN ('{values}')"
        elif condition["operator"] == "NOT IN":
            values = "', '".join(map(str, condition["values"]))
            query += f" AND {column} NOT IN ('{values}')"
        elif condition["operator"] in ["=", "!=", ">", "<"]:
            query += f" AND {column} {condition['operator']} {condition['values'][0]}"
    
    return query

st.title("SQL Query Builder")

table_name = st.text_input("Enter Table Name", "Employees")

filters = {}

col1, col2, col3 = st.columns(3)

with col1:
    column_name = st.text_input("Enter Column Name")

with col2:
    operator = st.selectbox("Select Operator", ["IN", "NOT IN", "=", "!=", ">", "<"])

with col3:
    values_input = st.text_area("Enter Values (comma separated)")

if st.button("Generate Query"):
    values = [v.strip() for v in values_input.split(",") if v.strip()]
    
    if column_name and values:
        filters[column_name] = {"operator": operator, "values": values}
    
    query = build_sql_query(table_name, filters)
    st.code(query, language="sql")
