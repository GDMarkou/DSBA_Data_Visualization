import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Paris Incident Exploration",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Hello")
st.text("In this assignment, we are going to present to you the accidents that occurred in Paris.")

alt.themes.enable("dark")
df_reshaped = pd.read_csv('data/question_ready_ds.csv', sep=",")

with st.sidebar:
    st.title('🗼🚗 Paris Incident Exploration')

### ------------------------------------------------ Alex First  -----------------------------------------------------------------------##

# Load the accidents data
accidents = pd.read_csv("data/accidentologie0.csv", sep=";")
accidents['Date'] = pd.to_datetime(accidents['Date'])

# Mapping modes of transportation to more readable forms
mode_mapping = {
    '2 Roues Motorisées': '2-Wheel Motorbike',
    '4 Roues': '4-Wheel',
    'Autres': 'Other',
    'EDP-m': 'Electric Scooter',
    'Piéton': 'Pedestrian',
    'Vélo': 'Bike'
}
accidents['Mode'] = accidents['Mode'].replace(mode_mapping).fillna('Other')
accidents['Year'] = accidents['Date'].dt.year

# Aggregating the data by Year and Mode
agg_data = accidents.groupby(['Year', 'Mode']).size().reset_index(name='Count')

# Creating a streamgraph (area chart) with Plotly
fig = px.area(agg_data, x='Year', y='Count', color='Mode',
              labels={'Count': 'Total Accidents', 'Mode': 'Type of Accident', 'Year': 'Year'},
              title='Evolution of Accidents by Mode')
fig.update_layout(xaxis_title='Year', yaxis_title='Total Accidents',
                  legend_title='Mode', width=800, height=400)

# Add range slider
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

# Display the figure using Streamlit
st.plotly_chart(fig)
### ------------------------------------------------ Alex First  -----------------------------------------------------------------------##
