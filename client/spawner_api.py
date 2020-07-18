import requests
import json
import pandas as pd
import streamlit as st

SPAWNER_API = "http://cvision-516524912.us-east-1.elb.amazonaws.com/spawner-api/"
headers = {"X-API-KEY": "cvision2020", 'content-type': 'application/json'}


def list_containers():
    data = pd.DataFrame(columns=['camera_id', 'container_id'])
    response = requests.get(url=SPAWNER_API+'container_list', headers=headers).json()

    data['camera_id'] = response['cam_running']
    data['container_id'] = response['container_ids']

    return data


@st.cache
def list_cameras():
    data = pd.DataFrame(columns=['camera_id'])
    response = requests.get(url=SPAWNER_API + 'register_camera', headers=headers).json()
    data['camera_id'] = response['registered_cameras']
    return data


@st.cache
def register_camera(camera_id, camera_url, start, stop, info):
    entry_points = start + '#' + stop

    body = json.dumps({"cam_id": camera_id, "cam_url": camera_url, "entry_points": entry_points, "info": info})

    response = requests.post(url=SPAWNER_API+'register_camera', headers=headers, data=body)

    # print(response.json())

    return response.json()


@st.cache
def camera_info(camera_id):

    body = json.dumps({"cam_id": camera_id})
    response = requests.post(url=SPAWNER_API + 'camera_info', headers=headers, data=body).json()

    return response


def container_start(camera_id):
    body = json.dumps({"cam_id": camera_id})
    response = requests.post(url=SPAWNER_API + 'container_start', headers=headers, data=body).text

    return response
