import streamlit as st
from streamlit_modal import Modal
from streamlit_extras.row import row as flex_row

from widgets.abstract import TableView
from services.apps import AppsService


class AppsView(TableView):

    def __init__(self):
        self.headers = [
            "№", "Name", "Docker Compose", "Dest path", "is_swarm", "Swarm stack", "Server", "Environments", ""
        ]
        self.instance_name = "приложение"
        self.instance_name_plural = "приложений"
        self.data_fields = {
            "name": "text",
            "local_path": "file",
            "dest_path": "text",
            "is_swarm": "bool",
            "swarm_stack": "text",
            "server": "text",
            "environments": ("custom", self.environments_field)
        }
        self.title = "Приложения"
        self.view_name = "application"
        self.add_func = AppsService.add_app
        self.get_data_func = AppsService.get_config
        self.del_func =  AppsService.del_app
        self.update_func = AppsService.update_app

        self.env_modal = Modal(
            f"Добавить env", 
            key="env_modal",
            padding=20,
            max_width=744
        )

        self.docker_compose_modal = Modal(
            f"Изменить docker compose", 
            key="docker_compose_modal",
            padding=20,
            max_width=744
        )

    def environments_field(self, params, column):
        envs = params["value"]
        if envs is None:
            envs = []
        for i, env in enumerate(envs):
            edit_env_btn = column.button(label=env, key=f"app_env_{i}", type="tertiary", args=[params["args"][1], i])
            if edit_env_btn:
                st.session_state["edit_env_app_index"] = params["args"][1]
                st.session_state["edit_env_env_index"] = i
                self.env_modal.open()
                st.rerun()
        add_env_btn = column.button(label="Add env", type="secondary", key=params["key"])
        if add_env_btn:
            st.session_state["edit_env_app_index"] = params["args"][1]
            self.env_modal.open()
            st.rerun()

    def docker_compose_field(self, params, column):
        local_path = params["value"]
        st.write(local_path)
