import jpype

from ....common.interface.ras.ras import RasInterface
from .table_descriptions.get_all_locks_table import columns
from .variable.app_translate import app_translate

# from .variable.app_translate import app_translate


def get_all_locks(connect_info):
    try:
        rac = RasInterface(req=connect_info)
        locks_all = rac.java_get_locks()
        connection_all = rac.java_get_connections_short()
        infobases_list = rac.java_get_infobases_short()
        working_processes_list = rac.java_get_working_processes()
        rac.close()
        all_base = {_.getInfoBaseId().toString(): _.getName() for _ in infobases_list}
        all_working_processes = {_.getWorkingProcessId().toString(): {"server": _.getHostName(), "port": _.getMainPort(), "pid": _.getPid()} for _ in working_processes_list}
        all_connections = {_.getInfoBaseConnectionId().toString(): {
            "app": app_translate.get(_.getApplication(), 'не определено'),
            "conn_id": _.getConnId(),
            "host": _.getHost(),
            "base": all_base.get(_.getInfoBaseId().toString(), None),
            "session_numer": _.getSessionNumber(),
            "working_process_id": _.getWorkingProcessId().toString()
        } for _ in connection_all}
        pass
    except Exception as ex:
        raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")

    locks_all[5].getConnectionId().toString()
    connection_all[0].getInfoBaseConnectionId().toString()
    try:
        result: list = {}
        result['columns'] = columns
        result['data'] = []
        SimpleDateFormat = jpype.JClass('java.text.SimpleDateFormat')
        sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        for one_lock in locks_all:
            connection_id = one_lock.getConnectionId().toString()
            result_data: dict = {
                "lock_descr": one_lock.getLockDescr(),
                "locked_at": sdf.format(one_lock.getLockedAt()),
                "base_name": all_connections.get(connection_id, {}).get('base', None),
                "connection": all_connections.get(connection_id, {}).get('conn_id', None),
                "session": all_connections.get(connection_id, {}).get('session_numer', None),
                "host_name": all_connections.get(connection_id, {}).get('host', None),
                "app_id": all_connections.get(connection_id, {}).get('app', None),
                "server": all_working_processes.get(all_connections.get(connection_id, {}).get('working_process_id', None), {}).get('server', None),
                "port": all_working_processes.get(all_connections.get(connection_id, {}).get('working_process_id', None), {}).get('port', None),
                "pid": all_working_processes.get(all_connections.get(connection_id, {}).get('working_process_id', None), {}).get('pid', None)
            }
            result['data'].append(result_data)
        result["header"] = f"Всего блокировок: {len(result['data'])}"
        return result
    except Exception as ex:
        raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
