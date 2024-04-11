import streamlit as st
import pandas as pd
from data.get_data import *
import altair as alt
import plotly.express as px
import numpy as np

accidents = pd.read_csv("/Users/oscarmeurer/Downloads/accidentologie0.csv", sep=";")

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

    data['Age_Group'] = data['Age'].apply(create_age_group)

    return data

accidents = create_age_groups(accidents)

accidents['Date'] = pd.to_datetime(accidents['Date'])
accidents['Month'] = accidents['Date'].dt.month

def animate_map(time_col):
    fig = px.density_mapbox(accidents,
              lat="Latitude" ,
              lon="Longitude",
              #hover_name="TYPE",
              #color="TYPE",
              animation_frame=time_col,
              mapbox_style='carto-positron',
              category_orders={
              time_col:list(np.sort(accidents[time_col].unique()))
              },                  
              zoom=10)
    fig.show()

animate_map(time_col='Month')