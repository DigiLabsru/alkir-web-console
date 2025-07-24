# suppressMovable - не дает перемещать столбец
# hide - скрывает столбец
# suppressSizeToFit=true
columns = [
    {"headerName": "№", "field": "count", 'filter': False, 'checkboxSelection': True},
    {"headerName": "Приложение", "field": "app_id"},
    # {"headerName": "blocked_by_ls", "field": "blocked_by_ls"},
    {"headerName": "Соединение", "field": "conn_id"},
    {"headerName": "Начало работы", "field": "connected_at"},
    {"headerName": "Имя хоста", "field": "host"},
    # {"headerName": "info_base_connection_id", "field": "info_base_connection_id"}, # Для показа информации о сессии наверное
    {"headerName": "Имя базы", "field": "infobase_id"},
    {"headerName": "Сеанс", "field": "session_number"},
    {"headerName": "Сервер", "field": "server"},
    {"headerName": "Порт", "field": "port"},
    {"headerName": "Pid процесса", "field": "pid"}
    # ]
    # blocked_by_ls
    # conn_id
    # connected_at
    # host
    # info_base_connection_id
    # infobase_id
    # session_number
    # working_process_id
    # },
]
