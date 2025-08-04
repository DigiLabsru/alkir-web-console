from ...common.interface.ras.ras import RasInterface


def del_agent_admin(remove_admin_name, connect_info):
    try:
        rac = RasInterface(req=connect_info)
        rac.java_unreg_agent_admin(remove_admin_name=remove_admin_name)
        rac.close()
    except Exception as ex:
        raise Exception(f"При удалении администратора агента произошла ошибка. Текст ошибки: {ex}")
