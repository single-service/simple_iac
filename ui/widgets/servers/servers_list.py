from datetime import datetime
import streamlit as st
from streamlit_extras.row import row as flex_row
from streamlit_modal import Modal

from services.server_service import ServerService


def update_server_value(field, server_index):
    value = st.session_state[f"server_{field}_{server_index}"]
    ServerService.update_server(field, value, int(server_index))


def list_view():

    delete_modal = Modal(
        "Удалить сервер", 
        key="delete-modal",
        
        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )

    st.title("Серверы")
    data = ServerService.get_config()
    # Add headers
    headers = ["№", "Name", "IP", "Port", "Login", "Password", "Is swarm", "is_master_node", "swarm_parent", "install_nginx", ""]
    cols = st.columns(11)
    for i, header in enumerate(headers):
        cols[i].write(header)
    st.divider()
    # Add server row
    cols = st.columns(11)
    cols[0].write("New")
    add_name = cols[1].text_input(label="", value="", key=f"server_name_new", label_visibility="collapsed")
    add_ip = cols[2].text_input(label="", value="", key=f"server_ip_new", label_visibility="collapsed")
    add_port = cols[3].text_input(label="", value="", key=f"server_port_new", label_visibility="collapsed")
    add_login = cols[4].text_input(label="", value="", key=f"server_login_new", label_visibility="collapsed")
    add_password = cols[5].text_input(label="", value="", key=f"server_password_new", label_visibility="collapsed")
    add_is_swarm = cols[6].checkbox(label="", value=False, key=f"server_is_swarm_new", label_visibility="collapsed")
    add_is_master_node = cols[7].checkbox(label="", value=False, key=f"server_is_master_node_new", label_visibility="collapsed")
    add_swarm_parent = cols[8].text_input(label="", value="", key=f"server_swarm_parent_new", label_visibility="collapsed")
    add_install_nginx = cols[9].checkbox(label="", value=False, key=f"server_install_nginx_new", label_visibility="collapsed")
    add_btn = cols[10].button(label="Add", key=f"server_add_btn", type="secondary")
    if add_btn:
        new_server = {
            "name": add_name,
            "ip": add_ip,
            "port": add_port,
            "login": add_login,
            "password": add_password,
            "is_swarm": add_is_swarm,
            "is_master_node": add_is_master_node,
            "swarm_parent": add_swarm_parent,
            "install_nginx": add_install_nginx,
        }
        _, errors = ServerService.add_server(**new_server)
        if errors:
            st.error(errors[0])
        else:
            st.rerun()
    st.divider()
    st.write("Список серверов")
    st.divider()
    # Show data
    del_buttons = []
    for i, row in enumerate(data):
        cols = st.columns(11)
        cols[0].write(i)
        cols[1].text_input(
            label="", value=row.name, key=f"server_name_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["name", i]
        )
        cols[2].text_input(
            label="", value=row.ip, key=f"server_ip_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["ip", i]
        )
        cols[3].text_input(
            label="", value=row.port, key=f"server_port_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["port", i]
        )
        cols[4].text_input(
            label="", value=row.login, key=f"server_login_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["login", i]
        )
        cols[5].text_input(
            label="", value=row.password, key=f"server_password_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["password", i]
        )
        cols[6].checkbox(
            label="", value=row.is_swarm, key=f"server_is_swarm_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["is_swarm", i]
        )
        cols[7].checkbox(
            label="", value=row.is_master_node, key=f"server_is_master_node_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["is_master_node", i]
        )
        cols[8].text_input(
            label="", value=row.swarm_parent, key=f"server_swarm_parent_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["swarm_parent", i]
        )
        cols[9].checkbox(
            label="", value=row.install_nginx, key=f"server_install_nginx_{i}", label_visibility="collapsed",
            on_change=update_server_value,
            args=["install_nginx", i]
        )
        del_btn = cols[10].button(label="Del", key=f"server_del_btn_{i}", type="primary")
        del_buttons.append(del_btn)
        st.divider()
    
    clicked_del_btn = [i for i, x in enumerate(del_buttons) if x]
    if clicked_del_btn:
        st.session_state["servers_del_candidate"] = clicked_del_btn[0]
        delete_modal.open()

    if delete_modal.is_open():
        with delete_modal.container():
            server_index = int(st.session_state["servers_del_candidate"])
            server_name = data[server_index].name
            st.write(f"Вы действительно хотите удалить сервер {server_name}?")
            buttons_row = flex_row(2)
            confirm_button = buttons_row.button(label="Да", type="primary", use_container_width=True)
            cancel_button = buttons_row.button(label="Нет", use_container_width=True)
            if confirm_button:
                ServerService.del_server(server_name)
                delete_modal.close()
                st.rerun()
            if cancel_button:
                delete_modal.close()
    else:
        st.session_state["servers_del_candidate"] = None
