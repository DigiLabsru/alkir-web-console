from nicegui import ui

# from ...common.interface.rac.rac import RaсInterface


def show_clusters(connect_info, main_container):
    main_container.clear()
    main_container.classes.clear()
    main_container.classes('nicegui-column w-[79%] h-full text-aqua bg-[#2A2A2A] rounded-lg p-2')
    central_admin = connect_info.central_admin if connect_info.central_admin != '' else 'Не задан'
    card_classes: str = 'bg-[#2A2A2A]'
    greed_classes: str = 'ml-5 text-custom-green p-0 gap-2 text-xs w-full'
    pass
    with main_container.classes('p-4 gap-4 h-full'):
        with ui.card().classes(card_classes):
            with ui.grid(columns=2).classes(greed_classes):
                ui.label("Сервер подключения")
                ui.label(connect_info.ras_server)
                ui.label("Порт подключения")
                ui.label(connect_info.ras_port)
                ui.label("Логин центрального агента")
                ui.label(central_admin)
                # ui.label("Версия RAS")
                # ui.label("12")
