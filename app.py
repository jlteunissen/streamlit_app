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
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
#def local_css(file_name):
#    with open(file_name) as f:
#        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


#local_css("style/style.css")

# ---- LOAD ASSETS ----
#lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_coding = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_YZrGzO2pAP.json")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Welcome at AirMax :wave:")
    st.title("atmosphere control")
    st.write(
        "We are passionate about air quality"
    )
    st.write("[Learn More >](https://www.airmax.nu/)")

# ---- WHAT I DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What we do")
        st.write("##")
        st.write(
            """
            On my YouTube channel I am creating tutorials for people who:
            - are looking for a way to leverage the power of Python in their day-to-day work.
            - are struggling with repetitive tasks in Excel and are looking for a way to use Python and VBA.
            - want to learn Data Analysis & Data Science to perform meaningful and impactful analyses.
            - are working with Excel and found themselves thinking - "there has to be a better way."

            If this sounds interesting to you, consider subscribing and turning on the notifications, so you don’t miss any content.
            """
        )
        st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")


@st.cache_data
def get_data(parameter, time=None):
    """ time units is in hours, if None all database entries are used """

    dyn = boto3.resource("dynamodb")
    table_name = "OpenAQ_Jos"
    table = dyn.Table(table_name)

    if time is None:
        response = table.query(
            IndexName = "parameter-epoch-index",
            KeyConditionExpression=Key('parameter').eq(parameter)
        )
    else:
        time_epoch = int(time_module.time()) - time*3600
        response = table.query(
            IndexName = "parameter-epoch-index",
            KeyConditionExpression=Key('parameter').eq(parameter) & Key('epoch').gt(time_epoch)
        )

    if len(response["Items"])==0:
        return None

    metadata = {'unit': response["Items"][0]["unit"] }
    ## aggregate multiple measurements from same location
    aggregated_data = dict()
    for item in response["Items"]:
        key = item["parameter_location"]
        if key in aggregated_data:
            aggregated_data[key]['values'].append(float(item['value']))
        else:
            new_item = {k:float(v) for k,v in item.items() if k in ['latitude', 'longitude']}
            new_item['values'] = [float(item['value'])]
            aggregated_data[item["parameter_location"]] = new_item

    ## add averages
    n = 0
    for key in aggregated_data:
        entry = aggregated_data[key]
        n += len(entry['values'])
        aggregated_data[key]['avg'] = np.average(entry['values'])
    metadata['n'] = n

    return aggregated_data, metadata


def get_belgium():
    BE = geopandas.read_file("./BEL_adm2.shp")
    return BE


with st.container():
    st.write("---")
    st.header("My Belgium Plots")
    st.write("##")
    text_column, plot_column = st.columns((1,1))

    #data = get_data()

    with text_column:
        st.write("##")
        st.header(":flag-be:")

        allp = ['co', 'no2', 'o3', 'pm10', 'pm25', 'so2']
        options_titles = {'co':'$CO$', 'no2':"$NO_2$", "o3":"$O_3$", "pm10":"$PM10$", "pm25":"$PM2.5$", "so2":"$SO_2$"}

        p = st.selectbox('Select an air quality parameter:',
                options = [p.upper() for p in allp])
        p = p.lower()
        ptitle = options_titles[p]

        time_str = st.selectbox("average over last $N$ days:",
                options = ["all time", "last 3 days", "last 3 hours"])
        # get time in number of hours.
        time_options = {"all time":None, "last 3 days":3*24, "last 3 hours":3}
        time_hrs = time_options[time_str]

        data = get_data(p, time_hrs)
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

            BE = get_belgium()

            # use a map from green to red for air quality
            cmap = seaborn.color_palette("blend:green,red", n_colors=20, as_cmap=True)

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

