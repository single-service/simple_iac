import json

from models.models import Registry

class DockerRegistryService:

    @staticmethod
    def get_config():
        data = DockerRegistryService.open_config()
        normilized_data = [Registry(**{"name": k, **v}) for k, v in data.items()]
        return normilized_data
    
    @staticmethod
    def del_registry(server_name):
        data = DockerRegistryService.open_config()
        del data[server_name]
        DockerRegistryService.write_config(data)

    @staticmethod
    def add_registry(name, url, login, password):
        errors = DockerRegistryService.validate_server_data(name, url, login, password)
        if errors:
            return False, errors
        data = DockerRegistryService.open_config()
        data[name] = {
            "url": url,
            "login": login,
            "password": password,
        }
        DockerRegistryService.write_config(data)
        return True, None
    
    @staticmethod
    def update_registry(field, value, index):
        data = DockerRegistryService.open_config()
        instance_name = list(data.keys())[index]
        if field == "name":
            old_body = data[instance_name].copy()
            data[value] = old_body
            del data[instance_name]
        else:
            data[instance_name][field] = value
        DockerRegistryService.write_config(data)

    @staticmethod
    def validate_server_data(name, url, login, password):
        errors = []
        data = DockerRegistryService.open_config()
        if not name:
            errors.append("Field name is required")
        else:
            if name in data:
                errors.append(f"Docker registry with name {name} already exist")
        if not url:
            errors.append("Field url is required")
        if not login:
            errors.append("Field login is required")
        if not password:
            errors.append("Field password is required")
        return errors


    @staticmethod
    def open_config():
        with open("configs/registries.json", "r") as json_file:
            data = json.load(json_file)
        return data
    
    @staticmethod
    def write_config(data):
        with open("configs/registries.json", "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)