from ...common.interface.ras.ras import RasInterface
from ...common.schemas.request import NewAdmin


def create_agent_admin(connect_info, user_data):
    try:
        rac = RasInterface(req=connect_info)
        admins_list = rac.java_get_agent_admins()
        for one_admin in admins_list:
            if one_admin.getName() == user_data['new_admin_name']:
                raise Exception(f"Администратор агента с именем {user_data['new_admin_name']} уже существует")
        rac.java_reg_agent_admin(agent_admin_property=NewAdmin(
            new_admin_name=user_data['new_admin_name'],
            new_admin_descr=user_data['new_admin_descr'],
            new_admin_password=user_data.get('new_admin_password', ""),
            new_admin_password_auth_allowed=user_data.get('new_admin_password_auth_allowed', False),
            new_admin_sys_auth_allowed=user_data.get('new_admin_sys_auth_allowed', False),
            new_admin_sys_user_name=user_data.get('new_admin_sys_user_name', "")
        )
        )
        rac.close()
    except Exception as ex:
        raise Exception(f"При добавлении админа кластера произошла ошибка. Текст ошибки: {ex}")
