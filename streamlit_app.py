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
    st.title('Paris Incident Exploration🗼')
    # Radio buttons for page navigation
    page = st.radio("Select a page to explore", ('Introduction', 'Paris Road Accident', 'Detailed Data View', 'Analytics'))

# Data Loading
accidents = pd.read_csv("data/accidentologie0.csv", sep=";")
accidents['Date'] = pd.to_datetime(accidents['Date'])
accidents['Mode'] = accidents['Mode'].replace({
    '2 Roues Motorisées': '2-Wheel Motorbike',
    '4 Roues': '4-Wheel',
    'Autres': 'Other',
    'EDP-m': 'Electric Scooter',
    'Piéton': 'Pedestrian',
    'Vélo': 'Bike'
}).fillna('Other')
accidents['Year'] = accidents['Date'].dt.year

# Aggregating Data
agg_data = accidents.groupby(['Year', 'Mode']).size().reset_index(name='Count')

# Page Display Logic

# Page One. This is the Introduction page here we will give a brief overview like we did in the 
if page == 'Introduction':
    st.title("Welcome to the Paris Incident Explorer! 🥐🚗🏍️")
    st.text("In this dashboard, we present to you the accidents that occurred in Paris.")
    st.write(accidents)  # Example of displaying a dataframe
elif page == 'Detailed Data View':
    st.title("Detailed Data View")
elif page == 'Analytics':
    st.title("Analytics on Accident Data")
    # Create and display a Plotly area chart for accident evolution
    fig = px.area(agg_data, x='Year', y='Count', color='Mode',
                  labels={'Count': 'Total Accidents', 'Mode': 'Type of Accident', 'Year': 'Year'},
                  title='Evolution of Accidents by Mode')
    fig.update_layout(xaxis_title='Year', yaxis_title='Total Accidents',
                      legend_title='Mode', width=800, height=400)
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor="rgba(68, 68, 68, 0.1)"
            ),
            type="date",
            tickfont=dict(
                family="Helvetica, sans-serif",
                size=10,
                color="darkblue")
        )
    )
    st.plotly_chart(fig)