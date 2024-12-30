import json
import yaml

from helpers.ssh_commands import (
    get_ssh_client,
    create_dirs,
    check_file_exists,
    copy_file2server,
    get_remote_file_content,
    docker_pull_container,
    docker_compose_run,
    docker_stack_run
)
from ui.services.crypto_service import CryptoService


def crypt_environment_file(path, encrypt=True):
    with open(path, "r") as env_file:
        content = env_file.read()
    if encrypt:
        content = CryptoService.encrypt(content)
    else:
        content = CryptoService.decrypt(content)
    with open(path, "w") as env_file:
        env_file.write(content)


if __name__ == "__main__":
    servers = {}
    with open("configs/servers.json", "r") as json_file:
        servers = json.load(json_file)

    apps = {}
    with open("configs/apps.json", "r") as json_file:
        apps = json.load(json_file)

    app_configs_changed = False

    for app_name, app_data in apps.items():
        server_data = servers[app_data["server"]]
        client = get_ssh_client(
            ip=CryptoService.decrypt(server_data["ip"]),
            port=int(server_data["port"]),
            username=CryptoService.decrypt(server_data["login"]),
            password=CryptoService.decrypt(server_data["password"]),
        )
        # check or create directories and docker compose yml
        create_dirs(client, app_data["dest_path"])
        docker_compose_file_path = f'{app_data["dest_path"]}/docker-compose.yml'
        is_exist = check_file_exists(client, docker_compose_file_path)
        if not is_exist:
            copy_file2server(client, app_data["local_path"], docker_compose_file_path)
            app_configs_changed = True
        else:
            cur_file_content = ""
            with open(app_data["local_path"], "r") as local_file:
                cur_file_content = local_file.read()
            remote_file_content = get_remote_file_content(client, docker_compose_file_path)
            if cur_file_content != remote_file_content:
                app_configs_changed = True
                copy_file2server(client, app_data["local_path"], docker_compose_file_path)
        
        # prepare environments
        create_dirs(client, f'{app_data["dest_path"]}/.envs')
        environments_files = app_data["environments"]
        if environments_files is None:
            environments_files = []
        for env_file_name in environments_files:
            # need to decrypt file content
            local_env_path = f"environments/{app_name}/{env_file_name}"
            remote_env_path = f'{app_data["dest_path"]}/.envs/{env_file_name}'
            crypt_environment_file(local_env_path, encrypt=False)
            is_exist = check_file_exists(client, remote_env_path)
            if not is_exist:
                app_configs_changed = True
                copy_file2server(client, local_env_path, remote_env_path)
            else:
                cur_file_content = ""
                with open(local_env_path, "r") as local_file:
                    cur_file_content = local_file.read()
                remote_file_content = get_remote_file_content(client, remote_env_path)
                if cur_file_content != remote_file_content:
                    app_configs_changed = True
                    copy_file2server(client, local_env_path, remote_env_path)
            crypt_environment_file(local_env_path, encrypt=True)
        
        # pull containers
        with open(app_data["local_path"]) as stream:
            try:
                dc_file_content = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                dc_file_content = None
        images = set()
        for service_name, service_data in dc_file_content.get("services", {}).items():
            image = service_data.get("image")
            if image:docker_compose_run
            docker_pull_container(client, image)
            print(f"end pull {image}")

        # run app
        if app_configs_changed:
            if not app_data["is_swarm"]:
                docker_compose_run(client, app_data["dest_path"], "docker-compose.yml")
            else:
                docker_stack_run(client, app_data["dest_path"], "docker-compose.yml", app_data["swarm_stack"])

        # complited
        client.close()
        print(f"App {app_name} complited!")
    print("Apps public successful")