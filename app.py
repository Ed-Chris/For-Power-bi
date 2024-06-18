import streamlit as st
import pandas as pd

st.title("Labour Market Data Visualization")

# Define the URL of your Flask endpoint
url = "http://localhost:5000/data.csv"

# Fetch the data from the Flask endpoint
@st.cache
def load_data():
    df = pd.read_csv(url)
    return df

# Load the data
data = load_data()

# Display the data in Streamlit
st.write(data)
