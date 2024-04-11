import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


st.set_page_config(
    page_title="Paris Road Accidents",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.write("Hello word")