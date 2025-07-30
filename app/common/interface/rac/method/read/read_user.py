from ..data_method import read_bool, read_bytes, read_string


async def read_user(packet):
    user = {}
    user['name'] = await read_string(packet)
    user['descr'] = await read_string(packet)
    user['password'] = await read_bytes(packet)
    user['password_auth_allowed'] = read_bool(packet)
    user['sys_auth_allowed'] = read_bool(packet)
    user['sys_user_name'] = await read_string(packet)
    return user
