from loguru import logger
from nicegui import run, ui

from ..data.gen_table_method.get_work_processes import get_work_processes

show_admins_default_classes: str = 'nicegui-column w-[79%] h-full text-aqua bg-[#2A2A2A] rounded-lg p-2 flex-col'


def show_work_processes(connect_info, main_container):
    main_container.clear()
    main_container.classes.clear()
    with main_container.classes(f'{show_admins_default_classes} justify-center items-center grow'):
        ui.spinner('gears', size='6em')
        ui.timer(0.5, once=True, callback=lambda: load_data(container=main_container, connect_info=connect_info))


async def load_data(container, connect_info):
    # main_container = container
    try:
        new_data = await run.io_bound(get_work_processes, connect_info=connect_info)
    except Exception as ex:
        ui.notify(ex, type='negative', position='top-right')
        logger.error(ex)
        container.clear()
        return
    container.clear()
    container.classes.clear()
    with container.classes(f'{show_admins_default_classes} justify-start items-start'):
        ui.button(icon='autorenew', on_click=lambda: show_work_processes(main_container=container, connect_info=connect_info)).classes('ml-auto')
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
