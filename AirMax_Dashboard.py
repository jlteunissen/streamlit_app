import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image

import boto3
from boto3.dynamodb.conditions import Key, Attr

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import geopandas

import time as time_module


seaborn.set(style='ticks', context="talk")
#plt.style.use("dark_background")
custom_style = {'axes.labelcolor': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white'}
seaborn.set_style("dark", rc=custom_style)

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="AirMax Dashboard", page_icon=":wind_blowing_face:", layout="wide")

st.sidebar.success("Select a demo above.")




def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# ---- LOAD ASSETS ----
#lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_coding = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_YZrGzO2pAP.json")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")

# ---- HEADER SECTION ----
with st.container():
    st.title("Welcome at AirMax :wave:")
    st.subheader("Atmosphere control for Belgium")

# ---- WHAT WE DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What we do")
        st.write("##")
        st.write(
            "We are passionate about air quality"
        )
        st.write("[Learn More >](https://www.airmax.nu/)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")


