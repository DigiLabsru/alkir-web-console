import jpype

from ....common.interface.ras.ras import RasInterface
from .table_descriptions.get_all_connections_table import columns
from .variable.app_translate import app_translate


def get_all_connections(connect_info):
    try:
        rac = RasInterface(req=connect_info)
        connection_all = rac.java_get_connections_short()
        infobases_list = rac.java_get_infobases_short()
        working_processes_list = rac.java_get_working_processes()
        rac.close()
        all_base = {_.getInfoBaseId().toString(): _.getName() for _ in infobases_list}
        all_working_processes = {_.getWorkingProcessId().toString(): {"server": _.getHostName(), "port": _.getMainPort(), "pid": _.getPid()} for _ in working_processes_list}
    except Exception as ex:
        raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
    try:
        result: list = {}
        result['columns'] = columns
        result['data'] = []
        SimpleDateFormat = jpype.JClass('java.text.SimpleDateFormat')
        sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        count: int = 0
        for one_connection in connection_all:
            count += 1
            result_data: dict = {
                "count": count,
                "app_id": app_translate.get(one_connection.getApplication(), 'не определено'),
                "blocked_by_ls": one_connection.getBlockedByLs(),
                "conn_id": one_connection.getConnId(),
                "connected_at": sdf.format(one_connection.getConnectedAt()),
                "host": one_connection.getHost(),
                "info_base_connection_id": one_connection.getInfoBaseConnectionId().toString(),
                "infobase_id": all_base.get(one_connection.getInfoBaseId().toString(), 'не определено'),
                "session_number": one_connection.getSessionNumber() if one_connection.getSessionNumber() != 0 else None,
                "server": all_working_processes.get(one_connection.getWorkingProcessId().toString(), 'не определено')['server'],
                "port": all_working_processes.get(one_connection.getWorkingProcessId().toString(), 'не определено')['port'],
                "pid": all_working_processes.get(one_connection.getWorkingProcessId().toString(), 'не определено')['pid']
            }
            result['data'].append(result_data)
        result["header"] = f"Всего соединений: {len(result['data'])}"
        result['data'] = result['data']
        return result
    except Exception as ex:
        raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
