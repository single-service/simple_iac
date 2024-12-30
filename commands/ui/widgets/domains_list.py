import streamlit as st
from streamlit_extras.row import row as flex_row
from streamlit_modal import Modal

from widgets.abstract import TableView
from services.domain_service import DomainService


class DomainsView(TableView):

    def __init__(self):
        self.headers = [
            "№", "Domain", "Is SSL", "Certbot Email", "Host", "Port", ""
        ]
        self.instance_name = "домен"
        self.instance_name_plural = "доменов"
        self.data_fields = {
            "name": "text",
            "is_ssl": "bool",
            "certbot_email": "text",
            "server": "text",
            "port": "text",
        }
        self.title = "Домены"
        self.view_name = "domains"
        self.add_func = DomainService.add_domain
        self.get_data_func = DomainService.get_config
        self.del_func =  DomainService.del_domain
        self.update_func = DomainService.update_domain

