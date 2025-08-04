

from loguru import logger
from nicegui import run, ui

from .del_cluster_admins import del_cluster_admins
from .get_cluster_admins import get_cluster_admins
from .show_add_user import show_add_user
from .update_table_data import update_table_data

show_admins_default_classes: str = 'nicegui-column w-[79%] h-full text-aqua bg-[#2A2A2A] rounded-lg p-2 flex-col'
greed_classes: str = 'ml-5 text-custom-green p-0 gap-2 text-xs w-full justify-center items-center'


def show_cluster_admins(connect_info, main_container):
    main_container.clear()
    main_container.classes.clear()
    with main_container.classes(f'{show_admins_default_classes} justify-center items-center grow'):
        ui.spinner('gears', size='6em')
        ui.timer(0.5, once=True, callback=lambda: load_data(container=main_container, connect_info=connect_info))


async def load_data(container, connect_info):
    # main_container = container
    try:
        new_data = await run.io_bound(get_cluster_admins, connect_info=connect_info)
    except Exception as ex:
        ui.notify(ex, type='negative', position='top-right')
        logger.error(ex)
        container.clear()
        return
    container.clear()
    container.classes.clear()
    with container.classes(f'{show_admins_default_classes} justify-start items-start'):
        with ui.row().classes('w-full justify-end items-center gap-2'):
            ui.button(icon='person_add', on_click=lambda: show_add_user(connect_info=connect_info, table=table))
            ui.button(icon='autorenew', on_click=lambda: update_table_data(table=table, connect_info=connect_info))  # .classes('ml-auto')
        table = ui.aggrid(
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
                "columnDefs": new_data["columns"],
                "rowData": new_data["data"],
                "rowSelection": "multiple",
            },
            auto_size_columns=True
        ).classes('ag-theme-balham-dark grow')  # h-full
        del_button = ui.button('Удалить выбранных администраторов агента', on_click=lambda: del_cluster_admins(
            table=table, connect_info=connect_info, del_button=del_button)).classes('w-full font-bold rounded flex-none')
