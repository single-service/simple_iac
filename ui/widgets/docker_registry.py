import streamlit as st
from streamlit_extras.row import row as flex_row
from streamlit_modal import Modal

from widgets.abstract import TableView
from services.docker_registry import DockerRegistryService


class DockerRegistryView(TableView):

    def __init__(self):
        self.headers = [
            "№", "Name", "Url", "Login", "Password", ""
        ]
        self.instance_name = "сервер"
        self.instance_name_plural = "серверов"
        self.data_fields = {
            "name": "text",
            "url": "text",
            "login": "text",
            "password": "text",
        }
        self.title = "Docker Хранилища"
        self.view_name = "registry"
        self.add_func = DockerRegistryService.add_registry
        self.get_data_func = DockerRegistryService.get_config
        self.del_func =  DockerRegistryService.del_registry
        self.update_func = DockerRegistryService.update_registry
