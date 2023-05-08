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

import utils

seaborn.set(style='ticks', context="talk")
#plt.style.use("dark_background")
custom_style = {'axes.labelcolor': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white'}
seaborn.set_style("dark", rc=custom_style)


st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")


with st.container():
    st.write("---")
    st.header("Geographical display of the Belgium Air Quality :flag-be:")
    st.write("##")
    text_column, plot_column = st.columns((1,1))

    with text_column:
        st.write("##")

        allp = ['co', 'no2', 'o3', 'pm10', 'pm25', 'so2']
        options_titles = {'co':'$CO$', 'no2':"$NO_2$", "o3":"$O_3$", "pm10":"$PM10$", "pm25":"$PM2.5$", "so2":"$SO_2$"}

        p = st.selectbox('Select an air quality parameter:',
                options = [p.upper() for p in allp])
        p = p.lower()
        ptitle = options_titles[p]

        time_str = st.selectbox("average over last $N$ days:",
                options = ["all time", "last 3 days", "last 3 hours"])
        time_options = {"all time":None, "last 3 days":3*24, "last 3 hours":3}
        time_hrs = time_options[time_str]

        data = utils.get_data(p, time_hrs)
        if data:
            sel_data, metadata = data
            st.write(f"read {metadata['n']:d} measurements from {len(sel_data):d} unique locations")
        else:
            st.write("no data available within this time window")

    with plot_column:

        if data is None:
            st.write("No data to display")
        else:
            #sel_data = [dat for dat in data if dat['parameter']==p]
            X = [ dat['longitude'] for dat in sel_data.values()]
            Y = [ dat['latitude'] for dat in sel_data.values()]
            C = [ dat['avg'] for dat in sel_data.values()]

            BE = utils.get_belgium()

            # use a map from green to red for air quality
            cmap = seaborn.color_palette("blend:green,red", n_colors=20, as_cmap=True)

            ## ---- matplotlib figure ----
            fig, ax = plt.subplots(facecolor="#0E1117")

            BE["geometry"].plot(ax=ax, facecolor='ghostwhite', edgecolor='orange', lw=1)
            p = ax.scatter(X,Y, c=C, alpha=0.1, s=100, cmap=cmap)

            # set colorbar but neglect transparancy
            cb = fig.colorbar(p, fraction=0.1, pad=-0.01)
            cb.set_alpha(1)
            cb.draw_all()
            cb.set_label(metadata['unit'])
            #fig.colorbar(p)

            ax.set_axis_off()
            plt.ylim([49.5,51.6])
            #ax.set_aspect("equal")
            ax.set_aspect(1.4)

            plt.title(f"{ptitle} concentrations in Belgium", color='white')

            plt.tight_layout()
            plt.figure(facecolor="#0E1117")
            fig.patch.set_facecolor('#0E1117')

            st.pyplot(fig, use_container_width=True)

