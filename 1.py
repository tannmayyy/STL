import streamlit as st
import snowflake.connector

def get_snowflake_connection():
    """Authenticate user using Snowflake SSO and establish a session."""
    try:
        conn = snowflake.connector.connect(
            user=st.session_state["snowflake_user"],
            account="your_snowflake_account",  # e.g., xyz-org.snowflakecomputing.com
            warehouse="analyticygvfnmnvgs",
            database="SIhhbgMI",
            schema="NOMkhhgggvvO",
            authenticator="externalbrowser"
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        return None

def check_user_access(conn):
    """Check if the user has access to required resources."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_ROLE();")  # Check user’s Snowflake role
        role = cursor.fetchone()[0]

        # Define allowed roles
        allowed_roles = ["ANALYST", "ADMIN"]
        if role not in allowed_roles:
            st.error("You're not authorized to access this resource.")
            return False
        return True
    except Exception as e:
        st.error(f"Access check failed: {e}")
        return False

# Streamlit UI
st.title("Snowflake SSO Login")

# Login Button
if st.button("Login with Snowflake SSO"):
    try:
        conn = get_snowflake_connection()
        if conn and check_user_access(conn):
            st.success("✅ Successfully connected to Snowflake!")
            st.session_state["snowflake_conn"] = conn
            st.session_state["authenticated"] = True
        else:
            st.error("Access Denied!")
    except Exception as e:
        st.error(f"SSO Authentication Failed: {e}")

# **SQL Query Execution**
if "snowflake_conn" in st.session_state and st.session_state["authenticated"]:
    st.subheader("Execute SQL Query")

    # Text area for SQL input
    query = st.text_area("Enter your SQL Query:", height=150)

    if st.button("Run Query"):
        try:
            conn = st.session_state["snowflake_conn"]
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            # Show results in a DataFrame
            st.write("Query Results:")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Query Execution Failed: {e}")
