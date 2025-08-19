# flake8: noqa
import re

from nicegui import run, ui

# from .create_agent_admin import create_agent_admin
# from .update_table_data import update_table_data

greed_classes: str = 'ml-5 text-custom-green p-0 gap-0 text-xs w-full justify-center items-center'
card_classes: str = 'w-full justify-center items-center gap-0'


async def show_add_cluster(connect_info, table):
    new_agent_admin_data: dict = {}
    with ui.dialog().props('persistent') as dialog, ui.card():
        with ui.column().classes('w-full justify-start items-start gap-0'):
            ui.label('Параметры кластера:')
            with ui.card().classes(card_classes):
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label("Имя кластера:")
                    cluster_name = ui.input().props('dense')
                    ui.label('Компьютер:')
                    hostname = ui.input().props('dense')
                    ui.label('Порт:')
                    port = ui.input().props('dense')
                    ui.label('Защищенное соединение:')
                    port = ui.input().props('dense')
                    ui.label('Разрешить запись событий аудита прав доступа:')
                    access_audit = ui.checkbox().props('dense')
            ui.label('Перезапускать рабочие процессы:')
            with ui.card().classes(card_classes):
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label('Расписание перезапуска:')
                    restart_cron = ui.input().props('dense')
                    ui.label('Принудительно завершать проблемные процессы:')
                    force_process_restart = ui.checkbox().props('dense')
                    ui.label('Записывать дамп процесса при превышении критического объема памяти:')
                    create_dump = ui.checkbox().props('dense')
            with ui.card().classes(card_classes):
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label('Проблемные процессы завершать через:')
                    problem_process_force_restart_delay = ui.input().props('dense')
                    ui.label('Уровень отказоустойчивости:')
                    fultolerance_level = ui.input().props('dense')
                    ui.label('Режим распределения нагрузки:')
                    loadbalance_type = ui.input().props('dense')
            ui.label('Отслеживание разрыва соединений:')
            with ui.card().classes(card_classes):
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label('Период проверки:')
                    keepalived_peroiod = ui.input().props('dense')
                    ui.label('Таймаут проверки:')
                    keepalived_timeout = ui.input().props('dense')

        def validate_inputs():
            # login_val = user_login.value.strip()
            # descr_val = user_descr.value.strip()
            # pwd1 = local_pwd_one.value
            # pwd2 = local_pwd_two.value
            # os_user_val = os_user.value.strip()
            # # 1. Проверка user_login и user_descr
            # valid_name_pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ0-9_-]{1,}$')
            # valid_pwd_pattern = re.compile(r'^[a-zA-Z0-9_-]{0,}$')
            # if not valid_name_pattern.match(login_val):
            #     ui.notify('Имя пользователя должно содержать минимум 1 символ: буквы, цифры, "_" или "-"', type='negative')
            #     return False
            # else:
            #     new_agent_admin_data['new_admin_name'] = login_val
            # if not valid_name_pattern.match(descr_val):
            #     ui.notify('Описание должно содержать минимум 1 символ: буквы, цифры, "_" или "-"', type='negative')
            #     return False
            # else:
            #     new_agent_admin_data['new_admin_descr'] = descr_val
            # # 2. Проверка совпадения паролей
            # if local_auth.value:
            #     if pwd1 != pwd2:
            #         ui.notify('Пароли не совпадают', type='negative')
            #         return False
            #     if not valid_pwd_pattern.match(pwd1):
            #         ui.notify('Пароль должен содержать только английские буквы, цифры или знаки "-", "_"', type='negative', position='top-right')
            #         return False
            #     new_agent_admin_data['new_admin_password'] = pwd1
            #     new_agent_admin_data['new_admin_password_auth_allowed'] = True
            # # 3. Проверка os_user
            # if os_auth.value:
            #     valid_os_user_pattern = re.compile(r'^[a-zA-Z\\]{2,}$')
            #     if not valid_os_user_pattern.match(os_user_val):
            #         ui.notify('Имя пользователя ОС должно содержать только английские буквы и "\\"', type='negative', position='top-right')
            #         return False
            #     else:
            #         new_agent_admin_data['new_admin_sys_user_name'] = os_user_val
            #         new_agent_admin_data['new_admin_sys_auth_allowed'] = True
            # if local_auth.value is False and os_auth.value is False:
            #     ui.notify('Должен быть выбран один из вариантов аутентификации (локальный или доменный)', type='negative', position='top-right')
            #     return False
            return True

        async def create_user():
            if validate_inputs():
                try:
                    # await run.io_bound(create_agent_admin, connect_info=connect_info, user_data=new_agent_admin_data)
                    ui.notify('Кластер успешно создан', type='positive', position='top-right')
                    # await update_table_data(table=table, connect_info=connect_info)
                except Exception as ex:
                    ui.notify(ex, type='negative', position='top-right')
                finally:
                    dialog.close()
        with ui.row().classes('w-full justify-center items-center gap-2'):
            ui.button('Создать', on_click=create_user)
            ui.button('Отмена', on_click=dialog.close)

    dialog.open()
