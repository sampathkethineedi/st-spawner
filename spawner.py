import streamlit as st
from client.spawner_api import list_containers, list_cameras, register_camera, camera_info, container_start


st.write('## Running cameras')
data = list_containers()
st.table(data.assign(hack='').set_index('hack'))

st.write('## Register Camera')
if st.checkbox('register'):
    camera_id = st.text_input(label='Enter Camera ID')
    camera_url = st.text_input(label='Enter Camera URL')
    info = st.text_input(label='Any information regarding the camera')

    st.write("### Entry points, *follow this format* `223#556`")
    start = st.text_input(label='start')
    stop = st.text_input(label='stop')

    if st.button(label='Register'):
        msg = register_camera(camera_id, camera_url, start, stop, info)
        st.json(msg)

st.write('## Start Camera process')
if st.checkbox('start'):

    if st.button("Show registered cameras"):
        data = list_cameras()
        st.table(data.assign(hack='').set_index('hack'))

    cam_id = st.text_input(label='Camera ID')

    if st.button("Show camera info"):
        response = camera_info(cam_id)
        st.json(response)

    st.write('Select process stack')
    process_stack = []
    if st.checkbox(label='Entry/Exit'):
        process_stack.append('person_counter')

    if st.checkbox(label='Socail Distancing'):
        process_stack.append('social_distancing')

    if st.checkbox(label='Config override'):
        st.write("### Configuration to override default, *follow this format*")
        st.write('`{ "nms_threshold": 0.5, "confidence_thresh": 0.4}`')
        config = st.text_input(label='config')

    if st.checkbox("Show Selection"):
        for p in process_stack:
            st.text(p)

    if st.button("Start Process"):
        response = container_start(cam_id)
        st.code(response)
