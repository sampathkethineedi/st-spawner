import streamlit as st
from client.spawner_api import list_containers, list_cameras, register_camera, camera_info, container_start, delete_camera


password = st.text_input(label='Enter Password')

if password:

    if password == "cvision2020":

        st.success("Authorization complete")
        st.write('## Running cameras')

        # LIST CONTAINERS
        data = list_containers(password)
        st.table(data.assign(hack='').set_index('hack'))

        st.write('## Register Camera')
        if st.checkbox('register'):
            camera_id = st.text_input(label='Enter Camera ID')
            camera_url = st.text_input(label='Enter Camera URL')
            info = st.text_input(label='Any information regarding the camera')

            st.write("### Entry points, *follow this format* `223#556#330#100` from line start to stop")
            entry_points = st.text_input(label='entry_points')

            st.write("### Floor points, *follow this format* `223#556#330#100#223#556#330#100` from lower right in clockwise")
            floor_points = st.text_input(label='floor_points')

            if st.button(label='Register'):
                # REGISTER CAMERA
                msg = register_camera(password, camera_id, camera_url, entry_points, floor_points, info)
                st.json(msg)

        st.write('## Start Camera process')
        if st.checkbox('start'):
            # LIST CAMERAS
            if st.button("Show registered cameras"):
                data = list_cameras(password)
                st.table(data.assign(hack='').set_index('hack'))

            # DELETE CAMERAS
            if st.checkbox("Delete camera"):
                st.write("### Camera id to delete. Enter ALL to delete all keys")
                cam_id_ = st.text_input(label='Enter Camera ID for delete')
                if st.button(label="Delete"):
                    msg = delete_camera(password, cam_id_)
                    st.success(msg)

            st.write("## Start Process")
            cam_id = st.text_input(label='Camera ID')

            if st.button("Show camera info"):
                response = camera_info(password, cam_id)
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
                response = container_start(password, cam_id)
                st.code(response)
    else:
        st.error("Password incorrect")
else:
    st.error("Password required")
