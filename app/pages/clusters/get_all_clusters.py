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

    # try:
    #     rac = RasInterface(req=connect_info)
    #     cluster_info = rac.java_get_cluster_info()
    #     platform_version = rac.java_get_agent_version()
    #     rac.close()
    # except Exception as ex:
    #     raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
    # try:
    #     result: dict = {
    #         "cluster_id": cluster_info.getClusterId().toString(),
    #         "expiration_timeout": cluster_info.getExpirationTimeout(),
    #         "host_name": cluster_info.getHostName(),
    #         "life_time_limit": cluster_info.getLifeTimeLimit(),
    #         "main_port": cluster_info.getMainPort(),
    #         "max_memory_size": cluster_info.getMaxMemorySize(),
    #         "max_memory_time_limit": cluster_info.getMaxMemoryTimeLimit(),
    #         "name": cluster_info.getName(),
    #         "security_level": cluster_info.getSecurityLevel(),
    #         "session_fault_tolerance_level": cluster_info.getSessionFaultToleranceLevel(),
    #         "load_balancing_mode": cluster_info.getLoadBalancingMode(),
    #         "cluster_recycling_errors_count_threshold": cluster_info.getClusterRecyclingErrorsCountThreshold(),
    #         "cluster_recycling_kill_by_memory_with_dump": cluster_info.isClusterRecyclingKillByMemoryWithDump(),
    #         "cluster_recycling_kill_problem_processes": cluster_info.isClusterRecyclingKillProblemProcesses(),
    #         "platform_version": platform_version
    #     }
    #     return result
    # except Exception as ex:
    #     raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
