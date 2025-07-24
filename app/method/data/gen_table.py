from .gen_table_method.get_all_sessions import get_all_sessions


def gen_table(id: str, server: str):
    from ....main import start_settings
    connect_info = [_ for _ in start_settings.server_list if _.ras_server == server]
    id_list = id.split("|")
    match id_list:
        case _ if id_list[-1] == 'all_sessions':
            pass
            return get_all_sessions(connect_info=connect_info)
        case _:
            return {
                "columns": [
                    {'name': 'na_me', 'label': 'Name', 'field': 'na_me', 'required': True, 'align': 'left', 'sortable': True},
                    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
                    {'name': 'age1', 'label': 'Age1', 'field': 'age1', 'sortable': True},
                    {'name': 'age2', 'label': 'Age2', 'field': 'age2', 'sortable': True},
                    {'name': 'age3', 'label': 'Age3', 'field': 'age3', 'sortable': True},
                    {'name': 'age4', 'label': 'Age4', 'field': 'age4', 'sortable': True},
                ],
                "data": [
                    {'na_me': 'Alice', 'age': 18, 'age1': 181, 'age2': 182, 'age3': 183, 'age4': 184},
                    {'na_me': 'Bob', 'age': 21, 'age1': 211, 'age2': 212, 'age3': 213, 'age4': 214},
                    {'na_me': 'Carol'},
                ],
                "header": "header"
            }
