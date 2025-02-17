import streamlit as st
import snowflake.connector
from concurrent.futures import ThreadPoolExecutor

# Function to get Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(
        user='YOUR_USER',
        password='YOUR_PASSWORD',
        account='YOUR_ACCOUNT',
        warehouse='YOUR_WAREHOUSE',
        database='YOUR_DATABASE',
        schema='YOUR_SCHEMA'
    )

# Function to execute queries
def execute_query(query, conn):
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

# Check if query is built
if st.session_state.get('query_built', False):

    if st.button("Execute Query"):
        with st.spinner("Executing query..."):
            conn = get_snowflake_connection()
            
            if conn:
                # Run queries in parallel
                with ThreadPoolExecutor(max_workers=2) as executor:
                    future_count = executor.submit(execute_query, st.session_state.pre_result, conn)
                    future_data = executor.submit(execute_query, st.session_state.sql_query, conn)

                    result = future_count.result()
                    data = future_data.result()

                # Get total rows
                total_rows = len(result) if result else 0
                st.write(total_rows)

                # Print results
                if data:
                    print("True")
                else:
                    print("False")
                    st.warning("No data to preview with this query!")

            conn.close()
