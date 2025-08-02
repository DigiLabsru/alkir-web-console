from loguru import logger
from nicegui import run, ui

from ..data.gen_table_method.get_work_server import get_work_server

show_admins_default_classes: str = 'nicegui-column w-[79%] h-full text-aqua bg-[#2A2A2A] rounded-lg p-2 flex-col'


def show_work_server(connect_info, main_container, work_server_id: str):
    main_container.clear()
    main_container.classes.clear()
    with main_container.classes(f'{show_admins_default_classes} justify-center items-center grow'):
        ui.spinner('gears', size='6em')
    ui.timer(0.5, once=True, callback=lambda: load_data(container=main_container, connect_info=connect_info, work_server_id=work_server_id))


async def load_data(container, connect_info, work_server_id: str):
    # main_container = container
    try:
        # cluster_admins_list = rac.java_get_cluster_admins()
        new_data = await run.io_bound(get_work_server, connect_info=connect_info, work_server_id=work_server_id)
    except Exception as ex:
        ui.notify(ex, type='negative', position='top-right')
        logger.error(ex)
        container.clear()
        return
    container.clear()
    container.classes.clear()
    greed_classes: str = 'ml-5 text-custom-green p-0 gap-2 text-xs w-full'
    card_classes: str = 'bg-[#2A2A2A] w-full'
    with container.classes(f'{show_admins_default_classes} justify-start items-start'):
        ui.button(icon='autorenew', on_click=lambda: show_work_server(main_container=container, connect_info=connect_info, work_server_id=work_server_id)).classes('ml-auto')
        with ui.tabs() as tabs:
            work_server_settings = ui.tab('Параметры рабочего сервера')
            tnf = ui.tab('Требования назначения функциональности')
            # service_settings = ui.tab('Настройка сервисов')
        with ui.tab_panels(tabs, value=work_server_settings).classes('bg-[#2A2A2A] w-full'):
            with ui.tab_panel(work_server_settings).classes('w-full'):
                with ui.card().classes(card_classes):
                    ui.label("Параметры рабочего сервера:")
                    with ui.card().classes(card_classes):
                        with ui.grid(columns=2).classes(greed_classes):
                            ui.label("Описание сервера:")
                            ui.label(new_data['working_server_info']['host_name'])
                            ui.label("Компьютер:")
                            ui.label(new_data['working_server_info']['host_name'])
                            ui.label("IP порт:")
                            ui.label(new_data['working_server_info']['main_port'])
                            ui.label("Диапазоны IP порт:")
                            ui.label(f"{new_data['working_server_info']['port_ranges'][0]}:{new_data['working_server_info']['port_ranges'][1]}")
                            ui.label("Безопасный расход памяти на один вызов:")
                            ui.label(new_data['working_server_info']['safe_call_memory_limit'])
                            ui.label("Критический объем памяти процессов:")
                            ui.label(new_data['working_server_info']['critical_processes_total_memory'])
                            ui.label("Временно допустимый объем памяти процессов:")
                            ui.label(new_data['working_server_info']['temporary_allowed_processes_total_memory'])
                            ui.label("Интервал превышения допустимого объема памяти:")
                            ui.label(new_data['working_server_info']['temporary_allowed_processes_total_memory_time_limit'])
                            ui.label("Имя службы (SPN) сервиса 1С:Предприятия:")
                            ui.label()
                            ui.label("Расписание перезапуска")
                            ui.label()
                    ui.label("Параметры рабочих процессов:")
                    with ui.card().classes(card_classes):
                        with ui.grid(columns=2).classes(greed_classes):
                            ui.label("Количество ИБ на процесс:")
                            ui.label(new_data['working_server_info']['infobases_per_working_process_limit'])
                            ui.label("Количество соединений на процесс:")
                            ui.label(new_data['working_server_info']['connections_per_working_process_limit'])
                    with ui.card().classes(card_classes):
                        with ui.grid(columns=2).classes(greed_classes):
                            ui.label("Порт главного менеджера кластера:")
                            ui.label(new_data['working_server_info']['cluster_main_port'])
                            ui.label("Менеджер под каждый сервис:")
                            ui.label(new_data['working_server_info']['is_dedicated_managers'])
                            ui.label("Центральный сервер:")
                            ui.label(new_data['working_server_info']['is_main_server'])
            with ui.tab_panel(tnf):
                ui.aggrid(
                    options={
                        "defaultColDef": {
                            "filter": True
                        },
                        "defaultColGroupDef": {
                            "columnGroupShow": "closed"
                        },
                        "autoSizeStrategy": {
                            "type": 'fitCellContents'
                        },
                        "suppressRowClickSelection": True,
                        "enableCellTextSelection": True,
                        "columnDefs": new_data['assignment_rules']['columns'],
                        "rowData": new_data['assignment_rules']["data"],
                        "rowSelection": "multiple",
                    },
                    auto_size_columns=True
                ).classes('ag-theme-balham-dark grow')
            # with ui.tab_panel(service_settings):
            #     with ui.card().classes(card_classes):
            #         ui.label("Параметры кластера:")
            #         with ui.grid(columns=2).classes(greed_classes):
            #             ui.label("Настройка сервисов:")
            #             ui.label(work_server_id)
