import os

import streamlit as st
from streamlit_extras.row import row as flex_row


st.title("Логи")
logs_files = os.listdir("logs")
logs_files = [x for x in logs_files if x != ".gitkeep"]

for i, log_file_name in enumerate(logs_files):
    cols = st.columns(2)
    cols[0].write(i+1)
    log_button = cols[1].button(
        label=log_file_name,
        type="tertiary",
        key=f"log_file_{i}"
    )
    if log_button:
        log_data = ""
        with open(f"logs/{log_file_name}", "r") as log_file:
            log_data = log_file.read()
        st.code(log_data, language="log", wrap_lines=True, line_numbers=True)
