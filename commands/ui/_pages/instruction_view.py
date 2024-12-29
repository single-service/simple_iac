import os

import streamlit as st


content = ""
readme_file_path = "README.md"
if os.path.exists(readme_file_path):
    with open("README.md") as readme_file:
        content = readme_file.read()
st.markdown(content)
