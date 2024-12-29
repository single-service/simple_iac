import streamlit as st
from streamlit_extras.row import row as flex_row
from streamlit_modal import Modal

from widgets.abstract import TableView
from services.server_service import ServerService


class ServersView(TableView):

    def __init__(self):
        self.headers = [
            "№", "Name", "IP", "Port", "Login", "Password", "Is swarm",
            "is_master_node", "swarm_parent", "install_nginx", ""
        ]
        self.instance_name = "сервер"
        self.instance_name_plural = "серверов"
        self.data_fields = {
            "name": "text",
            "ip": "text",
            "port": "text",
            "login": "text",
            "password": "text",
            "is_swarm": "bool",
            "is_master_node": "bool",
            "swarm_parent": "text",
            "install_nginx": "bool"
        }
        self.title = "Серверы"
        self.view_name = "server"
        self.add_func = ServerService.add_server
        self.get_data_func = ServerService.get_config
        self.del_func =  ServerService.del_server
        self.update_func = ServerService.update_server

