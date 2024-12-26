import streamlit as st
from supabase import create_client
import pandas as pd


# Initialize connection to Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# Perform query to fetch data from the "incidents" table
@st.cache_data(ttl=600)
def fetch_incidents():
    try:
        response = supabase.table("incidents").select("*").execute()
        return response.data  # Return only the data as a list of dictionaries.
    except Exception as e:
        st.error(f"Query failed: {e}")
        return []

# Fetch the incidents data
incidents = fetch_incidents()

# Display the data
st.title("Incidents Table")

if incidents:
    # Convert the data into a DataFrame for better display
    df = pd.DataFrame(incidents)

    # Display the table in Streamlit
    st.dataframe(df)

    # Optional: Show specific metrics or analysis
    st.subheader("Summary Statistics")
    st.write(f"Total Incidents: {len(df)}")
else:
    st.write("No incidents data available!.")
