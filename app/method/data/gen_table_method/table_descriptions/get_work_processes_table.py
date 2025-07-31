# suppressMovable - не дает перемещать столбец
# hide - скрывает столбец
# suppressSizeToFit=true
columns = [
    {"headerName": "Компьютер", "field": "hostname", 'checkboxSelection': True},
    {"headerName": "Время старта", "field": "start_time"},
    {"headerName": "Память", "field": "memory", "valueFormatter": 'formatBytes(value)'},
    {"headerName": "Соединений", "field": "connections"},
    {"headerName": "Порт", "field": "port"},
    {"headerName": "Использование", "field": "use"},
    {"headerName": "Включен", "field": "enable"},
    {"headerName": "Активен", "field": "active"},
    {"headerName": "Резервный", "field": "reserve"},
    {"headerName": "Доступная производительность", "field": "available_performance"},
    {"headerName": "Лицензия", "field": "license"},
    {"headerName": "Реакция сервера", "field": "server_speed"},
    {"headerName": "Затрачено сервером", "field": "server_time"},
    {"headerName": "Затрачено СУБД", "field": "db_time"},
    {"headerName": "Затрачено менеджером блокировок", "field": "lock_time"},
    {"headerName": "Клиентских потоков", "field": "threads"},
    {"headerName": "ID рабочего процесса", "field": "work_process_id"},
    {"headerName": "getSelectionSize", "field": "getSelectionSize"},
    {"headerName": "getAvgBackCallTime", "field": "getAvgBackCallTime"},
    {"headerName": "getMemoryExcessTime", "field": "getMemoryExcessTime"},
    {"headerName": "PID OS", "field": "os_pid"},
    {"headerName": "Производительность", "field": "performance"},
    {"headerName": "PID", "field": "pid"},
]
