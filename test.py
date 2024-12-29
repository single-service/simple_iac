from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv, set_key
# Генерация ключа
# key = "t2NnvjSdHgxgmriCgAIGx4wVwNs3LI".encode()
# key = Fernet.generate_key()
# print("key:", key.decode())
# cipher = Fernet(key)

# # Шифрование строки
# original_message = "Привет, мир!"
# encrypted_message = cipher.encrypt(original_message.encode())
# print(f"Зашифрованное сообщение: {encrypted_message.decode()}")

# # Расшифровка строки
# decrypted_message = cipher.decrypt(encrypted_message).decode()
# print(f"Расшифрованное сообщение: {decrypted_message}")

# import os
# from dotenv import load_dotenv, set_key

# Загрузка переменных окружения из .env файла
# load_dotenv()

# print(os.getenv("APP_CRYPT_KEY"))
env_file_path = ".env"
env_key = "APP_CRYPT_KEY"
if os.path.exists(env_file_path):
    environments = ""
    with open(env_file_path, "r") as env_file:
        environments = env_file.read()
    environments = environments.split("\n")
    envvar_index = None
    for i, envvar in enumerate(environments):
        if envvar.startswith(env_key):
            envvar_index = i
            break
    if envvar_index is None:
        environments = "\n".join(environments)
        key = Fernet.generate_key()
        with open(env_file_path, "w") as env_file:
            env_file.write(f"{env_key}={key.decode()}\n{environments}")
else:
    key = Fernet.generate_key()
    with open(env_file_path, "w") as env_file:
        env_file.write(f"{env_key}={key.decode()}\n")
load_dotenv()
