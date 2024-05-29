import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# Import data
#df_mpg = pd.read_csv("data/raw/mpg.csv") #could be a problem due to cloud limitations

# Instead put the data in cache
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path="data/raw/mpg.csv")
mpg_df = deepcopy(mpg_df_raw) # ensures that the cache is not modified

# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

# Whether to show the dataset
if st.checkbox("Show dataframe"):

    # Show data as table
    st.subheader("The dataset")
    st.dataframe(data=mpg_df)

# show a plot

# first, generate
#m_fig, ax = plt.subplots(figsize=(10, 8))
#ax.scatter(mpg_df['displ'], mpg_df['hwy'], alpha=0.7)
#ax.set_title("Engine Size vs. Highway Fuel Mileage")
#ax.set_xlabel('Displacement (Liters)')
#ax.set_ylabel('MPG')

# then, display
#st.pyplot(m_fig)

# modify the plot with selected parameters

left_col, right_col = st.columns(2) # to make the select box smaller

# selecting the year, including all
years = ["All"]+sorted(pd.unique(mpg_df['year']))
year = left_col.selectbox("Choose a Year", years) # store the selected year

if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

# highlight means?
show_means = right_col.radio(
    label='Show Class Means', options=['Yes', 'No'])

means = reduced_df.groupby('class').mean(numeric_only=True)


m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)

if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7, color="red")

ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

st.pyplot(m_fig)