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


#     with main_container.classes('p-4 gap-4 h-full flex flex-col'):
#         # Контейнер для кнопки с выравниванием и отступами
#         with ui.row().classes('w-[99%] mx-auto justify-between items-center mb-4 flex-none'):
#             header = ui.label(data["header"]).classes('text-custom-green text-sm')
#             ui.button(icon='autorenew', on_click=lambda: update_table_data(table=table, connect_info=connect_info, header=header)).classes('ml-auto')
#             with ui.button(icon='menu'):
#                 with ui.menu(), ui.column().classes('gap-0 p-2'):
#                     for column in data["columns"]:
#                         field = column.get('field')
#                         is_visible = not column.get('hide', False)
#                         ui.switch(column['headerName'], value=is_visible, on_change=lambda e, f=field: table.run_grid_method('setColumnsVisible', [f], e.value))
#             table = ui.aggrid(
#                 options={
#                     "defaultColDef": {
#                         "filter": True
#                     },
#                     "defaultColGroupDef": {
#                         "columnGroupShow": "open"
#                     },
#                     "autoSizeStrategy": {
#                         "type": 'fitCellContents'
#                     },
#                     "columnDefs": data["columns"],
#                     "rowData": data["data"],
#                     'pagination': True,
#                     'paginationPageSize': 30,
#                     # 'domLayout': 'autoHeight',
#                     "rowSelection": "multiple",
#                     # 'suppressDragLeaveHidesColumns': True
#                 },
#                 auto_size_columns=True
#             ).classes(add='ag-theme-balham-dark w-full h-96')

#             # async def drop_session(table):
#             #     selected_rows = await table.run_grid_method('getSelectedRows')
#             #     pass
#             #     return selected_rows
#             # ui.button('Отключить выбранные сессии', on_click=lambda: drop_session(table)).classes('w-full font-bold py-2 rounded')
#             ui.add_head_html('''
# <style>
#     .q-table__title {
#         color: #88B236 !important;
#     }
#     .my-sticky-header-table {
#         height: calc(85vh - 60px); /* Учитываем высоту верхней панели */
#     }

#     .my-sticky-header-table thead tr th {
#         position: sticky;
#         z-index: 2; /* Увеличиваем z-index */
#         background: #434343; /* Фон должен быть непрозрачным */
#         box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* Тень для разделения */
#         text-align: left !important;
#         color: #88B236 !important;
#     }

#     .my-sticky-header-table thead tr:first-child th {
#         color: #88B236 !important;
#         top: 0;
#         /* height: 48px;  Фиксированная высота заголовка */
#         text-align: left !important;
#     }

#     .my-sticky-header-table tbody td {
#         /* padding-top: 48px !important;  Отступ равный высоте заголовка */
#         color: #dedede !important;
#         background: #1f1f1f; /* Фон ячеек */
#         text-align: left !important;
#     }

#     .my-sticky-header-table tbody tr {
#         position: relative;
#         z-index: 1; /* Контент под заголовком */
#         text-align: left !important;
#     }
#     /* Основные настройки темы */
#     .ag-theme-balham-dark {
#         --ag-background-color: #1F1F1F;
#         --ag-foreground-color: #dedede;
#         --ag-header-background-color: #2A2A2A;
#         --ag-header-foreground-color: #88B236;
#         --ag-border-color: #434343;
#         --ag-row-hover-color: rgba(136, 178, 54, 0.1);
#         --ag-selected-row-background-color: rgba(136, 178, 54, 0.2);
#     }

#     /* Дополнительные стили */
#     .ag-header-cell-label {
#         justify-content: left !important;
#         font-weight: bold;
#     }

#     .ag-cell {
#         border-bottom: 1px solid var(--ag-border-color) !important;
#         padding-left: 12px !important;
#     }
# </style>
# ''')
