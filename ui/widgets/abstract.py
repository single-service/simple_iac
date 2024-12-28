import streamlit as st
from streamlit_extras.row import row as flex_row
from streamlit_modal import Modal


class TableView:
    def __init__(self):
        self.headers = []
        self.instance_name = "instance"
        self.instance_name_plural = "instance_name_plural"
        self.data_fields = {}
        self.title = "Instances"
        self.view_name = "instance"
        self.add_func = None
        self.get_data_func = None
        self.del_func =  None
        self.update_func = None

    def _get_modal(self):
        return Modal(
            f"Удалить {self.instance_name}", 
            key="delete-modal",
            padding=20,
            max_width=744
        )

    def _update_server_value(self, field, server_index):
        value = st.session_state[f"{self.view_name}_{field}_{server_index}"]
        self.update_func(field, value, int(server_index))
    
    def _table_headers(self):
        cols = st.columns(len(self.headers))
        for i, header in enumerate(self.headers):
            cols[i].write(header)
        st.divider()

    def _table_add_row(self):
        cols = st.columns(len(self.headers))
        cols[0].write("New")
        col_number = 1
        for name, field_type in self.data_fields.items():
            params = dict(
                label="1",
                value="",
                key=f"{self.view_name}_{name}_new",
                label_visibility="collapsed"
            )
            if field_type == "bool":
                field = cols[col_number].checkbox(**params)
            elif field_type == "text":
                field = cols[col_number].text_input(**params)
            self.add_fields.append(field)
            col_number += 1
        add_btn = cols[col_number].button(label="Add", key=f"{self.view_name}_add_btn", type="secondary")
        if add_btn:

            new_instance = {}
            for i, field_name in enumerate(list(self.data_fields.keys())):
                new_instance[field_name] = self.add_fields[i]
            _, errors = self.add_func(**new_instance)
            if errors:
                st.error(errors[0])
            else:
                st.rerun()
        st.divider()
        st.write(f"Список {self.instance_name_plural}")
        st.divider()

    def _table_body(self, data):
        del_buttons = []
        for i, row in enumerate(data):
            cols = st.columns(len(self.headers))
            cols[0].write(i+1)
            col_number = 1
            for field_name, field_type in self.data_fields.items():
                params = dict(
                    label="1",
                    value=getattr(row, field_name),
                    key=f"{self.view_name}_{field_name}_{i}",
                    label_visibility="collapsed",
                    on_change=self._update_server_value,
                    args=[field_name, i]
                )
                if field_type == "bool":
                    cols[col_number].checkbox(**params)
                elif field_type == "text":
                    cols[col_number].text_input(**params)
                col_number += 1
            del_btn = cols[col_number].button(label="Del", key=f"{self.view_name}_del_btn_{i}", type="primary")
            del_buttons.append(del_btn)
            st.divider()
    
        clicked_del_btn = [i for i, x in enumerate(del_buttons) if x]
        if clicked_del_btn:
            st.session_state[f"{self.view_name}_del_candidate"] = clicked_del_btn[0]
            self.delete_modal.open()

    def _check_modal(self, data):
        if self.delete_modal.is_open():
            with self.delete_modal.container():
                server_index = int(st.session_state[f"{self.view_name}_del_candidate"])
                instance_name = data[server_index].name
                st.write(f"Вы действительно хотите удалить {self.instance_name} {instance_name}?")
                buttons_row = flex_row(2)
                confirm_button = buttons_row.button(label="Да", type="primary", use_container_width=True)
                cancel_button = buttons_row.button(label="Нет", use_container_width=True)
                if confirm_button:
                    self.del_func(instance_name)
                    self.delete_modal.close()
                    st.rerun()
                if cancel_button:
                    self.delete_modal.close()
        else:
            st.session_state[f"{self.view_name}_del_candidate"] = None

    def view(self):
        st.title(self.title)
        self.delete_modal = self._get_modal()
        self.add_fields = []
        data = self.get_data_func()
        self._table_headers()
        self._table_add_row()
        self._table_body(data)
        self._check_modal(data)