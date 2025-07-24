from pydantic import BaseModel, Field


class BaseRequest(BaseModel):
    cluster_admin: str = Field(title='Админ кластера', description='Админ кластера', default="")
    cluster_pwd: str = Field(title='Пароль админа кластера', description='Пароль админа кластера', default="")
    central_admin: str = Field(title='Админ центрального кластера', description='Админ центрального кластера', default="")
    central_pwd: str = Field(title='Пароль админа центрального кластера', description='Пароль админа центрального кластера', default="")
    ras_server: str = Field(title='Адрес RAS', description='Адрес RAS')
    ras_port: int = Field(title='Порт RAS', description='Порт RAS', default=1545)
    timeout: int = Field(title='Таймаут на коннект к серверу', description='Таймаут на коннект к серверу', default=2000)
    cluster_name: str = Field(title='Имя кластера', description='Имя кластера. Если на сервере один кластер получается автоматически.', default=None)
    cluster_id: str = Field(title='ID кластера', description='ID кластера. Если на сервере один кластер получается автоматически.', default=None)
    debug: bool = Field(title='Отладка запроса', default=False)


class OneUser(BaseModel):
    login: str
    pwd: str


class StartSettings(BaseModel):
    server_list: list[BaseRequest] = Field(title='Список серверов')


class UserList(BaseModel):
    user_list: list[OneUser] = Field(title='Список пользователей')
