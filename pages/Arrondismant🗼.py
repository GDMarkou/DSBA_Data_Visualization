import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import streamlit as st
import pydeck as pdk

st.set_page_config(layout="wide")

df_accidents = pd.read_csv('data/accidentologie0.csv', sep=';')

df_accidents[['latitude', 'longitude']] = df_accidents['Coordonnées'].str.split(',', expand=True)
df_accidents['latitude'] = df_accidents['latitude'].astype(float)
df_accidents['longitude'] = df_accidents['longitude'].astype(float)

mode_translation = {
    '2 Roues Motorisées': 'Motorized 2 Wheels',
    'Piéton': 'Pedestrian',
    '4 Roues': '4 Wheels',
    'Vélo': 'Bicycle',
    'EDP-m': 'Motorized Personal Transport Devices',
    'Autres': 'Other'
}

age_group_translation = {
    '0-13 ans': '0-13 years',
    '14-17ans': '14-17 years',
    '18-24 ans': '18-24 years',
    '25-34 ans': '25-34 years',
    '35-44 ans': '35-44 years',
    '45-54 ans': '45-54 years',
    '55-64 ans': '55-64 years',
    '65-74 ans': '65-74 years',
    '75 ans et +': '75 years and over'
}

df_accidents['Mode'] = df_accidents['Mode'].map(mode_translation)
df_accidents["Tranche d'age"] = df_accidents["Tranche d'age"].map(age_group_translation)

# Assume you have latitude and longitude for the center of each arrondissement in the df_agg DataFrame.
# Start your Streamlit app.
st.title('Accidents in Paris')


st.write("Filter by Age Group")
selected_age_brackets = st.radio(
    "Select Age Group",
    ['All'] + sorted(df_accidents["Tranche d'age"].dropna().unique().tolist()), horizontal=True
)

# Set up the map
col1, col2 = st.columns([6,6])

# Filter the data
if selected_age_brackets != 'All':
    df_accidents = df_accidents[df_accidents["Tranche d'age"] == selected_age_brackets]

# Aggregate data for the map
agg_data = df_accidents.groupby('Arrondissement').agg({
    'latitude': 'mean',  # Compute the mean latitude for each arrondissement
    'longitude': 'mean',  # Compute the mean longitude for each arrondissement
    'IdUsager': 'count'  # Count the number of accidents in each arrondissement
}).reset_index()

def calculate_color(number_of_accidents, max_accidents):
    # Convert the number of accidents to a color
    # Green (few accidents): [0, 128, 0, 255]
    # Red (many accidents): [240, 100, 0, 255]
    red_to_yellow = 255 * (1 - (number_of_accidents / max_accidents))
    return [255, red_to_yellow, 0, 255]

# Calculate the maximum number of accidents for color scaling
max_accidents = agg_data['IdUsager'].max()

# Add a color column to your DataFrame
agg_data['color'] = agg_data['IdUsager'].apply(lambda x: calculate_color(x, max_accidents))

# Set up PyDeck layer with the point colors determined by 'IdUsager'
scatterplot_layer = pdk.Layer(
    "ScatterplotLayer",
    agg_data,
    get_position=["longitude", "latitude"],
    get_color = 'color',
    get_radius=500,  # Fixed radius for all points
    pickable=True,
    auto_highlight=True,
)

agg_data['IdUsagertext'] = agg_data['IdUsager'].apply(str)

text_layer = pdk.Layer(
    "TextLayer",
    agg_data,
    get_position='[longitude, latitude]',
    get_text='IdUsagertext',
    get_color=[0, 0, 0, 255],  # Black text
    get_size=10,
    get_alignment_baseline="'bottom'",
)

# Set the initial view state for the PyDeck map
view_state = pdk.ViewState(
    latitude=agg_data['latitude'].mean(),
    longitude=agg_data['longitude'].mean(),
    zoom=11
)

# Assuming df['Mode'] contains the mode of transport or cause of the accidents
mode_count = df_accidents['Mode'].value_counts().reset_index()
mode_count.columns = ['Mode', 'Count']

fig = px.pie(mode_count, names='Mode', values='Count')

# Update the layout to add a legend, if it's not displaying by default
fig.update_layout(legend=dict(
    title="Modes",
    orientation="v",  # Vertical legend
    y=0.5,  # Center the legend vertically
    x=1.05,  # Place the legend to the right of the chart
    xanchor="left",  # Anchor the legend to the left of its x-position
    yanchor="middle",  # Anchor the legend to the middle of its y-position
),
    width=500,  # Adjust the width as needed
    height=500,  # Adjust the height as needed
    margin=dict(l=0, r=0, t=0, b=0),  # You can adjust margins if needed
)

# Column for the map
with col1:
    st.write("Map of Accidents")
    st.pydeck_chart(pdk.Deck(
        layers=[scatterplot_layer,text_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9'
    ))


# Column for the bar chart
with col2:
    st.write("Distribution of Accident Modes")
    
    # Create the pie chart using Plotly Express
    st.plotly_chart(fig)