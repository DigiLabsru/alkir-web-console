from loguru import logger
from nicegui import ui

from ..agent_admins.show_agent_admins import show_agent_admins
from ..cluster_admins.show_cluster_admins import show_cluster_admins
from ..cluster_manager.show_cluster_manager import show_cluster_manager
from ..clusters.show_clusters import show_clusters
from ..clusters.show_one_cluster import show_one_cluster
from ..connections.show_connections import show_connections
from ..locks.show_locks import show_locks
from ..sessions.show_sessions import show_sessions
from ..sessions.show_sessions_per_base import show_sessions_per_base
from ..work_processes.show_work_processes import show_work_processes
from ..work_server.show_work_server import show_work_server


def update_main(id: str, main_container, server: str):
    from ...main import start_settings
    connect_info = [_ for _ in start_settings.server_list if f'{_.ras_server}:{_.ras_port}' == server][0]
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
                    show_cluster_admins(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'central_admins':
                    show_agent_admins(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'cluster_manager':
                    show_cluster_manager(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-1] == 'work_processes':
                    show_work_processes(connect_info=connect_info, main_container=main_container)
                case _ if id_list[-2] == 'work_server':
                    show_work_server(connect_info=connect_info, main_container=main_container, work_server_id=id_list[-1])
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
