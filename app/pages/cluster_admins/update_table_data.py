from nicegui import run

from .get_cluster_admins import get_cluster_admins


async def update_table_data(table, connect_info):
    # new_data = get_all_sessions(connect_info=connect_info)
    new_data = await run.io_bound(get_cluster_admins, connect_info=connect_info)
    table.options["rowData"] = new_data["data"]
    table.update()
