import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


st.title("Analytics on Accident Data")
st.text("A streamgraph")

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


accidents['Gravité'] = accidents['Gravité'].replace({
    'Blessé léger': 'Minor Incident',
    'Blessé hospitalisé': 'Hospitalization',
    'Tué': 'Fatal'
}).fillna('Other')

accidents['Arrondissement'] = accidents['Arrondissement'].astype(str).str[-2:]


accidents['Year'] = accidents['Date'].dt.year

# Filter widgets
# Creating columns for side-by-side filters

# Creating columns for side-by-side filters
col1, col2 = st.columns(2)
with col1:
    genre_filter = st.multiselect('Select Gender', options=list(accidents['Genre'].unique()), default=list(accidents['Genre'].unique()))
with col2:
    gravity_filter = st.multiselect('Select Gravity', options=list(accidents['Gravité'].unique()), default=list(accidents['Gravité'].unique()))

arrondissement_filter = st.multiselect('Select Arrondissement', options=sorted(list(accidents['Arrondissement'].unique())), default=sorted(list(accidents['Arrondissement'].unique())))

# Filter data based on selection
filtered_data = accidents[(accidents['Gravité'].isin(gravity_filter)) & (accidents['Genre'].isin(genre_filter)) & (accidents['Arrondissement'].isin(arrondissement_filter))]

# Aggregating Data
agg_data = filtered_data.groupby(['Year', 'Mode']).size().reset_index(name='Count')

# Create and display a Plotly area chart for accident evolution
fig = px.area(agg_data, x='Year', y='Count', color='Mode',
                labels={'Count': 'Total Accidents', 'Mode': 'Type of Accident', 'Year': 'Year'},
                title='Evolution of Accidents by Mode')
fig.update_layout(xaxis_title='Year', yaxis_title='Total Accidents',
                    legend_title='Mode', width=1200, height=600)
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