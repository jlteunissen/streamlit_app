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


def run_dynamo_query(parameter, time):
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

    return response


def aggregate_response(response):
    metadata = {'unit': response["Items"][0]["unit"]}

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


@st.cache_data
def get_data(parameter, time=None):
    """ time units is in hours, if None all database entries are used """

    response = run_dynamo_query(parameter, time)

    if len(response["Items"])==0:
        return None
    else:
        return aggregate_response(response)


def get_belgium():
    BE = geopandas.read_file("./BEL_adm2.shp")
    return BE

