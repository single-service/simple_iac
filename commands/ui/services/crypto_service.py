import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class CryptoService:
    @staticmethod
    def create_crypto_token(recreate_mode=False):
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
                if recreate_mode:
                    key = Fernet.generate_key()
                    environments[envvar_index] = f"{env_key}={key.decode()}"
                    with open(env_file_path, "w") as env_file:
                        env_file.write("\n".join(environments))
        else:
            key = Fernet.generate_key()
            with open(env_file_path, "w") as env_file:
                env_file.write(f"{env_key}={key.decode()}\n")
        load_dotenv()
            

    @staticmethod
    def get_crypto_token_from_file():
        env_file_path = ".env"
        env_key = "APP_CRYPT_KEY"
        if not os.path.exists(env_file_path):
            return None
        environments = []
        with open(env_file_path, "r") as env_file:
            environments = env_file.read().split("\n")
        tokens_list = [x for x in environments if x.startswith(env_key)]
        if not tokens_list:
            return None
        token = tokens_list[0].replace(f"{env_key}=", "")
        return token
    
    @staticmethod
    def get_crypto_token():
        token = os.getenv("APP_CRYPT_KEY")
        return token
    
    @staticmethod
    def encrypt(original_string):
        token = CryptoService.get_crypto_token_from_file()
        if not token:
            return original_string
        if original_string.startswith("!@?_"):
            return original_string
        token = token.encode()
        cipher = Fernet(token)
        encrypted_message = cipher.encrypt(original_string.encode())
        encrypted_message = encrypted_message.decode()
        return f"!@?_{encrypted_message}"
    
    @staticmethod
    def decrypt(encrypted_string):
        token = CryptoService.get_crypto_token_from_file()
        if not token:
            return encrypted_string
        if not encrypted_string.startswith("!@?_"):
            return encrypted_string
        str_without_salt = encrypted_string[4:].encode()
        cipher = Fernet(token.encode())
        decrypted_message = cipher.decrypt(str_without_salt).decode()
        return decrypted_message