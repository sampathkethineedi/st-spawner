import streamlit as st
import time
import st_state_patch
from client.spawner_api import *
import config

config = config.Settings()

# Creating a session
session = st.State()
if not session:
    session.authenticated=False
    session.password=''


# Authentication Funciton
def auth():
    if session.authenticated:
        return True
    textInputBlock = st.empty()
    password = textInputBlock.text_input(label='Enter Password', type='password')
    
    if password:   
        if password == config.API_KEY:
            infoBlock = st.success("Authorization complete")
            session.password = password
            session.authenticated = True
            time.sleep(.5)
            # Clearing screen
            infoBlock.empty()
            textInputBlock.empty()
        else:
            st.error("Password Incorrect")
    else:
        st.error("Password Required")


def displayRunningCams(block):
    block.empty() # clearing existing data
    data = list_containers(session.password)
    if not data.empty :
        block.table(data.assign(hack='').set_index('hack'))
    else:
        st.error('No running cameras found')


# Running Cameras
def showRunningCameras():
    st.write('# Running cameras')
    block=st.empty()
    block.info('Please Refresh')
    runningCameraBlock = st.empty()  # Placeholder for the table
    if st.sidebar.button('Refresh Data'):
        block.empty()
        displayRunningCams(runningCameraBlock)


# Register a camera
def registerCamera():
    st.write('# Register Camera')
    camera_id = st.text_input(label='Enter Camera ID')
    camera_url = st.text_input(label='Enter Camera URL')
    info = st.text_input(label='Any information regarding the camera')

    entry_points = st.text_input(label='Entry Points')
    st.write("> ###### Entry points, *follow this format* `223#556#330#100` from line start to stop")
    
    floor_points = st.text_input(label='Floor Points')
    st.write("> ###### Floor points, *follow this format* `223#556#330#100#223#556#330#100` from lower right in clockwise")

    if st.button(label='Register'):
        # REGISTER CAMERA
        msg = register_camera(session.password, camera_id, camera_url, entry_points, floor_points, info)
        st.json(msg)


# Manage Cameras
def listCameras():
    block = st.empty()
    data = list_cameras(session.password)

    block.table(data.assign(hack='').set_index('hack'))
    if st.sidebar.button("Reload Data"):
        block.empty()
        data = list_cameras(session.password)
        block.table(data.assign(hack='').set_index('hack'))


def deleteCameras():
    cam_id_ = st.text_input(label="Enter Camera ID. 'ALL' to delete all keys")
    if st.button(label="Delete"):
        msg = delete_camera(session.password, cam_id_)
        st.success(msg)


def startProcess():

    cam_id = st.text_input(label='Camera ID')
    if cam_id:
        response = camera_info(session.password, cam_id)
        st.write("## Camera Info")
        st.json(response)

        st.write('## Select process stack')
        process_stack = []
        if st.checkbox(label='Entry/Exit'):
            process_stack.append('person_counter')

        if st.checkbox(label='Socail Distancing'):
                process_stack.append('social_distancing')

        if st.checkbox(label='Config override'):
            config = st.text_input(label='Enter configuration')
            st.write("##### Configuration to override default, *follow this format*")
            st.write(''' > `{ "nms_threshold": 0.5, "confidence_thresh": 0.4}` ''')

        st.write("## Current Selection")
        st.write(process_stack)
        if st.button("Start Process"):
            response = container_start(session.password, cam_id, process_stack)
            st.code(response)

    else: 
        st.error('Please enter camera-id')


def main():
    if session.authenticated:
        st.sidebar.title("Argus Spawner API")
        appMode = st.sidebar.selectbox("Choose the app mode",
            ["Show Running Cameras", "Register A Camera", "Manage Cameras"])
        
        if appMode =='Show Running Cameras':
            showRunningCameras()
        elif appMode =='Register A Camera':
            registerCamera()
        elif appMode == 'Manage Cameras':
            manageOption = st.sidebar.radio("Select an option",
            ('List Cameras', 'Delete Cameras', 'Start A Process'))
            st.write('# Manage Cameras')
            if manageOption=='List Cameras':
                st.write('## List all registered cameras')
                listCameras()
            elif manageOption == 'Delete Cameras':
                st.write('## Delete Cameras')
                deleteCameras()
            elif manageOption == 'Start A Process':
                #st.write("## Start A Process")
                startProcess()

# Authentication
auth()
# Main Program
main()