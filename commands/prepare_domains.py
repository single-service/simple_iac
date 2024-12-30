import json

from helpers.ssh_commands import (
    get_ssh_client,
    ping_domain,
    check_file_exists,
    copy_file2server,
    get_remote_file_content,
    set_link4nginx_conf,
    restart_nginx,
    install_ssl2domain
)
from ui.services.crypto_service import CryptoService

def prepare_domains_func():
    servers = {}
    with open("configs/servers.json", "r") as json_file:
        servers = json.load(json_file)

    domains = {}
    with open("configs/domains.json", "r") as json_file:
        domains = json.load(json_file)

    for domain_url, domain_data in domains.items():
        server_data = servers[domain_data["server"]]
        ip_address = ping_domain(domain_url)
        print("ip_address", ip_address)
        if not ip_address:
            raise Exception(f"Domain {domain_url} doesn't proxy to ip {CryptoService.decrypt(server_data['ip'])}")
        if ip_address != CryptoService.decrypt(server_data['ip']):
            raise Exception(f"Domain {domain_url} proxy  to another ip({ip_address})")
        
        client = get_ssh_client(
            ip=CryptoService.decrypt(server_data["ip"]),
            port=int(server_data["port"]),
            username=CryptoService.decrypt(server_data["login"]),
            password=CryptoService.decrypt(server_data["password"]),
        )
        # check conf files
        remote_path = f"/etc/nginx/sites-available/{domain_url}"
        is_exist = check_file_exists(client, remote_path)
        if not is_exist:
            copy_file2server(client, domain_data["config_path"], remote_path)
        else:
            local_content = ""
            with open(domain_data["config_path"], "r") as local_conf:
                local_content = local_conf.read()
            remote_content = get_remote_file_content(client, remote_path)
            if local_content != remote_content:
                copy_file2server(client, domain_data["config_path"], remote_path)
        set_link4nginx_conf(client, domain_url)

        # restart nginx
        restart_nginx(client)
        print("nginx restarted")

        # install certbot
        if domain_data["is_ssl"]:
            cert_path = f"/etc/letsencrypt/live/{domain_url}/privkey.pem"
            is_exist = check_file_exists(client, cert_path)
            if not is_exist:
                install_ssl2domain(client, domain_url, domain_data["certbot_email"])
            print("SSl updated")
        
        client.close()
        print(f"Domain {domain_url} prepared!")
    print("All domains are prepared succesfully!")


if __name__ == "__main__":
    prepare_domains_func()