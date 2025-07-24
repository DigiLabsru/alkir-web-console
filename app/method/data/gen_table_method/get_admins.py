from ....common.interface.ras.ras import RasInterface
from .table_descriptions.get_admins_table import columns


def get_admins(connect_info):
    try:
        rac = RasInterface(req=connect_info)
        cluster_admins_list = rac.java_get_cluster_admins()
        rac.close()
    except Exception as ex:
        raise Exception(f"Произошла ошибка при получении данных из RAS. Текст ошибки: {ex}")
    try:
        result: list = {}
        result['columns'] = columns
        result['data'] = []
        for one_admin in cluster_admins_list:
            result_data: dict = {
                "descr": one_admin.getDescr(),
                "name": one_admin.getName(),
                "domain_name": one_admin.getSysUserName().replace("\\\\", "\\"),
                "password_allow": "✅" if one_admin.isPasswordAuthAllowed() is True else "❌",
                "domain_password_allow": "✅" if one_admin.isSysAuthAllowed() is True else "❌"
            }
            result['data'].append(result_data)
        return result
    except Exception as ex:
        raise Exception(f"Произошла ошибка при обработке данных. Текст ошибки: {ex}")
