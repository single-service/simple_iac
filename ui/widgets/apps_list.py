from widgets.abstract import TableView
from services.apps import AppsService


class AppsView(TableView):

    def __init__(self):
        self.headers = [
            "№", "Name", "Docker Compose", "Dest path", "is_swarm", "Server", ""
        ]
        self.instance_name = "приложение"
        self.instance_name_plural = "приложений"
        self.data_fields = {
            "name": "text",
            "local_path": "file",
            "dest_path": "text",
            "is_swarm": "bool",
            "server": "text"
        }
        self.title = "Приложения"
        self.view_name = "application"
        self.add_func = AppsService.add_app
        self.get_data_func = AppsService.get_config
        self.del_func =  AppsService.del_app
        self.update_func = AppsService.update_app
