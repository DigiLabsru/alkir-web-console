from nicegui import ui


def show_clusters(connect_info, main_container):
    main_container.clear()
    central_admin = connect_info.central_admin if connect_info.central_admin != '' else 'Не задан'
    with main_container.classes('p-4 gap-4 h-full flex flex-col'):
        with ui.row().classes('w-[99%] mx-auto justify-between items-center mb-4 flex-none'):
            ui.label(f"Сервер подключения: {connect_info.ras_server}").classes('text-custom-green text-sm')
        with ui.row().classes('w-[99%] mx-auto justify-between items-center mb-4 flex-none'):
            ui.label(f"Порт подключения: {connect_info.ras_port}").classes('text-custom-green text-sm')
        with ui.row().classes('w-[99%] mx-auto justify-between items-center mb-4 flex-none'):
            ui.label(f"Логин центрального агента: {central_admin}").classes('text-custom-green text-sm')
