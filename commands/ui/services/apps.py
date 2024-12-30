import json
import os

import streamlit as st

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
            "environments": v.get("environments"),
            "swarm_stack": v.get("swarm_stack"),
        }) for k, v in data.items()]
        return normilized_data
    
    @staticmethod
    def del_app(name):
        data = AppsService.open_config()
        del data[name]
        local_path = f"composes/{name}.yml"
        if os.path.exists(local_path):
            os.remove(local_path)
        AppsService.write_config(data)

    @staticmethod
    def add_app(name, local_path, dest_path, is_swarm, swarm_stack, server, environments):
        errors = AppsService.validate_data(name, local_path, dest_path, is_swarm, swarm_stack, server)
        if errors:
            return False, errors
        data = AppsService.open_config()
        real_path = f"composes/{name}.yml"
        print("local_path", local_path)
        compose_data = local_path.getvalue().decode()
        with open(real_path, "w") as compose_file:
            compose_file.write(compose_data)
        data[name] = {
            "local_path": real_path,
            "dest_path": dest_path,
            "is_swarm": is_swarm,
            "swarm_stack": swarm_stack,
            "server": server,
            "environments": None
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
            os.rename(f"composes/{instance_name}.yml", f"composes/{value}.yml")
        elif field == "local_path":
            compose_data = value.getvalue().decode()
            local_path = f"composes/{instance_name}.yml"
            with open(local_path, "w") as compose_file:
                compose_file.write(compose_data)
            data[instance_name]["local_path"] = local_path
        else:
            data[instance_name][field] = value
        AppsService.write_config(data)

    @staticmethod
    def validate_data(name, local_path, dest_path, is_swarm, swarm_stack, server):
        errors = []
        data = AppsService.open_config()
        if not name:
            errors.append("Field name is required")
        else:
            if name in data:
                errors.append(f"App with name {name} already exist")
        if local_path is None:
            errors.append("Field local_path is required")
        if not dest_path:
            errors.append("Field dest_path is required")
        if is_swarm and not swarm_stack:
            errors.append("Field swarm_stack is required if is_swarm true")
        if not server:
            errors.append("Field is_swarm is required")
        else:
            servers_list = [x.name for x in ServerService.get_config()]
            print(servers_list)
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