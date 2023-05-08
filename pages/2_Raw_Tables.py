import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image

from collections import Counter
import numpy as np
import time as time_module
import pandas as pd

import utils

st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

with st.container():
    st.write("---")
    st.header("Tables display of the Belgium Air Quality :flag-be:")
    st.write("##")

    allp = ['co', 'no2', 'o3', 'pm10', 'pm25', 'so2']
    options_titles = {'co':'$CO$', 'no2':"$NO_2$", "o3":"$O_3$", "pm10":"$PM10$", "pm25":"$PM2.5$", "so2":"$SO_2$"}

    p = st.selectbox('Select an air quality parameter:',
            options = [p.upper() for p in allp])
    p = p.lower()
    ptitle = options_titles[p]

    time_str = st.selectbox("select only records from:",
            options = ["all time", "last 3 days", "last 3 hours"])
    time_options = {"all time":None, "last 3 days":3*24, "last 3 hours":3}
    time_hrs = time_options[time_str]

    if data := utils.run_dynamo_query(p, time_hrs)["Items"]:
        st.write(f"read {len(data):d} measurements")
        dfraw = pd.json_normalize(data)
        df = dfraw.drop(["parameter_location", "date_utc", "country", "epoch"], axis=1)

        # different display options
        # 1. whole table
        st.write(df)
        # 2. counts of values
        st.write("value counts per location")
        c = df["location"].value_counts()
        st.write(c)
    else:
        st.write("no data available within this time window")


