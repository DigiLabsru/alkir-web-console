from loguru import logger
from nicegui import ui

from .show_admins import show_admins
from .show_clusters import show_clusters
from .show_connections import show_connections
from .show_locks import show_locks
from .show_one_cluster import show_one_cluster
from .show_sessions import show_sessions
from .show_sessions_per_base import show_sessions_per_base


def update_main(id: str, main_container, server: str):
    from ...main import start_settings
    connect_info = [_ for _ in start_settings.server_list if _.ras_server == server][0]
    if id is not None:
        id_list = id.split("|")
        try:
            match id_list:
                case _ if id_list[-1] == 'all_sessions':
                    show_sessions(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'clusters':
                    show_clusters(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'cluster':
                    show_one_cluster(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'sessions_per_base':
                    show_sessions_per_base(connect_info=connect_info, main_container=main_container, base_name=id_list[-2])
                case _ if id_list[-1] == 'connections':
                    show_connections(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'locks':
                    show_locks(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'admins':
                    show_admins(connect_info=connect_info, main_container=main_container)
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
        except Exception as ex:
            ui.notify(f"При генерации страницы произошла ошибка.\n Текст ошибки: {ex}", type='negative', position='top-right', multi_line=True)
            logger.error(ex)
            main_container.clear()
