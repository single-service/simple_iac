import json

from helpers.command_args import parse_args
from helpers.ssh_commands import get_ssh_client, docker_registry_login
from ui.services.crypto_service import CryptoService


def prepare_registres_func(chosen_server=None):
    servers = {}
    with open("configs/servers.json", "r") as json_file:
        servers = json.load(json_file)
    
    registries = {}
    with open("configs/registries.json", "r") as json_file:
        registries = json.load(json_file)

    if chosen_server:
        if chosen_server not in servers:
            raise Exception(f"Wrong chosen server name - {chosen_server}")
        servers = {k:v for k, v in servers.items() if k == chosen_server}

    for server_name, server_data in servers.items():
        client = get_ssh_client(
            ip=CryptoService.decrypt(server_data["ip"]),
            port=int(server_data["port"]),
            username=CryptoService.decrypt(server_data["login"]),
            password=CryptoService.decrypt(server_data["password"]),
        )
        print(f"Получен client {server_name}")
        for registry_name, registry_data in registries.items():
            docker_registry_login(
                client=client,
                username=CryptoService.decrypt(registry_data["login"]),
                password=CryptoService.decrypt(registry_data["password"]),
                url=registry_data["url"],
            )
            print(f"Прошла регистрация в {registry_name}")
        client.close()
    print("Docker Registries login successfull!")

if __name__ == "__main__":
    server = parse_args("server")
    prepare_registres_func(chosen_server=server)
