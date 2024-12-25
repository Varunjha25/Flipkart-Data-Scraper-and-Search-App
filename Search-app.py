import pandas as pd
import sqlite3
import streamlit as st

# Load your data from SQLite database
db_path = "E:/Portfolio Project/Flipkart/scraped_data.db"

# Streamlit app title
st.title("Customer Search Box")

# Create a search box for user input
customer_code = st.text_input("Enter Customer Code or Keyword to Search:", "")

# Function to load data from SQLite database
def load_data(query):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Query the database
if customer_code:
    query = f"""
    SELECT * FROM scraped_links 
    WHERE title LIKE '%{customer_code}%' OR link LIKE '%{customer_code}%'
    """
    filtered_data = load_data(query)
    
    # Display results
    if not filtered_data.empty:
        st.write("Search Results:")
        st.dataframe(filtered_data)
    else:
        st.write("No data found for the entered keyword.")
else:
    st.write("Please enter a keyword to search.")
