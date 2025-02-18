import streamlit as st
import snowflake.connector

def get_snowflake_connection():
    """Authenticate user using Snowflake SSO and establish a session."""
    try:
        conn = snowflake.connector.connect(
            account="your_snowflake_account",  # Example: xyz-org.snowflakecomputing.com
            warehouse="analytics",
            database="SIMI",
            schema="NOMO",
            authenticator="externalbrowser"
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        return None

def check_user_access(conn):
    """Check if the user has the required roles."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_ROLE();")  # Get user's role
        role = cursor.fetchone()[0]

        allowed_roles = ["ANALYST", "ADMIN"]
        if role not in allowed_roles:
            st.error("❌ You're not authorized to access this resource.")
            return False
        return True
    except Exception as e:
        st.error(f"Access check failed: {e}")
        return False

# Streamlit UI
st.title("Snowflake SSO Login")

# Initialize session state variables if they don't exist
if "snowflake_conn" not in st.session_state:
    st.session_state["snowflake_conn"] = None
    st.session_state["authenticated"] = False

# Login Button
if st.button("Login with Snowflake SSO"):
    conn = get_snowflake_connection()
    if conn and check_user_access(conn):
        st.success("✅ Successfully connected to Snowflake!")
        st.session_state["snowflake_conn"] = conn
        st.session_state["authenticated"] = True
    else:
        st.error("Access Denied!")

# **SQL Query Execution**
if st.session_state["authenticated"]:
    st.subheader("Execute SQL Query")

    query = st.text_area("Enter your SQL Query:", height=150)

    if st.button("Run Query"):
        try:
            conn = st.session_state["snowflake_conn"]
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            st.write("Query Results:")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Query Execution Failed: {e}")
