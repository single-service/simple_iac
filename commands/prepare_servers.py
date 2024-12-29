import json

from helpers.ssh_commands import (
    get_ssh_client, install_docker,
    docker_without_sudo,
    install_nginx,
    swarm_init,
    set_swarm_node_tag,
    get_swarm_token,
    join_swarm
)
from ui.services.crypto_service import CryptoService



def prepare_server(
        server_name, ip, port, login, password, is_swarm,
        is_master_node, swarm_parent, is_install_nginx,
        swarm_join=None
):
    client = get_ssh_client(
        ip=ip,
        port=port,
        username=login,
        password=password,
    )
    install_docker(client, password)
    docker_without_sudo(client, login)
    if is_swarm:
        if is_master_node:
            swarm_init(client)
        else:
            join_swarm(client, swarm_join)
        set_swarm_node_tag(client, server_name)
    if is_install_nginx:
        install_nginx(client)
    client.close()
    print(f"{server_name} successfully prepared")

def get_swarm_join_token(
    ip, port, login, password
):
    client = get_ssh_client(
        ip=ip,
        port=port,
        username=login,
        password=password,
    )
    token = get_swarm_token(client)
    return token

if __name__ == "__main__":
    # прием аргумента
    # Валидация конфига servers

    servers_data = {}
    with open("configs/servers.json", "r") as json_file:
        servers_data = json.load(json_file)

    # серверы без сварма
    servers_without_swarm = {k:v for k, v in servers_data.items() if v['is_swarm'] is False}
    print("servers_without_swarm", servers_without_swarm)
    for server_name, server_data in servers_without_swarm.items():
        prepare_server(
            server_name=server_name,
            ip=CryptoService.decrypt(server_data["ip"]),
            port=server_data["port"],
            login=CryptoService.decrypt(server_data["login"]),
            password=CryptoService.decrypt(server_data["password"]),
            is_swarm=server_data["is_swarm"],
            is_master_node=server_data["is_master_node"],
            swarm_parent=server_data["swarm_parent"],
            is_install_nginx=server_data["install_nginx"],
        )
    # серверы мастер сварм
    servers_master_swarm = {k:v for k, v in servers_data.items() if v['is_swarm'] and v['is_master_node']}
    print("servers_master_swarm", servers_master_swarm)
    for server_name, server_data in servers_master_swarm.items():
        prepare_server(
            server_name=server_name,
            ip=CryptoService.decrypt(server_data["ip"]),
            port=server_data["port"],
            login=CryptoService.decrypt(server_data["login"]),
            password=CryptoService.decrypt(server_data["password"]),
            is_swarm=server_data["is_swarm"],
            is_master_node=server_data["is_master_node"],
            swarm_parent=server_data["swarm_parent"],
            is_install_nginx=server_data["install_nginx"],
        )

    # серверы slave сварм
    servers_slave_swarm = {k:v for k, v in servers_data.items() if v['is_swarm'] and not v['is_master_node']}
    print("servers_slave_swarm", servers_slave_swarm)
    for server_name, server_data in servers_slave_swarm.items():
        master_node_data = servers_data[server_data["swarm_parent"]]
        token = get_swarm_join_token(
            ip=CryptoService.decrypt(master_node_data["ip"]),
            port=int(master_node_data["port"]),
            login=CryptoService.decrypt(master_node_data["login"]),
            password=CryptoService.decrypt(master_node_data["password"]),
        )
        prepare_server(
            server_name=server_name,
            ip=CryptoService.decrypt(server_data["ip"]),
            port=server_data["port"],
            login=CryptoService.decrypt(server_data["login"]),
            password=CryptoService.decrypt(server_data["password"]),
            is_swarm=server_data["is_swarm"],
            is_master_node=server_data["is_master_node"],
            swarm_parent=server_data["swarm_parent"],
            is_install_nginx=server_data["install_nginx"],
            swarm_join=token
        )
    print("All servers prepared")