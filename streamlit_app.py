import streamlit as st
from supabase import create_client

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
    response = supabase.table("incidents").select("*").execute()
    if response.status_code != 200:
        st.error("Failed to fetch data from Supabase!")
        return []
    return response.data

# Fetch the incidents data
incidents = fetch_incidents()

# Display the data
st.title("Incidents Table")

if incidents:
    # Convert the data into a DataFrame for better display
    import pandas as pd
    df = pd.DataFrame(incidents)

    # Display the table in Streamlit
    st.dataframe(df)

    # Optional: Show specific metrics or analysis
    st.subheader("Summary Statistics")
    st.write(f"Total Incidents: {len(df)}")
    st.write(f"Zones Covered: {df['Zone'].nunique()}")
else:
    st.write("No incidents data available.")
