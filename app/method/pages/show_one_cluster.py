from nicegui import ui

from ..data.gen_table_method.get_one_cluster_settings import get_cluster_info


def show_one_cluster(connect_info, main_container):
    data = get_cluster_info(connect_info)
    main_container.clear()
    greed_classes: str = 'ml-5 text-custom-green p-0 gap-2 text-xs w-full'
    card_classes: str = 'bg-[#2A2A2A] w-full'
    with main_container:
        with ui.tabs() as tabs:
            current = ui.tab('Текущие параметры', icon='preview')
            edit = ui.tab('Настройка', icon='edit')
        with ui.tab_panels(tabs, value=current).classes('bg-[#2A2A2A] w-full'):
            with ui.tab_panel(current).classes('w-full'):
                with ui.card().classes(card_classes):
                    ui.label("Параметры кластера:")
                    with ui.grid(columns=2).classes(greed_classes):
                        ui.label("Версия платформы:")
                        ui.label(data['platform_version'])
                        ui.label("Имя кластера:")
                        ui.label(data['name'])
                        ui.label("Компьютер:")
                        ui.label(data['host_name'])
                        ui.label("IP порт:")
                        ui.label(data['main_port'])
                        ui.label("Защищенное соединение")
                        ui.label(data['security_level'])
                        ui.label("Разрешать запись событий аудита прав доступа:")
                        ui.label(data['security_level'])
                with ui.card().classes(card_classes):
                    ui.label("Настройка перезапуска рабочих процессов")
                    with ui.grid(columns=2).classes(greed_classes):
                        ui.label("Расписание перезапуска:")
                        ui.label(data['security_level'])
                        ui.label("Принудительно завершать проблемные процессы:")
                        ui.label("Да" if data['cluster_recycling_kill_problem_processes'] is True else "Нет")
                        ui.label("Записывать дамп процесса при превышении критического объема памяти:")
                        ui.label("Да" if data['cluster_recycling_kill_by_memory_with_dump'] is True else "Нет")
                        ui.label("Проблемные процессы завершать через:")
                        ui.label(data['expiration_timeout'])
                with ui.card().classes(card_classes):
                    ui.label("Настройка высокой доступности кластера:")
                    with ui.grid(columns=2).classes(greed_classes):
                        ui.label("Уровень отказоустойчивости:")
                        ui.label(data['expiration_timeout'])
                        ui.label("Режим распределения нагрузки:")
                        ui.label(data['expiration_timeout'])
                with ui.card().classes(card_classes):
                    ui.label("Отслеживание разрыва соединений:")
                    with ui.grid(columns=2).classes(greed_classes):
                        ui.label("Период проверки:")
                        ui.label(data['expiration_timeout'])
                        ui.label("Таймаут проверки:")
                        ui.label(data['life_time_limit'])
            with ui.tab_panel(edit):
                ui.label("Параметры кластера:")
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label("Версия платформы:")
                    ui.label(data['platform_version'])
                    ui.label("Имя кластера:").classes('content-center')
                    # ui.label(data['name'])
                    ui.input(placeholder=data['name']).props('clearable outlined')
                    ui.label("Компьютер:")
                    ui.label(data['host_name'])
                    ui.label("IP порт:")
                    ui.label(data['main_port'])
                    ui.label("Защищенное соединение")
                    ui.label(data['security_level'])
                    ui.label("Разрешать запись событий аудита прав доступа:")
                    ui.label(data['security_level'])
                ui.separator()
                ui.label("Настройка перезапуска рабочих процессов")
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label("Расписание перезапуска:")
                    ui.label(data['security_level'])
                    ui.label("Принудительно завершать проблемные процессы:")
                    ui.label("Да" if data['cluster_recycling_kill_problem_processes'] is True else "Нет")
                    ui.label("Записывать дамп процесса при превышении критического объема памяти:")
                    ui.label("Да" if data['cluster_recycling_kill_by_memory_with_dump'] is True else "Нет")
                    ui.label("Проблемные процессы завершать через:")
                    ui.label(data['expiration_timeout'])
                ui.separator()
                ui.label("Настройка высокой доступности кластера:")
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label("Уровень отказоустойчивости:")
                    ui.label(data['expiration_timeout'])
                    ui.label("Режим распределения нагрузки:")
                    ui.label(data['expiration_timeout'])
                ui.separator()
                ui.label("Отслеживание разрыва соединений:")
                with ui.grid(columns=2).classes(greed_classes):
                    ui.label("Период проверки:")
                    ui.label(data['expiration_timeout'])
                    ui.label("Таймаут проверки:")
                    ui.label(data['life_time_limit'])
                ui.button("Сохранить", icon='save')
