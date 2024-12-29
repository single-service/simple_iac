import os

from ui.services.crypto_service import CryptoService

if __name__ == "__main__":
    os.system("python commands/decrypt_configs.py")
    CryptoService.create_crypto_token(recreate_mode=True)
    os.system("python commands/encrypt_configs.py")
    print("Token succesfully recreated!")