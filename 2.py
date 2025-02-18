import snowflake.connector
import streamlit as st

# Initialize session state variables
if "snowflake_conn" not in st.session_state:
    st.session_state["snowflake_conn"] = None

def get_snowflake_connection():
    """Establish a connection to Snowflake using stored credentials."""
    try:
        if st.session_state["snowflake_conn"] is None:
            conn = snowflake.connector.connect(
                
            )
            st.session_state["snowflake_conn"] = conn
            print("✅ Snowflake connection established.")
        return st.session_state["snowflake_conn"]
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        return None

def execute_query(query):
    """Execute a SQL query using the existing Snowflake connection."""
    conn = st.session_state.get("snowflake_conn")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            print("Query ID:", cursor.sfqid)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return None
    else:
        st.error("No active Snowflake connection.")
        return None
