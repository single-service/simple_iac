
import json
import os

from ui.models import models

if __name__ == "__main__":
    # check_servers config
    configs_list = ["servers", "apps", "domains", "registries"]
    for config in configs_list:
        if not os.path.exists(f"configs/{config}.json"):
            raise Exception(f"Need to create {config}.json file in configs")
    
    with open("configs/servers.json", "r") as json_file:
        data = json.load(json_file) 
    
    server_names = set()
    for server in data:
        server_names.add(server)
        server_data = models.Server(**{"name": server, **data[server]})

    with open("configs/registries.json", "r") as json_file:
        data = json.load(json_file)
    for registry in data:
        registry_data = models.Registry(**{"name": registry, **data[registry]})

    with open("configs/domains.json", "r") as json_file:
        data = json.load(json_file)
    for domain in data:
        domain_data = models.DomainFromConfig(**{"name": domain, **data[domain]})
        if domain_data.server not in server_names:
            raise Exception(f"Server {domain_data.server} doesn't exist for domain {domain}")
        if domain_data.config_path:
            if not os.path.exists(domain_data.config_path):
                raise Exception(f"Nginx conf {domain_data.config_path} for domain {domain} doesn't exist")

    with open("configs/apps.json", "r") as json_file:
        data = json.load(json_file)
    for app in data:
        app_data = models.Application(**{"name": app, **data[app]})
        if app_data.server not in server_names:
            raise Exception(f"Server {app_data.server} doesn't exist for app {app}")
        if not os.path.exists(app_data.local_path):
            raise Exception(f"Wrong local path for docker compose({app_data.local_path}) in app {app}")
        if app_data.environments:
            for env_path in app_data.environments:
                if not os.path.exists(f"environments/{app}/{env_path}"):
                    raise Exception(f"Wrong path for environment ({env_path}) in app {app}")
                
    print("Configs are correct!")
