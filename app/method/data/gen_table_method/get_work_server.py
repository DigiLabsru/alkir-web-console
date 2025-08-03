from ....common.interface.ras.ras import RasInterface
from ..gen_table_method.table_descriptions.get_work_server_table import columns


def get_work_server(connect_info, work_server_id):
    try:
        rac = RasInterface(req=connect_info)
        working_server_info = rac.java_get_working_server_info(server_id=work_server_id)
        assignment_rules_list = rac.java_get_assignment_rules(server_id=work_server_id)
        service_list = rac.java_get_cluster_service_all()
        rac.close()
    except Exception as ex:
        raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
    try:
        result: dict = {}
        services: dict = {_.getName(): _.getDescr() for _ in service_list}
        result['working_server_info'] = {}
        result['working_server_info']["cluster_main_port"] = working_server_info.getClusterMainPort()
        result['working_server_info']["connections_per_working_process_limit"] = working_server_info.getConnectionsPerWorkingProcessLimit()
        result['working_server_info']["critical_processes_total_memory"] = working_server_info.getCriticalProcessesTotalMemory()
        result['working_server_info']["host_name"] = working_server_info.getHostName()
        result['working_server_info']["infobases_per_working_process_limit"] = working_server_info.getInfoBasesPerWorkingProcessLimit()
        result['working_server_info']["main_port"] = working_server_info.getMainPort()
        result['working_server_info']["name"] = working_server_info.getName()
        result['working_server_info']["port_ranges"] = [working_server_info.getPortRanges()[0].getLowBound(), working_server_info.getPortRanges()[0].getHighBound()]
        result['working_server_info']["safe_call_memory_limit"] = working_server_info.getSafeCallMemoryLimit()
        result['working_server_info']["safe_working_processes_memory_limit"] = working_server_info.getSafeWorkingProcessesMemoryLimit()
        result['working_server_info']["temporary_allowed_processes_total_memory"] = working_server_info.getTemporaryAllowedProcessesTotalMemory()
        result['working_server_info']["temporary_allowed_processes_total_memory_time_limit"] = working_server_info.getTemporaryAllowedProcessesTotalMemoryTimeLimit()
        result['working_server_info']["working_process_memory_limit"] = working_server_info.getWorkingProcessMemoryLimit()
        result['working_server_info']["working_server_id"] = working_server_info.getWorkingServerId().toString()
        result['working_server_info']["is_dedicated_managers"] = working_server_info.isDedicatedManagers()
        result['working_server_info']["is_main_server"] = working_server_info.isMainServer()
        result['assignment_rules'] = {}
        result['assignment_rules']['columns'] = columns
        result['assignment_rules']['data'] = []
        count: int = 0
        rule_types: dict = {
            0: "Не назначать",
            1: "Авто",
            2: "Назначать"
        }
        for one_assignment_rule in assignment_rules_list:
            result['assignment_rules']['data'].append(
                {
                    "counter": count,
                    "application_ext": one_assignment_rule.getApplicationExt(),
                    "assignment_rule_id": one_assignment_rule.getAssignmentRuleId().toString(),
                    "info_base_name": one_assignment_rule.getInfoBaseName() if one_assignment_rule.getInfoBaseName() != "" else "Для всех",
                    "object_type": services[one_assignment_rule.getObjectType()] if one_assignment_rule.getObjectType() != "" else "Для всех",
                    "priority": one_assignment_rule.getPriority(),
                    "rule_type": rule_types[one_assignment_rule.getRuleType()]
                }
            )
            count += 1
        return result
    except Exception as ex:
        raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
