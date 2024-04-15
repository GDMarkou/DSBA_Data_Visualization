import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Paris Incident Exploration",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Page Navigation if it's not already set
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Sidebar for Navigation
with st.sidebar:
    st.title('Home Navigator')
    # Radio buttons for page navigation
    page = st.radio("Welcome to the home page. Here you can take a deep dive into the improta", ('Introduction', 'Importance of the Problem', 'Dataset'))

# Data Loading
accidents = pd.read_csv("data/accidentologie0.csv", sep=";")

# Page Display Logic
if page == 'Introduction':
    st.title("Welcome to the Paris Incident Explorer!")
    st.text("In this dashboard, we present to you the accidents that occurred in Paris.")
    
elif page == 'Importance of the Problem':
    st.title("Importance of the Problem")
    


elif page == 'Dataset':
    st.title("Dataset")
    st.text("The Dataframe bellow ")
    st.write(accidents)  # Example of displaying a dataframe
    
