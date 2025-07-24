# suppressMovable - не дает перемещать столбец
# hide - скрывает столбец
# suppressSizeToFit=true
columns = [
    {"headerName": "Имя пользователя (login для локальной учетной записи)", "field": "name", 'checkboxSelection': True},
    {"headerName": "Доменная учетная запись", "field": "domain_name"},
    {"headerName": "Разрешена локальная аутентификация", "field": "password_allow"},
    {"headerName": "Разрешена доменная аутентификация", "field": "domain_password_allow"},
    {"headerName": "Описание", "field": "descr"}
]
