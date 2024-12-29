import json
import os

from ui.services.crypto_service import CryptoService

if __name__ == "__main__":
    # encrypt configs
    configs = {
        "servers": ["ip", "login", "password"],
        "registries": ["login", "password"],
    }
    for file_name in configs:
        data = None
        print(file_name)
        with open(f"configs/{file_name}.json", "r") as json_file:
            data = json.load(json_file)

        for k in data:
            for field in configs[file_name]:
                data[k][field] = CryptoService.encrypt(data[k][field])
        
        with open(f"configs/{file_name}.json", "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=10)

    # encrypt environments
    for app in os.listdir("environments"):
        for env_file_name in os.listdir(f"environments/{app}"):
            data = None
            with open(f"environments/{app}/{env_file_name}", "r") as env_file:
                data = env_file.read()
            data = CryptoService.encrypt(data)
            with open(f"environments/{app}/{env_file_name}", "w") as env_file:
                env_file.write(data)
    print("Encrypt success!")
    