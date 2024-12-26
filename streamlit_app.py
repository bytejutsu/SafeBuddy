import streamlit as st
from supabase import create_client

# Initialize connection.
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Failed to connect to Supabase: {e}")
        return None

supabase = init_connection()

# Perform query.
@st.cache_data(ttl=600)
def run_query():
    try:
        response = supabase.table("mytable").select("*").execute()
        return response.data  # Return only the data as a list of dictionaries.
    except Exception as e:
        st.error(f"Query failed: {e}")
        return []

rows = run_query()

# Display results.
if rows:
    for row in rows:
        st.write(f"{row.get('name', 'Unknown')} has a :{row.get('pet', 'unknown pet')}:")
else:
    st.warning("No data to display.")
