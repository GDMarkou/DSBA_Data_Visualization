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

# Initialize Session State for Page Navigation if it's not already set
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Sidebar for Navigation
with st.sidebar:
    st.title('Paris Incident Exploration🗼')
    # Radio buttons for page navigation
    page = st.radio("Select a page to explore", ('Introduction', 'Paris Road Accident', 'Seasonality Map', 'Analytics'))

# Data Loading
accidents = pd.read_csv("/Users/oscarmeurer/Downloads/accidentologie0.csv", sep=";")

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


# Page One. This is the Introduction page here we will give a brief overview like we did in the
if page == 'Introduction':
    st.title("Welcome to the Paris Incident Explorer! 🥐🚗🏍️")
    st.text("In this dashboard, we present to you the accidents that occurred in Paris.")
    st.write(accidents)  # Example of displaying a dataframe

elif page == 'Seasonality Map':
    st.title("Seasonality Map")
    st.text("In this dashboard, we present to you the an interactive map that displays for each month and the selected age group .")

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

elif page == 'Analytics':
    st.title("Analytics on Accident Data")

    # Aggregating Data
    agg_data = accidents.groupby(['Year', 'Mode']).size().reset_index(name='Count')

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
