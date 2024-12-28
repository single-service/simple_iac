import json
import os

from models.models import Domain
from services.server_service import ServerService

class DomainService:

    @staticmethod
    def get_config():
        data = DomainService.open_config()
        normilized_data = [Domain(**{
            "name": k, 
            "is_ssl": v.get("is_ssl"),
            "server": v.get("server"),
            "port": v.get("port"),
        }) for k, v in data.items()]
        return normilized_data
    
    @staticmethod
    def del_domain(name):
        data = DomainService.open_config()
        del data[name]
        if os.path.exists(f"nginx_conf/{name}.conf"):
            os.remove(f"nginx_conf/{name}.conf")
        DomainService.write_config(data)

    @staticmethod
    def add_domain(name, is_ssl, server, port):
        errors = DomainService.validate_domain_data(name, is_ssl, server, port)
        if errors:
            return False, errors
        data = DomainService.open_config()
        # create config
        config_path = DomainService.create_nginx_conf(name, port)
        # save data
        data[name] = {
            "config_path": config_path,
            "is_ssl": is_ssl,
            "server": server,
            "port": port
        }
        DomainService.write_config(data)
        return True, None
    
    @staticmethod
    def create_nginx_conf(domain, port):
        base_content = ""
        with open("templates/nginx.conf", "r") as nginx_conf:
            base_content = nginx_conf.read()
        base_content = base_content.replace("{{_DOMAIN_}}", domain)
        base_content = base_content.replace("{{_DOMAIN_PORT_}}", port)
        config_path = f"nginx_conf/{domain}.conf"
        with open(config_path, "w") as new_conf:
            new_conf.write(base_content)
        return config_path
    
    @staticmethod
    def update_domain(field, value, index):
        data = DomainService.open_config()
        instance_name = list(data.keys())[index]
        if field == "name":
            old_body = data[instance_name].copy()
            data[value] = old_body
            del data[instance_name]
            if os.path.exists(f"nginx_conf/{instance_name}.conf"):
                os.remove(f"nginx_conf/{instance_name}.conf")
            config_path = DomainService.create_nginx_conf(value, old_body['port'])
            data[value]["config_path"] = config_path
        else:
            data[instance_name][field] = value
            if field == "port":
                DomainService.create_nginx_conf(instance_name, value)
        DomainService.write_config(data)

    @staticmethod
    def validate_domain_data(name, is_ssl, server, port):
        errors = []
        data = DomainService.open_config()
        if not name:
            errors.append("Field name is required")
        else:
            if name in data:
                errors.append(f"Server with name {name} already exist")
        if not server:
            errors.append("Field server is required")
        else:
            servers_list = ServerService.get_config()
            if server not in [x.name for x in servers_list]:
                errors.append(f"Server {server} doesn't exist")
        if not port:
            errors.append("Field port is required")
        return errors


    @staticmethod
    def open_config():
        with open("configs/domains.json", "r") as json_file:
            data = json.load(json_file)
        return data
    
    @staticmethod
    def write_config(data):
        with open("configs/domains.json", "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)