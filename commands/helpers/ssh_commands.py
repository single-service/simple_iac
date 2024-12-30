import paramiko

def get_ssh_client(ip, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        ip,
        username=username,
        password=password,
        port=int(port)
    )
    return client

def install_docker(client, server_password):
    command = "sudo docker --version"
    stdin, stdout, stderr = client.exec_command(command)
    stdin.write(server_password + '\n')  # Ввод пароля для sudo
    stdin.flush()

    error = stderr.read().decode()
    print("Docker version check error: ", stderr.read().decode())
    print("Docker version check out: ", stdout.read().decode())
    if "command not found" not in error:
        print("Docker installed yet")
        return
    print("Installing docker")
    # Установка Docker
    install_command = (
        "sudo apt-get update && "
        "sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common && "
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && "
        "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" && "
        "DEBIAN_FRONTEND=noninteractive sudo apt-get install -y docker-ce"
    )
    stdin, stdout, stderr = client.exec_command(install_command)
    stdin.write(server_password + '\n')  # Ввод пароля для sudo
    stdin.flush()
    print("Docker install error: ", stderr.read().decode())
    print("Docker install out: ", stdout.read().decode())

    print("Docker installed successfully")

def docker_without_sudo(client, server_username):
    stdin, stdout, stderr = client.exec_command(f"sudo usermod -aG docker {server_username}")
    print(stdout.read().decode())
    print(stderr.read().decode())
    stdin, stdout, stderr = client.exec_command("docker --version")
    if "Docker version" in stdout.read().decode():
        print("Docker can be used without sudo")
        return
    print("Docker set rights is failed")

def install_nginx(client):
    _, stdout, stderr = client.exec_command("sudo apt update")
    print("--------")
    print("sudo apt update")
    print("stdout:", stdout.read().decode())
    print("~~~~")
    print("stderr:", stderr.read().decode())
    packages = [
        "nginx",
        "certbot",
        "python3-certbot-nginx"
    ]
    
    for package in packages:
        # Проверка, установлен ли пакет
        check_command = f"dpkg -l | grep {package}"
        _, stdout, stderr = client.exec_command(check_command)
        
        if stdout.read().decode().strip() == "":
            # Пакет не установлен, установка его
            install_command = f"sudo apt install -y {package}"
            print(f"Установка {package}...")
            _, stdout, stderr = client.exec_command(install_command)
            print("--------")
            print(install_command)
            print("stdout:", stdout.read().decode())
            print("~~~~")
            print("stderr:", stderr.read().decode())
        else:
            print(f"{package} уже установлен.")

def swarm_init(client):
        command = "docker node ls"
        stdin, stdout, stderr = client.exec_command(command)
        if "Error response from daemon" not in stderr.read().decode():
            print("Swarm initialized yet")
            return
        command = "docker swarm init"
        stdin, stdout, stderr = client.exec_command(command)
        response = stdout.read().decode().split("\n")
        for resp in response:
            if "docker swarm join --token " in resp:
                token_data = resp.split("docker swarm join --token ")[1]
                print(f"JOIN for swarm: docker swarm join --token {token_data}")
                break
        return token_data

def set_swarm_node_tag(client, tag):
    command = "docker node ls"
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode().split("\n")[1:-1]
    print("_set_node_tag ", stdout.read().decode())
    for line in output:
        if "*" in line:
            line = line.split("   ")
            current_host = line[1]
            break
    print("_set_node_tag current_host", current_host)
    command = f'docker node update --label-add tag={tag} {current_host}'
    stdin, stdout, stderr = client.exec_command(command)
    print(f"Тег для ноды {current_host} обновлен на {tag}.")

def get_swarm_token(client):
    command = "docker swarm join-token manager"
    _, stdout, _ = client.exec_command(command)
    response = stdout.read().decode().split("\n")
    token_data = None
    for resp in response:
        if "docker swarm join --token " in resp:
            token_data = resp
            break
    return token_data

def join_swarm(client, join_command):
    stdin, stdout, stderr = client.exec_command("docker info --format '{{.Swarm.LocalNodeState}}'")
    swarm_state = stdout.read().decode().strip()

    if swarm_state != "active":
        print("Сервер не присоединен к кластеру. Выполняем команду join...")
        stdin, stdout, stderr = client.exec_command(join_command)
        print(stdout.read().decode())
        print(stderr.read().decode())
    else:
        print("Сервер уже присоединен к кластеру.")

def docker_registry_login(client, username, password, url=None):
    command = f"docker login -u {username} -p {password}"
    if url:
        command = f"{command} {url}"
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def docker_pull_container(client, image):
    command = f"docker pull {image}"
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def docker_compose_run(client, path, compose_file_name):
    command = f"cd {path} && docker compose -f {compose_file_name} up -d --build --remove-orphans"
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def docker_stack_run(client, path, compose_file_name, stack_name):
    command = f"cd {path} && docker stack deploy -c {compose_file_name} {stack_name}"
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def create_dirs(client, path):
    dest_path = path.split("/")[1:]
    for i in range(len(dest_path)):
        cur_path = "/".join(dest_path[:i+1])
        stdin, stdout, stderr = client.exec_command(f'if [ ! -d /{cur_path} ]; then mkdir /{cur_path}; fi')
        print(f"Dir: {cur_path} created!")

def check_file_exists(client, path):
    sftp = client.open_sftp()
    try:
        # Проверяем, существует ли файл на сервере
        sftp.stat(path)
        file_exists = True
    except FileNotFoundError:
        file_exists = False
    sftp.close()
    return file_exists

def copy_file2server(client, local_path, server_path):
    sftp = client.open_sftp()
    sftp.put(local_path, server_path)
    sftp.close()


def get_remote_file_content(client, path):
    sftp = client.open_sftp()
    with sftp.open(path, 'r') as remote_file:
        remote_content = remote_file.read().decode()
    sftp.close()
    return remote_content