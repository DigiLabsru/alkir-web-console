from nicegui import ui

from ..data.gen_table_method.get_all_connections import get_all_connections


def show_connections(connect_info, main_container):
    data = get_all_connections(connect_info=connect_info)
    main_container.clear()
    with main_container:
        with ui.row().classes('w-full'):
            header = ui.label(data["header"]).classes('text-custom-green text-sm')
            ui.button(icon='autorenew', on_click=lambda: update_table_data(table=table, header=header, connect_info=connect_info)).classes('ml-auto')
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


def update_table_data(table, header, connect_info):
    new_data = get_all_connections(connect_info=connect_info)
    header.set_text(new_data["header"])
    table.options["rowData"] = new_data["data"]
    table.update()
