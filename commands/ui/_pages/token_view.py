import os
import random
import string

import streamlit as st

from services.crypto_service import CryptoService

env_file_path = '.env'

TOKEN = CryptoService.get_crypto_token_from_file()

st.title("Токен-Шифр")
if TOKEN:
    st.success(f"У вас есть токен шифрования: {TOKEN}")
    st.write("Сохраните этот ключ, иначе вам не получится расшифровать зашифрованные данные")
    st.button("Обновить ключ шифрования", type="secondary")
else:
    st.write("У вас отсутствует ключ шифрования")
    btn = st.button(label="Сформировать токен")
    if btn:
        CryptoService.create_crypto_token()
        st.rerun()
