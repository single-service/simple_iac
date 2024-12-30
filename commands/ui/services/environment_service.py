import os

from services.apps import AppsService
from services.crypto_service import CryptoService


class EnvironmentService:

    @staticmethod
    def check_environment_file_exists(app_name, env_file_name):
        if os.path.exists(f"environments/{app_name}/{env_file_name}"):
            return True
        return False
    
    @staticmethod
    def create_environment_file(app_name, env_file_name, variables):
        os.makedirs(f"environments/{app_name}", exist_ok=True)
        with open(f"environments/{app_name}/{env_file_name}", "w") as env_file:
            env_file.write(CryptoService.encrypt(variables))
        data = AppsService.open_config()
        environments = data[app_name].get("environments")
        if environments is None:
            environments = []
        environments.append(env_file_name)
        data[app_name]["environments"] = environments
        AppsService.write_config(data)

    @staticmethod
    def env_file_name(app_name, env_index):
        data = AppsService.open_config()
        environments = data[app_name].get("environments")
        return environments[env_index]
    
    @staticmethod
    def env_file_data(app_name, env_file_name):
        filepath = f"environments/{app_name}/{env_file_name}"
        if not os.path.exists(filepath):
            return ""
        variables = ""
        with open(filepath, "r") as env_file:
            variables = env_file.read()
        return CryptoService.decrypt(variables)
