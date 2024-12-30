import subprocess

import streamlit as st
from streamlit_extras.row import row as flex_row


COMMANDS = [
    {
        "name": "Пересоздать токен шифрования",
        "command": "recreate_crypto_token",
        "params": None
    },
    {
        "name": "Расшифровать файлы",
        "command": "decrypt_configs",
        "params": None
    },
    {
        "name": "Зашифровать файлы",
        "command": "encrypt_configs",
        "params": None
    },
    {
        "name": "Проверить конфиги",
        "command": "validate_configs",
        "params": None
    },
    {
        "name": "Синхронизировать инфраструктуру",
        "command": "sync_infrastructure",
        "params": None
    },
    {
        "name": "Настроить серверы",
        "command": "prepare_servers",
        "params": "server"
    },
    {
        "name": "Настроить docker registry",
        "command": "login_docker_registry",
        "params": "server"
    },
    {
        "name": "Опубликовать приложения",
        "command": "public_app",
        "params": "app"
    },
    {
        "name": "Настроить домены",
        "command": "prepare_domains",
        "params": "domain"
    },
]

st.title("Команды")
for command in COMMANDS:
    command_row = flex_row(3)
    command_row.write(command['name'])
    if command.get("params"):
        command_row.text_input(label=f'{command["params"]}(Не обязательный)', key=f"command_param_{command['command']}")
    command_run_btn = command_row.button(
        label="Выполнить",
        type="primary",
        key=f"command_btn_{command['command']}",
        args=[command['command']]
    )
    if command_run_btn:
        
        command_line = ["python", f"commands/{command['command']}.py"]
        command_param = command.get("params")
        if command_param:
            argument = st.session_state.get(f"command_param_{command['command']}")
            if argument:
                command_line.append(f"--{command_param}={argument}")
        subprocess.Popen(command_line)
        print("Run", command_line)
    st.divider()