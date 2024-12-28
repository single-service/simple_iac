import streamlit as st
from streamlit_modal import Modal
from streamlit_extras.row import row as flex_row
from code_editor import code_editor

from widgets.apps_list import AppsView
from services.environment_service import EnvironmentService



view = AppsView()
view.view()

if view.env_modal.is_open():
    with view.env_modal.container():
        app_index = st.session_state.get("edit_env_app_index")
        app_name = view.get_data_func()[app_index].name
        is_create = True
        st.write(f"App: {app_name}")

        env_index = st.session_state.get("edit_env_env_index")
        if env_index is not None:
            is_create = False
        file_name_value = None
        variables_value = None

        if not is_create:
            file_name_value = EnvironmentService.env_file_name(app_name, env_index)
            variables_value = EnvironmentService.env_file_data(app_name, file_name_value)

        file_name = st.text_input(label="env file name", value=file_name_value)
        variables = st.text_area(label="environment variables", value=variables_value)
        buttons_row = flex_row(2)
        save_btn = buttons_row.button(label="Сохранить", type="primary", use_container_width=True)
        cancel_btn = buttons_row.button(label="Отмена", use_container_width=True)
        if cancel_btn:
            del st.session_state["edit_env_app_index"]
            if not is_create:
                del st.session_state["edit_env_env_index"]
            view.env_modal.close()
        if save_btn:
            if not file_name:
                st.error("env file name is required")
            else:
                if not variables:
                    st.error("env variables are required")
                else:
                    # проверить наличие такого файла
                    if is_create:
                        is_exist = EnvironmentService.check_environment_file_exists(app_name, file_name)
                        if is_exist:
                            st.error("env variables is already exist")
                        else:
                            EnvironmentService.create_environment_file(app_name, file_name, variables)
                            view.env_modal.close()
                    else:
                        if file_name_value != file_name:
                            is_exist = EnvironmentService.check_environment_file_exists(file_name)
                            if is_exist:
                                st.error("env variables is already exist")
                            else:
                                EnvironmentService.create_environment_file(app_name, file_name, variables)
                                view.env_modal.close()
                        else:
                            EnvironmentService.create_environment_file(app_name, file_name, variables)
                            view.env_modal.close()


if view.file_modal.is_open():
    with view.file_modal.container():
        path = st.session_state["file_modal_filename"]
        filedata = ""
        with open(path, "r") as compose_file:
            filedata = compose_file.read()
        st.write(f"Файл: {path}")
        new_file_data = st.text_area(label="content", value=filedata, height=500)
        buttons_row = flex_row(2)
        save_btn = buttons_row.button(label="Сохранить", type="primary", use_container_width=True)
        cancel_btn = buttons_row.button(label="Отмена", use_container_width=True)
        if cancel_btn:
            del st.session_state["file_modal_filename"]
            view.file_modal.close()
        if save_btn:
            with open(path, "w") as compose_file:
                compose_file.write(new_file_data)
            view.file_modal.close()
