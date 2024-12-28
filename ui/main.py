import streamlit as st


def index():
    pages = [
        st.Page("_pages/instruction_view.py", title="Инструкция"),
        st.Page("_pages/servers.py", title="Серверы"),
        st.Page("_pages/apps.py", title="Приложения"),
        st.Page("_pages/docker_registries.py", title="Хранилища Docker"),
        st.Page("_pages/domains.py", title="Домены"),
        st.Page("_pages/commands.py", title="Команды"),
        st.Page("_pages/commandslogs_view.py", title="Логи команд"),
        st.Page("_pages/token_view.py", title="Токен-Шифр"),
    ]
    pg = st.navigation(pages)
    print("menu st.session_state['page']", st.session_state.get('page'))
    pg.run()

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    index()