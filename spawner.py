import streamlit as st
import time
import st_state_patch
from client import spawner_api
import config

config = config.Settings()

# Creating a session
session = st.State()
if not session:
    session.authenticated = False
    session.api_key = None


def auth():
    """Authentication

    :return:
    """
    if session.authenticated:
        return True
    textInputBlock = st.empty()
    password = textInputBlock.text_input(label='Enter Password', type='password')
    if password:
        if password == config.API_KEY:
            infoBlock = st.success("Authorization complete")
            session.api_key = config.API_KEY
            session.authenticated = True
            time.sleep(.5)
            # Clearing screen
            infoBlock.empty()
            textInputBlock.empty()
        else:
            st.error("Password Incorrect")
    else:
        st.error("Password Required")


def display_running_cams(block):
    """Running camera containers

    :param block:
    :return:
    """
    block.empty()  # clearing existing data
    data = spawner_api.list_containers(session.api_key)
    if not data.empty:
        block.table(data.assign(hack='').set_index('hack'))
    else:
        st.error('No running cameras found')


# Running Cameras
def show_running_cameras():
    """Show running cameras

    :return:
    """
    st.write('# Running cameras')
    block = st.empty()
    block.info('Please Refresh')
    runningCameraBlock = st.empty()  # Placeholder for the table
    if st.sidebar.button('Refresh Data'):
        block.empty()
        display_running_cams(runningCameraBlock)


def register_camera():
    """Camera registration

    :return:
    """
    st.write('# Register Camera')
    camera_id = st.text_input(label='Enter Camera ID')
    camera_url = st.text_input(label='Enter Camera URL')
    info = st.text_input(label='Any information regarding the camera')

    entry_points = st.text_input(label='Entry Points')
    st.write("> ###### Entry points, *follow this format* `223#556#330#100` from line start to stop")
    
    floor_points = st.text_input(label='Floor Points')
    st.write("> ###### Floor points, *follow this format* "
             "`223#556#330#100#223#556#330#100` from lower right in clockwise")

    if st.button(label='Register'):
        # REGISTER CAMERA
        msg = spawner_api.register_camera(session.api_key, camera_id, camera_url, entry_points, floor_points, info)
        st.json(msg)


def list_cameras():
    """List registered cameras

    :return:
    """
    block = st.empty()
    data = spawner_api.list_cameras(session.api_key)

    block.table(data.assign(hack='').set_index('hack'))
    if st.sidebar.button("Reload Data"):
        block.empty()
        data = spawner_api.list_cameras(session.api_key)
        block.table(data.assign(hack='').set_index('hack'))
    st.write("## Camera Info")
    cam_id = st.text_input(label='Camera ID')
    if cam_id:
        response = spawner_api.camera_info(session.api_key, cam_id)
        st.json(response)


def delete_cameras():
    """Delete camera

    :return:
    """
    cam_id_ = st.text_input(label="Enter Camera ID. 'ALL' to delete all keys")
    if st.button(label="Delete"):
        msg = spawner_api.delete_camera(session.api_key, cam_id_)
        st.success(msg)


def start_process():
    """Strt camera container

    :return:
    """

    cam_id = st.text_input(label='Camera ID')
    if cam_id:
        response = spawner_api.camera_info(session.api_key, cam_id)
        st.write("## Camera Info")
        st.json(response)

        st.write('## Select process stack')
        process_stack = []
        if st.checkbox(label='Entry/Exit'):
            process_stack.append('person_counter')

        if st.checkbox(label='Socail Distancing'):
            process_stack.append('social_distancing')

        if st.checkbox(label='Config override'):
            # config = st.text_input(label='Enter configuration')
            st.write("##### Configuration to override default, *follow this format*")
            st.write(''' > `{ "nms_threshold": 0.5, "confidence_thresh": 0.4}` ''')

        st.write("## Current Selection")
        st.write(process_stack)
        if st.button("Start Process"):
            process_stack = '#'.join(process_stack)
            response = spawner_api.container_start(session.api_key, cam_id, process_stack, stable=True)
            st.code(response)

    else:
        st.error('Please enter camera-id')

def get_logs():
    st.write("# Log Viewer")
    container_id_input = st.text_input("Enter Container ID")
    block = st.empty()
    if container_id_input:
        view_mode = st.sidebar.radio("Select Viewing Mode",
        ('View All Logs', 'View Logs By Lines', 'View Latest'))
        data = spawner_api.container_logs(session.api_key, container_id_input)
        if view_mode == 'View All Logs':
            block.write(data['logs_raw'])
        elif view_mode == 'View Logs By Lines':
            block.write(data['logs_lines'])
        elif view_mode == 'View Latest':
            block.write(data['logs_latest'])
    
    
def main():
    if session.authenticated:
        st.sidebar.title("Argus Spawner API")
        appMode = st.sidebar.selectbox("Choose the app mode",
                                       ["Show Running Cameras", "Register A Camera", "Manage Cameras", "Log Viewer"])

        if appMode == 'Show Running Cameras':
            show_running_cameras()
        elif appMode == 'Register A Camera':
            register_camera()
        elif appMode == 'Manage Cameras':
            manageOption = st.sidebar.radio("Select an option",
                                            ('List Cameras', 'Delete Cameras', 'Start A Process'))
            st.write('# Manage Cameras')
            if manageOption == 'List Cameras':
                st.write('## List all registered cameras')
                list_cameras()
            elif manageOption == 'Delete Cameras':
                st.write('## Delete Cameras')
                delete_cameras()
            elif manageOption == 'Start A Process':
                # st.write("## Start A Process")
                start_process()
        elif appMode == 'Log Viewer':
            get_logs()


# Authentication
auth()
# Main Program
main()
