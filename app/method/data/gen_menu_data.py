from ...common.interface.ras.ras import RasInterface


def gen_menu_data(server: str):
    from ...main import start_settings
    central_admins_list: list = []
    clusters_list: list = []
    # SimpleDateFormat = jpype.JClass('java.text.SimpleDateFormat')
    # sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    # cluster_info: dict = {}
    for one_server in start_settings.server_list:
        if server == one_server.ras_server:
            try:
                rac = RasInterface(req=one_server)
                cluster_list = rac.java_get_clusters()
                agent_admins_list = rac.java_get_agent_admins()
                platform_version = rac.java_get_agent_version()
                for one_agent_admin in agent_admins_list:
                    central_admins_list.append({"id": f"central_admins|{one_agent_admin.getName()}", "text": one_agent_admin.getName()})
                rac.close()
            except Exception as ex:
                raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
            try:
                for one_cluster in cluster_list:
                    current_cluster_id = one_cluster.getClusterId().toString()
                    menu_infobases_list: list = []
                    menu_work_server_list: list = []
                    menu_work_process_list: list = []
                    menu_cluster_manager_list: list = []
                    menu_locks_per_connection: list = []
                    one_server.cluster_id = current_cluster_id
                    rac = RasInterface(req=one_server)
                    infobases_list = rac.java_get_infobases_short()
                    cluster_admins_list = rac.java_get_cluster_admins()
                    work_server_list = rac.java_get_working_servers()
                    work_process_list = rac.java_get_working_processes()
                    locks_list = rac.java_get_locks()
                    rac_session_all = rac.java_get_sessions()
                    rac.close()
                    all_base = {_.getInfoBaseId().toString(): _.getName() for _ in infobases_list}
                    session_all = {_.getConnectionId().toString(): _ for _ in rac_session_all if _.getConnectionId().toString() != '00000000-0000-0000-0000-000000000000'}
                    menu_cluster_admins_list = [{"id": f"clusters|{current_cluster_id}|admins|{_.getName()}", "text": _.getName()} for _ in cluster_admins_list]
                    for one_base in infobases_list:
                        menu_infobases_list.append(
                            {
                                "id": f"clusters|{current_cluster_id}|info_base|{one_base.getName()}",
                                "text": one_base.getName(),
                                'children': [
                                    {"id": f"clusters|{current_cluster_id}|info_base|{one_base.getName()}|binary_storage", "text": "Хранилище двоичных данных"},
                                    {"id": f"clusters|{current_cluster_id}|info_base|{one_base.getName()}|sessions_per_base", "text": "Сеансы"},
                                    {"id": f"clusters|{current_cluster_id}|info_base|{one_base.getName()}|locks", "text": "Блокировки", 'children': [
                                        {"id": f"clusters|{current_cluster_id}|info_base|{one_base.getName()}|locks|locks_all", "text": "Все"},
                                        {"id": f"clusters|{current_cluster_id}|info_base|{one_base.getName()}|locks|locks_per_session", "text": "По сеансам"}
                                    ]
                                    },
                                    {"id": f"clusters|{current_cluster_id}|info_base|{one_base.getName()}|connections", "text": "Соединения"}
                                ]
                            }
                        )
                    for one_work_process in work_process_list:
                        menu_work_process_list.append(
                            {
                                "id": f"clusters|{current_cluster_id}|work_process|{one_work_process.getWorkingProcessId().toString()}",
                                "text": one_work_process.getHostName(),
                                "children": [
                                    {
                                        "id": f"clusters|{current_cluster_id}|work_process|{one_work_process.getWorkingProcessId().toString()}|connections",
                                        "text": "Соединения"
                                    }
                                ]
                            }
                        )
                    for one_work_server in work_server_list:
                        menu_cluster_manager_list.append(
                            {
                                "id": f"clusters|{current_cluster_id}|cluster_manager|{one_work_server.getWorkingServerId().toString()}",
                                "text": "Главный менеджер кластера" if one_work_server.isMainServer() is True else "Дополнительный менеджер кластера"
                            }
                        )
                        menu_work_server_list.append(
                            {
                                "id": f"clusters|{current_cluster_id}|work_server|{one_work_server.getWorkingServerId().toString()}",
                                "text": one_work_server.getHostName(),
                                "children": [
                                    {
                                        "id": f"clusters|{current_cluster_id}|work_server|{one_work_server.getWorkingServerId().toString()}|cluster_manager",
                                        "text": "Менеджеры кластера",
                                        "children": [
                                            {
                                                "id": f"clusters|{current_cluster_id}|work_server|{one_work_server.getWorkingServerId().toString()}|cluster_manager|role",
                                                "text": "Главный менеджер кластера" if one_work_server.isMainServer() is True else "Дополнительный менеджер кластера"
                                            }
                                        ]
                                    },
                                    {
                                        "id": f"clusters|{current_cluster_id}|work_server|{one_work_server.getWorkingServerId().toString()}|work_process",
                                        "text": "Рабочие процессы",
                                        "children": [
                                            {
                                                "id": f"clusters|{current_cluster_id}|work_server|{one_work_server.getWorkingServerId().toString()}|work_process|role",
                                                "text": "Главный менеджер кластера" if one_work_server.isMainServer() is True else "Дополнительный менеджер кластера"
                                            }
                                        ]
                                    },
                                    {
                                        "id": f"clusters|{current_cluster_id}|work_server|{one_work_server.getWorkingServerId().toString()}|tnf",
                                        "text": "Требования назначения функциональности",
                                    },
                                    {
                                        "id": f"clusters|{current_cluster_id}|work_server|{one_work_server.getWorkingServerId().toString()}|service_config",
                                        "text": "Настройки сервисов",
                                    }
                                ]
                            }
                        )
                    for one_lock in locks_list:
                        if one_lock.getConnectionId().toString() != '00000000-0000-0000-0000-000000000000':
                            if session_all.get(one_lock.getConnectionId().toString(), None) is not None:
                                menu_locks_per_connection.append(
                                    {
                                        "id": f"clusters|{current_cluster_id}|locks|per_connection|{one_lock.getConnectionId().toString()}",
                                        "text": f"{all_base[session_all[one_lock.getConnectionId().toString()].getInfoBaseId().toString()]}.\
{session_all[one_lock.getConnectionId().toString()].getSessionId()}.{session_all[one_lock.getConnectionId().toString()].getHost()}"
                                    }
                                )
                                pass
                                # база/что-то/хост
                                # session_all[one_lock.getConnectionId().toString()].getHost()
                    # menu_locks_list: list = [
                    #     {
                    #         "id": f"clusters|{current_cluster_id}|locks|all",
                    #         "text": "Все"
                    #     },
                    #     {
                    #         "id": f"clusters|{current_cluster_id}|locks|per_connection",
                    #         "text": f"По сеансам ({len(menu_locks_per_connection)})",
                    #         "children": menu_locks_per_connection
                    #     }
                    # ]
                    clusters_list.append(
                        {"id": f"clusters|{current_cluster_id}|cluster", "text": one_cluster.getName(), "children": [
                            {"id": f"clusters|{current_cluster_id}|info_base", "text": f"Информационные базы ({len(menu_infobases_list)})", "children": menu_infobases_list},
                            {"id": f"clusters|{current_cluster_id}|work_server", "text": f"Рабочие серверы ({len(menu_work_server_list)})", "children": menu_work_server_list},
                            {"id": f"clusters|{current_cluster_id}|admins", "text": f"Администраторы ({len(menu_cluster_admins_list)})", "children": menu_cluster_admins_list},
                            {"id": f"clusters|{current_cluster_id}|cluster_manager", "text": f"Менеджеры кластера ({len(menu_cluster_manager_list)})", "children": menu_cluster_manager_list},
                            {"id": f"clusters|{current_cluster_id}|work_processes", "text": f"Рабочие процессы ({len(menu_work_process_list)})", "children": menu_work_process_list},
                            {"id": f"clusters|{current_cluster_id}|all_sessions", "text": "Сеансы"},
                            {"id": f"clusters|{current_cluster_id}|locks", "text": "Блокировки"},
                            {"id": f"clusters|{current_cluster_id}|connections", "text": "Соединения"},
                            {"id": f"clusters|{current_cluster_id}|security_profiles", "text": "Профили безопасности"},
                            {"id": f"clusters|{current_cluster_id}|resource_consumption_counters", "text": "Счетчики потребления ресурсов"},
                            {"id": f"clusters|{current_cluster_id}|resource_consumption_restrictions", "text": "Ограничения потребления ресурсов"}
                        ]
                        }
                    )
            except Exception as ex:
                raise Exception(f"Произошла ошибка при обработке данных при построении меню. Текст ошибки: {ex}")
    menu_data: dict = [
        {"id": "clusters", 'text': f'Кластеры ({platform_version})', 'children': clusters_list},
        {"id": "central_admins", 'text': 'Администраторы', 'children': central_admins_list}
    ]
    return menu_data
