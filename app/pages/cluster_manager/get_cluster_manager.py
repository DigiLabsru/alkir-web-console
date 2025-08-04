from ...common.interface.ras.ras import RasInterface


def get_cluster_manager(connect_info):
    try:
        rac = RasInterface(req=connect_info)
        cluster_managers_list = rac.java_get_cluster_managers()
        cluster_managers_data: list = []
        service_list = rac.java_get_cluster_service_all()
        service_list_data: list = []
        for one_service in service_list:
            service_list_data.append(
                {
                    "managers": [_.toString() for _ in one_service.getClusterManagerIds()],
                    "descr": one_service.getDescr(),
                    "main_only": one_service.getMainOnly(),
                    "name": one_service.getName()
                }
            )
        for one_cluster_manager in cluster_managers_list:
            cluster_managers_data.append({
                "hostname": one_cluster_manager.getHostName(),
                "descr": one_cluster_manager.getDescr(),
                "pid": one_cluster_manager.getPid(),
                "main_port": one_cluster_manager.getMainPort(),
                "main_manager": one_cluster_manager.getMainManager(),
                "id": one_cluster_manager.getClusterManagerId().toString()
            })
        rac.close()
    except Exception as ex:
        raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
    columns = [
        {"headerName": "Имя сервиса", "field": "service_name"},
    ]
    for one_cluster_manager_data in cluster_managers_data:
        columns.append(
            {"headerName": one_cluster_manager_data["hostname"], "field": one_cluster_manager_data["id"]}
        )
    try:
        result: list = {}
        result['columns'] = columns
        result['data'] = []
        result['data'].append({"service_name": "Роль"} | {_['id']: _['descr'] for _ in cluster_managers_data})
        result['data'].append({"service_name": "PID"} | {_['id']: _['pid'] for _ in cluster_managers_data})
        result['data'].append({"service_name": "IP Порт"} | {_['id']: _['main_port'] for _ in cluster_managers_data})
        result['data'].append({"service_name": "ID"} | {_['id']: _['id'] for _ in cluster_managers_data})
        for one_service in service_list_data:
            pass
            result['data'].append(
                {"service_name": one_service['descr']} | {_['id']: "✅" if _["id"] in one_service['managers'] else "❌" for _ in cluster_managers_data}
            )
        return result
    except Exception as ex:
        raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
