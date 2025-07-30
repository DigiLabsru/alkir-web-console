from ..data_method import (
    date_from_int64,
    read_bool,
    read_bytes,
    read_int32,
    read_int64,
    read_string,
    read_uuid,
)


async def read_infobase(packet):
    infobase = {}
    infobase['infobase'] = read_uuid(packet)
    infobase['date_offset'] = read_int32(packet)
    infobase['dbms'] = await read_string(packet)
    infobase['db_name'] = await read_string(packet)
    infobase['db_password'] = await read_bytes(packet)
    infobase['db_server_name'] = await read_string(packet)
    infobase['db_user'] = await read_string(packet)
    infobase['denied_from'] = date_from_int64(read_int64(packet))
    infobase['denied_message'] = await read_string(packet)
    infobase['denied_parameter'] = await read_string(packet)
    infobase['denied_to'] = date_from_int64(read_int64(packet))
    infobase['descr'] = await read_string(packet)
    infobase['locale'] = await read_string(packet)
    infobase['name'] = await read_string(packet)
    infobase['permission_code'] = await read_string(packet)
    infobase['scheduled_jobs_denied'] = read_bool(packet)
    infobase['security_level'] = read_int32(packet)
    infobase['sessions_denied'] = read_bool(packet)
    infobase['license_distribution'] = read_int32(packet)
    infobase['external_connection_string'] = await read_string(packet)
    infobase['external_session_manager_required'] = read_bool(packet)
    infobase['securirty_profile'] = await read_string(packet)
    infobase['safe_mode_securirty_profile'] = await read_string(packet)
    infobase['reserve_working_processes'] = read_bool(packet)
    return infobase
