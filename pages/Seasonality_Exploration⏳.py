import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from data.get_data import get_data, create_age_groups
import calendar


# Page Configuration
st.set_page_config(
    page_title="Paris Accidents Exploration",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Data Loading
accidents = pd.read_csv("data/accidentologie0.csv", sep=";")

#accidents = get_data() #retrieving the data from a function in the data folder

#Preprocessing
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
accidents['Month'] = accidents['Date'].dt.month
accidents['Month_Name'] = pd.to_datetime(accidents['Month'], format='%m').dt.strftime('%B')  # Add month names

# Group by month and count the number of accidents
monthly_accidents = accidents.groupby(['Year', 'Month'])['IdUsager'].count().reset_index()
monthly_accidents.columns = ['Year', 'Month', 'Accident_Count']
monthly_accidents['Month_Name'] = monthly_accidents['Month'].apply(lambda x: calendar.month_name[x])
monthly_accidents = monthly_accidents.sort_values(by=['Year', 'Month'])



st.title("Exploration of seasonal effect on accidents")
st.text("Graph that plots for the whole year, month by month, for the selected age group, the density map of accidents.")

accidents = create_age_groups(accidents)
# Filter by age group
age_group = st.selectbox('Select Age Group', sorted(accidents['Age_Group'].unique()))
# Filter dataframe by selected age group
filtered_df = accidents[accidents['Age_Group'] == age_group]

# Sort the DataFrame monthly_accidents by month

print(monthly_accidents.head())

# Plotting the density map
fig = px.density_mapbox(filtered_df, lat='Latitude', lon='Longitude',
                        radius=10, center=dict(lat=48.8566, lon=2.3522),
                        zoom=10, mapbox_style="carto-positron",
                        animation_frame='Month_Name', title='Paris Density Map by Age Group',
                        color_continuous_scale='inferno',
                        category_orders={'Month_Name': monthly_accidents['Month_Name']})

fig.update_layout(margin=dict(b=0, t=40, l=0, r=0),
                    height=600,  # Increase height
                    width=800)  # Increase width

# Show the density map
st.plotly_chart(fig)



