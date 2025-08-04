from nicegui import run, ui

from .get_all_clusters import get_all_clusters
from .show_add_cluster import show_add_cluster

show_clusters_default_classes: str = 'nicegui-column w-[79%] h-full text-aqua bg-[#2A2A2A] rounded-lg p-2 flex-col'


def show_clusters(connect_info, main_container):
    main_container.clear()
    main_container.classes.clear()
    with main_container.classes(f'{show_clusters_default_classes} justify-center items-center grow'):
        ui.spinner('gears', size='6em')
        ui.timer(0.5, once=True, callback=lambda: load_data(main_container=main_container, connect_info=connect_info))


async def load_data(connect_info, main_container):
    data = await run.io_bound(get_all_clusters, connect_info=connect_info)
    main_container.clear()
    main_container.classes.clear()
    with main_container.classes(f'{show_clusters_default_classes} justify-start items-start'):
        with ui.row().classes('w-full justify-end items-center gap-2'):
            ui.button(icon='domain_add', on_click=lambda: show_add_cluster(connect_info=connect_info, table=table))
            ui.button(icon='autorenew', on_click=lambda: show_clusters(main_container=main_container, connect_info=connect_info))
        table = ui.aggrid(
            options={
                "defaultColDef": {
                    "filter": True
                },
                "defaultColGroupDef": {
                    "columnGroupShow": "open"
                },
                "autoSizeStrategy": {
                    "type": 'fitCellContents'
                },
                "columnDefs": data["columns"],
                "rowData": data["data"],
                "rowSelection": "multiple",
                # 'suppressDragLeaveHidesColumns': True
            },
            auto_size_columns=True
        ).classes('ag-theme-balham-dark grow')
        del_button = ui.button('Удалить выбранные кластера', on_click=lambda: del_cluster(
            table=table, connect_info=connect_info, del_button=del_button)).classes('w-full font-bold rounded flex-none')


async def del_cluster(connect_info, table):
    pass
