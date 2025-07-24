# app/gui/pages/main_page.py
from nicegui import ui

from ..method.pages.update_tree import update_tree


def create_main_page():
    from ..main import start_settings
    ui.colors(primary="#88B236")
    ui.add_head_html('''
        <style>
            body {
                height: 100vh;  /* Используем viewport height */
                background: #141414;
            }
            .nicegui-content {
                height: 100vh !important;
            }
        </style>
        <script>
        function formatBytes(value) {
            const size = value;
            const units = ['B', 'KB', 'MB', 'GB', 'TB'];
            let index = 0;
            let s = size;
            while (s >= 1024 && index < units.length - 1) {
            s /= 1024;
            index++;
            }
            return s.toFixed(1) + ' ' + units[index];
        }
        </script>
    ''')
    with ui.row().classes('w-full h-full'):
        # Левая панель
        with ui.column().classes('w-[19%] h-full bg-[#2A2A2A] p-2 rounded-lg flex-col'):
            root_select = ui.select(
                options={_.ras_server: f'{_.ras_server}:{_.ras_port}' for _ in start_settings.server_list},
                label='Выберите сервер',
                with_input=True,
                on_change=lambda e: update_tree(server=e.value, containers={"tree_container": tree_container, "main_container": main_container, "root_select": root_select})
            ).classes('w-full rounded-lg flex-none').props(add='outlined')
            # Контейнер для дерева
            tree_container = ui.element().classes('flex w-full min-h-0 grow overflow-y-auto')
            ui.button('Выйти', on_click=handle_logout).classes('w-full font-bold rounded-lg flex-none')
        # Правая панель
        main_container = ui.column().classes('w-[79%] h-full text-aqua bg-[#2A2A2A] rounded-lg p-2 flex-col')


def handle_logout():
    ui.navigate.to('/logout')
