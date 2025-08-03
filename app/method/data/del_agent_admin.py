from ...common.interface.ras.ras import RasInterface


def del_agent_admin(remove_admin_name, connect_info):
    try:
        rac = RasInterface(req=connect_info)
        # admins_list = rac.java_get_agent_admins()
        # login_find_flsg: bool = False
        # for one_admin in admins_list:
        #     if one_admin.getName() == remove_admin_name:
        #         login_find_flsg = True
        # if login_find_flsg is False:
        #     return {
        #         "error": 1,
        #         "message": f"Администратор агента с именем {remove_admin_name} в списку существующих не найден",
        #         "data": ""
        #     }
        rac.java_unreg_agent_admin(remove_admin_name=remove_admin_name)
        # admins_list = rac.java_get_agent_admins()
        rac.close()
        return [False, ""]
    except Exception as ex:
        return [True, ex]
