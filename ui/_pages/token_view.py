import os
import random
import string

import streamlit as st

env_file_path = '.env'

TOKEN = None
# Проверяем, существует ли файл .env
if os.path.exists(env_file_path):
    with open(env_file_path) as f:
        # Читаем строки файла
        for line in f:
            # Проверяем, содержит ли строка переменную APP_CRYPT_KEY
            if line.startswith('APP_CRYPT_KEY='):
                TOKEN = line.split("APP_CRYPT_KEY=")[1].split("\n")[0]
                print("Переменная APP_CRYPT_KEY найдена.")
                break
        else:
            print("Переменная APP_CRYPT_KEY не найдена.")
else:
    print("Файл .env не существует.")

st.title("Токен-Шифр")
if TOKEN:
    st.success(f"У вас есть токен шифрования: {TOKEN}")
    st.write("Сохраните этот ключ, иначе вам не получится расшифровать зашифрованные данные")
else:
    st.write("У вас отсутствует ключ шифрования")
    btn = st.button(label="Сформировать токен")
    if btn:
        key_choices = string.ascii_letters + string.digits
        key = "".join([random.choice(key_choices) for _ in range(30)])
        with open(env_file_path, "a") as env_file:
            env_file.write(f"APP_CRYPT_KEY={key}\n")
        st.rerun()
