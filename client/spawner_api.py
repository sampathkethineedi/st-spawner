import requests
import json
import pandas as pd
import config

config = config.Settings()

SPAWNER_API = config.API_URL

headers = {"spawner-api-key": None, 'content-type': 'application/json'}


# CAMERA FUNCTIONALITY
def list_cameras(api_key: str):
    """List registered cameras

    :param api_key: api key
    :return: dataframe with cam ids
    """
    headers["spawner-api-key"] = api_key
    data = pd.DataFrame(columns=['camera_id'])
    response = requests.get(url=SPAWNER_API + 'cameras/info/all/cam_id', headers=headers).json()
    data['camera_id'] = response
    return data


def register_camera(api_key: str, camera_id: str, camera_url: str,
                    entry_points: str = None, floor_points: str = None, info: str = "Information about the camera"):
    """Register camera

    :param api_key:
    :param camera_id:
    :param camera_url:
    :param entry_points:
    :param floor_points:
    :param info:
    :return: api response
    """

    headers["spawner-api-key"] = api_key

    body = json.dumps({"cam_id": camera_id, "cam_url": camera_url,
                       "entry_points": entry_points, "floor_points": floor_points, "info": info})

    response = requests.post(url=SPAWNER_API+'cameras/register', headers=headers, data=body)

    return response.json()


def camera_info(api_key: str, camera_id: str):
    """Information about a registered camera

    :param api_key:
    :param camera_id:
    :return:
    """

    headers["spawner-api-key"] = api_key

    response = requests.get(url=SPAWNER_API + 'cameras/info/'+camera_id, headers=headers).json()

    return response


def delete_camera(api_key: str, camera_id: str):
    headers["spawner-api-key"] = api_key
    response = requests.get(url=SPAWNER_API + 'cameras/delete/'+camera_id, headers=headers).json()

    if "message" in response.keys():
        return response["message"]
    else:
        return "Error deleting the camera info"


# CONTAINER FUNCTIONALITY
def list_containers(api_key: str):
    """List running containers

    :param api_key:
    :return:
    """
    headers["spawner-api-key"] = api_key
    data = pd.DataFrame(columns=['camera_id', 'container_id'])
    response = requests.get(url=SPAWNER_API+'containers/list', headers=headers).json()
    data['camera_id'] = response['camera_ids']
    data['container_id'] = response['container_ids']

    return data


def container_start(api_key: str, camera_id: str):
    """Start a container process for a registered camera

    :param api_key:
    :param camera_id:
    :return:
    """
    headers["spawner-api-key"] = api_key
    response = requests.get(url=SPAWNER_API + 'containers/start/'+camera_id, headers=headers,).text

    return response
