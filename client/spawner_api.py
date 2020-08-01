import requests
import json
import pandas as pd
import streamlit as st
import config

config = config.Settings()

SPAWNER_API = config.API_URL
headers = {"spawner-api-key": None, 'content-type': 'application/json'}


def list_containers(password):
    headers["spawner-api-key"] = password
    data = pd.DataFrame(columns=['camera_id', 'container_id'])
    response = requests.get(url=SPAWNER_API+'containers/list', headers=headers).json()

    data['camera_id'] = response['camera_ids']
    data['container_id'] = response['container_ids']

    return data


def list_cameras(password):
    headers["X-API-KEY"] = password
    data = pd.DataFrame(columns=['camera_id'])
    response = requests.get(url=SPAWNER_API + 'cameras/info/all/cam_id', headers=headers).json()
    data['camera_id'] = response
    return data


def register_camera(password, camera_id, camera_url, entry_points=None, floor_points=None, info="information"):
    headers["X-API-KEY"] = password

    body = json.dumps({"cam_id": camera_id, "cam_url": camera_url,
                       "entry_points": entry_points, "floor_points": floor_points, "info": info})

    response = requests.post(url=SPAWNER_API+'cameras/register', headers=headers, data=body)

    # print(response.json())

    return response.json()


def camera_info(password, camera_id: str):
    headers["X-API-KEY"] = password

    body = json.dumps({"cam_id": camera_id})
    response = requests.get(url=SPAWNER_API + 'cameras/info/'+camera_id, headers=headers).json()

    return response


def delete_camera(password, camera_id: str):
    headers["X-API-KEY"] = password
    response = requests.get(url=SPAWNER_API + 'cameras/delete/'+camera_id, headers=headers).json()

    if "message" in response.keys():
        return response["message"]
    else:
        return None


def container_start(password, camera_id, process_stack):
    headers["X-API-KEY"] = password
    body = json.dumps({"cam_id": camera_id, "process_stack": '#'.join(process_stack)})
    response = requests.post(url=SPAWNER_API + 'containers/start/'+camera_id, headers=headers, data=body).text

    return response
