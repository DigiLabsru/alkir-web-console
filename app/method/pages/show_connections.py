from nicegui import run, ui

from ..data.gen_table_method.get_all_connections import get_all_connections

show_connections_default_classes: str = 'nicegui-column w-[79%] h-full text-aqua bg-[#2A2A2A] rounded-lg p-2 flex-col'


def show_connections(connect_info, main_container):
    main_container.clear()
    main_container.classes.clear()
    with main_container.classes(f'{show_connections_default_classes} justify-center items-center grow'):
        ui.spinner('gears', size='6em')
        ui.timer(0.5, once=True, callback=lambda: load_data(main_container=main_container, connect_info=connect_info))


async def load_data(connect_info, main_container):
    data = await run.io_bound(get_all_connections, connect_info=connect_info)
    main_container.clear()
    main_container.classes.clear()
    with main_container.classes(show_connections_default_classes):
        with ui.row().classes('w-full'):
            ui.label(data["header"]).classes('text-custom-green text-sm')
            ui.button(icon='autorenew', on_click=lambda: show_connections(main_container=main_container, connect_info=connect_info)).classes('ml-auto')
            with ui.button(icon='menu'):
                with ui.menu(), ui.column().classes('gap-0 p-2'):
                    for column in data["columns"]:
                        field = column.get('field')
                        is_visible = not column.get('hide', False)
                        ui.switch(column['headerName'], value=is_visible, on_change=lambda e, f=field: table.run_grid_method('setColumnsVisible', [f], e.value))
        with ui.column().classes('text-custom-green text-sm w-full h-full flex flex-col'):
            with ui.element().classes('w-full grow min-h-0'):
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
                        # 'pagination': True,
                        # 'paginationPageSize': 30,
                        # 'domLayout': 'autoHeight',
                        "rowSelection": "multiple",
                        # 'suppressDragLeaveHidesColumns': True
                    },
                    auto_size_columns=True
                ).classes('ag-theme-balham-dark w-full h-full')


# def update_table_data(table, header, connect_info):
#     new_data = get_all_connections(connect_info=connect_info)
#     header.set_text(new_data["header"])
#     table.options["rowData"] = new_data["data"]
#     table.update()
