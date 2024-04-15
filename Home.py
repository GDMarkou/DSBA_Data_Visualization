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

# Data Loading
accidents = pd.read_csv("data/accidentologie0.csv", sep=";")

# Page Display Logic

st.title("Welcome to the Paris Incident Explorer 🚦🛣️")
st.write("In this dashboard, we give you full power to explore and understand how, where, and when road accidents occur in Paris. Specifically, we prepared 3 different interactive visualization that include analysis of the different districts, modes of transportation, and seasonality. You can access the following from the pages tab.")

st.title("Dataset Exploration 📊")
st.write("The dataset titled 'Paris Traffic Accident Data' spans from 2017 to 2022 and offers a comprehensive examination of traffic accidents within Paris. It is structured such that each row represents a unique accident, detailing the type of vehicle involved, the accident date, location, and demographic information such as age and gender of the individuals involved, along with the severity and descriptions of each incident. This dataset is sourced from official reports by the Paris Police Prefecture and is curated to ensure accuracy and minimize human errors, as stated on the Open Data Paris website. The data is crucial for analyzing patterns, contributing factors, and areas of concern related to road safety in Paris. This analysis aims to aid in developing targeted interventions by authorities to decrease accident rates and enhance road safety.")
st.write(accidents)  # Example of displaying a dataframe
    
