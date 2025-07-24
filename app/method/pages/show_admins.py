from loguru import logger
from nicegui import run, ui

from ..data.gen_table_method.get_admins import get_admins


def show_admins(connect_info, main_container):
    main_container.clear()
    with main_container.classes('justify-center items-center grow'):
        ui.spinner('gears', size='6em')
    ui.timer(0.5, once=True, callback=lambda: load_data(container=main_container, connect_info=connect_info))


async def load_data(container, connect_info):
    # main_container = container
    try:
        # cluster_admins_list = rac.java_get_cluster_admins()
        new_data = await run.io_bound(get_admins, connect_info=connect_info)
    except Exception as ex:
        ui.notify(ex, type='negative', position='top-right')
        logger.error(ex)
        container.clear()
        return
    container.clear()
    with container.classes('justify-start items-start'):
        ui.button(icon='autorenew', on_click=lambda: show_admins(main_container=container, connect_info=connect_info)).classes('ml-auto')
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
                "columnDefs": new_data["columns"],
                "rowData": new_data["data"],
                "rowSelection": "multiple",
            },
            auto_size_columns=True
        ).classes('ag-theme-balham-dark grow')  # h-full
