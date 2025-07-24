from nicegui import run, ui

from ..data.del_sessions import del_sessions
from ..data.gen_table_method.get_all_sessions import get_all_sessions


def show_sessions(connect_info, main_container):
    data = get_all_sessions(connect_info=connect_info)
    main_container.clear()
    with main_container:
        # Контейнер для кнопки с выравниванием и отступами
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
                            "columnGroupShow": "closed"
                        },
                        "autoSizeStrategy": {
                            "type": 'fitCellContents'
                        },
                        "suppressRowClickSelection": True,
                        "enableCellTextSelection": True,
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
            del_button = ui.button('Отключить выбранные сессии', on_click=lambda: drop_session(table=table, connect_info=connect_info,
                                   header=header, del_button=del_button)).classes('w-full font-bold rounded flex-none')


async def drop_session(table, connect_info, header, del_button):
    del_button.disable()
    session_to_kill = await table.run_grid_method('getSelectedRows')
    for one_session_to_kill in session_to_kill:
        error, message = await run.io_bound(del_sessions, session_to_kill=session_to_kill[0], connect_info=connect_info)
        if error is False:
            ui.notify(message=f"Сессия пользователя {one_session_to_kill['user_name']} успешно завершена", type='positive', position='top-right')
        else:
            ui.notify(message=f"Попытка завершить сессию пользователя {one_session_to_kill['user_name']} завершилась неудачей. Текст ошибки: {message}", type='negative', position='top-right')
    await update_table_data(table=table, header=header, connect_info=connect_info)
    del_button.enable()


async def update_table_data(table, header, connect_info):
    # new_data = get_all_sessions(connect_info=connect_info)
    new_data = await run.io_bound(get_all_sessions, connect_info=connect_info)
    header.set_text(new_data["header"])
    table.options["rowData"] = new_data["data"]
    table.update()
