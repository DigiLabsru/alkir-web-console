from ...common.interface.ras.ras import RasInterface


def get_all_clusters(connect_info):
    try:
        rac = RasInterface(req=connect_info, its_get_clusters=True)
        cluster_info = rac.java_get_clusters()
        rac.close()
    except Exception as ex:
        raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
    try:
        result: dict = {}
        result['columns'] = [
            {"headerName": "Имя кластера", "field": "name", 'checkboxSelection': True},
            {"headerName": "Имя хоста", "field": "host_name"},
            {"headerName": "Основной порт", "field": "main_port"},
            {"headerName": "ID кластера", "field": "cluster_id"},
        ]
        result['data'] = []
        for one_cluster in cluster_info:
            result['data'].append(
                {
                    "cluster_id": one_cluster.getClusterId().toString(),
                    "host_name": one_cluster.getHostName(),
                    "main_port": one_cluster.getMainPort(),
                    "name": one_cluster.getName()
                }
            )
        return result
    except Exception as ex:
        raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
