from prepare_servers import prepare_servers_func
from login_docker_registry import prepare_registres_func
from public_app import prepare_apps_func
from prepare_domains import prepare_domains_func

if __name__ == "__main__":
    prepare_servers_func()
    prepare_registres_func()
    prepare_apps_func()
    prepare_domains_func()
