from ..data_method import write_bool


def write_user(user, packet):
    packet.append(user['name'].encode())
    packet.append(user['descr'].encode())
    packet.append(user['password'].encode())
    packet.append_raw(write_bool(user['password_auth_allowed']))
    packet.append_raw(write_bool(user['sys_auth_allowed']))
    packet.append(user['sys_user_name'].encode())
