import json

from models.models import Application
from services.server_service import ServerService

class AppsService:

    @staticmethod
    def get_config():
        data = AppsService.open_config()
        normilized_data = [Application(**{
            "name": k,
            "local_path": v.get("local_path"),
            "dest_path": v.get("dest_path"),
            "is_swarm": v.get("is_swarm"),
            "server": v.get("server"),
        }) for k, v in data.items()]
        return normilized_data
    
    @staticmethod
    def del_app(name):
        data = AppsService.open_config()
        del data[name]
        AppsService.write_config(data)

    @staticmethod
    def add_app(name, local_path, dest_path, is_swarm, server):
        errors = AppsService.validate_data(name, local_path, dest_path, is_swarm, server)
        if errors:
            return False, errors
        data = AppsService.open_config()
        data[name] = {
            "local_path": local_path,
            "dest_path": dest_path,
            "is_swarm": is_swarm,
            "server": server
        }
        AppsService.write_config(data)
        return True, None
    
    @staticmethod
    def update_app(field, value, index):
        data = AppsService.open_config()
        instance_name = list(data.keys())[index]
        if field == "name":
            old_body = data[instance_name].copy()
            data[value] = old_body
            del data[instance_name]
        else:
            data[instance_name][field] = value
        AppsService.write_config(data)

    @staticmethod
    def validate_data(name, local_path, dest_path, is_swarm, server):
        errors = []
        data = AppsService.open_config()
        if not name:
            errors.append("Field name is required")
        else:
            if name in data:
                errors.append(f"App with name {name} already exist")
        if not local_path:
            errors.append("Field local_path is required")
        if not dest_path:
            errors.append("Field dest_path is required")
        if not is_swarm:
            errors.append("Field is_swarm is required")
        if not server:
            errors.append("Field is_swarm is required")
        else:
            servers_list = [x.name for x in ServerService.get_config()]
            if server not in servers_list:
                errors.append(f"Server {server} doesn't exist")
        return errors


    @staticmethod
    def open_config():
        with open("configs/apps.json", "r") as json_file:
            data = json.load(json_file)
        return data
    
    @staticmethod
    def write_config(data):
        with open("configs/apps.json", "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)