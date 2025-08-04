from nicegui import run, ui

from .del_agent_admin import del_agent_admin
from .update_table_data import update_table_data


async def del_agent_admins(table, connect_info, del_button):
    del_button.disable()
    agent_admin_to_del = await table.run_grid_method('getSelectedRows')
    for one_agent_admin_to_del in agent_admin_to_del:
        try:
            await run.io_bound(del_agent_admin, remove_admin_name=one_agent_admin_to_del['name'], connect_info=connect_info)
            ui.notify(message=f"Администратора агента {one_agent_admin_to_del['name']} успешно удален", type='positive', position='top-right')
        except Exception as ex:
            ui.notify(message=f"Попытка удалить администратора агента {one_agent_admin_to_del['name']} завершилась неудачей. Текст ошибки: {ex}", type='negative', position='top-right')
    await update_table_data(table=table, connect_info=connect_info)
    del_button.enable()
