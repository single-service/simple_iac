import os
import json

from models.models import Server
from services.crypto_service import CryptoService


class ServerService:

    @staticmethod
    def get_config():
        data = ServerService.open_config()
        normilized_data = [Server(**{
            "name": k,
            "ip": CryptoService.decrypt(v.get("ip")),
            "port": v.get("port"),
            "login": CryptoService.decrypt(v.get("login")),
            "password": CryptoService.decrypt(v.get("password")),
            "is_swarm": v.get("is_swarm"),
            "is_master_node": v.get("is_master_node"),
            "swarm_parent": v.get("swarm_parent"),
            "install_nginx": v.get("install_nginx"),
        }) for k, v in data.items()]
        return normilized_data
    
    @staticmethod
    def del_server(server_name):
        data = ServerService.open_config()
        del data[server_name]
        ServerService.write_config(data)

    @staticmethod
    def add_server(name, ip, port, login, password, is_swarm, is_master_node, swarm_parent, install_nginx):
        errors = ServerService.validate_server_data(name, ip, port, login, password, is_swarm, is_master_node, swarm_parent, install_nginx)
        if errors:
            return False, errors
        data = ServerService.open_config()
        data[name] = {
            "ip": CryptoService.encrypt(ip),
            "port": port,
            "login": CryptoService.encrypt(login),
            "password": CryptoService.encrypt(password),
            "is_swarm": is_swarm,
            "is_master_node": is_master_node,
            "swarm_parent": swarm_parent,
            "install_nginx": install_nginx,
        }
        ServerService.write_config(data)
        return True, None
    
    @staticmethod
    def update_server(field, value, index):
        data = ServerService.open_config()
        server_name = list(data.keys())[index]
        encrypt_fields = {"ip", "login", "password"}
        if field == "name":
            old_body = data[server_name].copy()
            data[value] = old_body
            del data[server_name]
        else:
            if field in encrypt_fields:
                value = CryptoService.encrypt(value)
            data[server_name][field] = value
        ServerService.write_config(data)

    @staticmethod
    def validate_server_data(name, ip, port, login, password, is_swarm, is_master_node, swarm_parent, install_nginx):
        errors = []
        data = ServerService.open_config()
        if not name:
            errors.append("Field name is required")
        else:
            if name in data:
                errors.append(f"Server with name {name} already exist")
        if not ip:
            errors.append("Field ip is required")
        if not ip:
            errors.append("Field port is required")
        if not ip:
            errors.append("Field login is required")
        if not ip:
            errors.append("Field password is required")
        if is_swarm and not is_master_node and not swarm_parent:
            errors.append("If  server not is master swarm_parent is required")
        return errors


    @staticmethod
    def open_config():
        with open("configs/servers.json", "r") as json_file:
            data = json.load(json_file)
        return data
    
    @staticmethod
    def write_config(data):
        with open("configs/servers.json", "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)