import jpype

from ....common.interface.ras.ras import RasInterface
from .table_descriptions.get_work_processes_table import columns


def get_work_processes(connect_info):
    try:
        rac = RasInterface(req=connect_info)
        work_process_list = rac.java_get_working_processes()
        rac.close()
    except Exception as ex:
        raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
    try:
        result: list = {}
        result['columns'] = columns
        result['data'] = []
        SimpleDateFormat = jpype.JClass('java.text.SimpleDateFormat')
        sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        for one_work_process in work_process_list:
            pass
            result['data'].append(
                {
                    "hostname": one_work_process.getHostName(),
                    "port": one_work_process.getMainPort(),
                    "start_time": sdf.format(one_work_process.getStartedAt()),
                    "connections": one_work_process.getConnections(),
                    "use": "✅" if one_work_process.getUse() == 1 else "❌",
                    "enable": "✅" if one_work_process.isEnable() is True else "❌",
                    "active": "✅" if one_work_process.getRunning() == 1 else "❌",
                    "reserve": "✅" if one_work_process.isReserve() is True else "❌",
                    "pid": one_work_process.getWorkingProcessId().toString(),
                    "memory": one_work_process.getMemorySize()*1024,
                    "available_performance": one_work_process.getAvailablePerfomance(),
                    "performance": one_work_process.getCapacity(),
                    "license": one_work_process.getLicense()[0].getFullPresentation() if one_work_process.getLicense().size() != 0 else "Не потребляет лицензию",
                    "os_pid": one_work_process.getPid(),
                    "server_speed": float(one_work_process.getAvgCallTime()),
                    "server_time": float(one_work_process.getAvgServerCallTime()),
                    "db_time": float(one_work_process.getAvgDBCallTime()),
                    "lock_time": float(one_work_process.getAvgLockCallTime()),
                    "threads": float(one_work_process.getAvgThreads()),
                    "work_process_id": one_work_process.getWorkingProcessId().toString(),
                    "getSelectionSize": one_work_process.getSelectionSize(),
                    "getAvgBackCallTime": float(one_work_process.getAvgBackCallTime()),
                    "getMemoryExcessTime": one_work_process.getMemoryExcessTime()
                }
            )
        return result
    except Exception as ex:
        raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
