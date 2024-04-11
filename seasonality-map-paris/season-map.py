import streamlit as st
import pandas as pd
from data.get_data import *
import altair as alt
import plotly.express as px

accidents = pd.read_csv("/Users/oscarmeurer/Downloads/accidentologie0.csv", sep=";")

print(accidents.columns)

def create_age_groups(accidents):

    data = accidents.copy()
    def create_age_group(age):
        if age <= 18:
            return '0-18'
        elif 19 <= age <= 25:
            return '19-25'
        elif 26 <= age <= 35:
            return '26-35'
        elif 36 <= age <= 45:
            return '36-45'
        elif 46 <= age <= 55:
            return '46-55'
        elif 56 <= age <= 65:
            return '56-65'
        else:
            return '65+'

    # Assuming your DataFrame is called 'accidents' and it contains an 'Age' column
    data['Age_Group'] = data['Age'].apply(create_age_group)

    return data


accidents=create_age_groups(accidents)
print(accidents.head())

# Convert 'Date' column to datetime if it's not already in datetime format
accidents['Date'] = pd.to_datetime(accidents['Date'])

# Extract month from 'Date' column
accidents['Month'] = accidents['Date'].dt.month
# Assuming you have latitude and longitude columns in your dataset
fig = px.density_mapbox(accidents, lat='Latitude', lon='Longitude', z='Month', radius=10,
                         center=dict(lat=48.8566, lon=2.3522), zoom=10,
                         mapbox_style="stamen-terrain", animation_frame='Month',
                         title="Accident Heatmap by Month in Paris")

# Update layout to include age bucket selection
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(label="0-18",
                     method="update",
                     args=[{"visible": [True if age_group == '0-18' else False for age_group in accidents['Age_Group']]}]),
                dict(label="19-25",
                     method="update",
                     args=[{"visible": [True if age_group == '19-25' else False for age_group in accidents['Age_Group']]}]),
                dict(label="26-35",
                     method="update",
                     args=[{"visible": [True if age_group == '26-35' else False for age_group in accidents['Age_Group']]}]),
                dict(label="36-45",
                     method="update",
                     args=[{"visible": [True if age_group == '36-45' else False for age_group in accidents['Age_Group']]}]),
                dict(label="46-55",
                     method="update",
                     args=[{"visible": [True if age_group == '46-55' else False for age_group in accidents['Age_Group']]}]),
                dict(label="56-65",
                     method="update",
                     args=[{"visible": [True if age_group == '56-65' else False for age_group in accidents['Age_Group']]}]),
                dict(label="65+",
                     method="update",
                     args=[{"visible": [True if age_group == '65+' else False for age_group in accidents['Age_Group']]}]),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=0.9,
            yanchor="top"
        ),
    ]
)

fig.update_xaxes(type='category')  # Ensure months are treated as categories for ordering

fig.show()