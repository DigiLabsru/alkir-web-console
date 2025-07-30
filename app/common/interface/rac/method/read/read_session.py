from ..data_method import (
    read_bool,
    read_int32,
    read_int64,
    read_string,
    read_uuid,
    unpack_varint_base64,
)


async def read_session(packet):
    session = {}
    session['session_id'] = read_uuid(packet)
    session['app_id'] = await read_string(packet)
    session['blocked_by_dbms'] = read_int32(packet)
    session['blocked_by_ls'] = read_int32(packet)
    session['bytes_all'] = read_int64(packet)
    session['bytes_last5min'] = read_int64(packet)
    session['calls_all'] = read_int32(packet)
    session['calls_last5min'] = read_int64(packet)
    session['connection_id'] = read_uuid(packet)
    session['dbms_bytes_all'] = read_int64(packet)
    session['dbms_bytes_last5min'] = read_int64(packet)
    session['db_proc_info'] = await read_string(packet)
    session['db_proc_took'] = read_int32(packet)
    session['db_proc_took_at'] = read_int64(packet)
    session['duration_all'] = read_int32(packet)
    session['duration_all_dbms'] = read_int32(packet)
    session['duration_current'] = read_int32(packet)
    session['duration_current_dbms'] = read_int32(packet)
    session['duration_last_5_min'] = read_int64(packet)
    session['duration_last_5_min_dbms'] = read_int64(packet)
    session['host'] = await read_string(packet)
    session['infobase_id'] = read_uuid(packet)
    session['last_active_at'] = read_int64(packet)
    session['hibernate'] = read_bool(packet)
    session['passive_session_hibernate_time'] = read_int32(packet)
    session['hibernate_session_terminate_time'] = read_int32(packet)
    session['licenses'] = []
    lic_count = await unpack_varint_base64(packet)
    for lic_number in range(lic_count):
        lic = {}
        lic['full_name'] = await read_string(packet)
        lic['full_presentation'] = await read_string(packet)
        lic['issued_by_server'] = read_bool(packet)
        lic['license_type'] = read_int32(packet)
        lic['max_users_all'] = read_int32(packet)
        lic['max_users_cur'] = read_int32(packet)
        lic['net'] = read_bool(packet)
        lic['rmngr_address'] = await read_string(packet)
        lic['rmngr_pid'] = await read_string(packet)
        lic['rmngr_port'] = read_int32(packet)
        lic['series'] = await read_string(packet)
        lic['short_presentation'] = await read_string(packet)
        session['licenses'].append(lic)
    session['locale'] = await read_string(packet)
    session['process_id'] = read_uuid(packet)
    session['id'] = read_int32(packet)
    session['started_at'] = read_int64(packet)
    session['user_name'] = await read_string(packet)
    # version >= 4
    session['memory_current'] = read_int64(packet)
    session['memory_last5min'] = read_int64(packet)
    session['memory_total'] = read_int64(packet)
    session['read_current'] = read_int64(packet)
    session['read_last5min'] = read_int64(packet)
    session['read_total'] = read_int64(packet)
    session['write_current'] = read_int64(packet)
    session['write_last5min'] = read_int64(packet)
    session['write_total'] = read_int64(packet)
    # version >= 5
    session['duration_current_service'] = read_int32(packet)
    session['duration_last5min_service'] = read_int64(packet)
    session['duration_all_service'] = read_int32(packet)
    session['current_service_name'] = await read_string(packet)
    # version >= 6
    session['cpu_time_current'] = read_int64(packet)
    session['cpu_time_last5min'] = read_int64(packet)
    session['cpu_time_total'] = read_int64(packet)
    # version >= 7
    session['data_separation'] = await read_string(packet)
    # version >= 10
    session['client_ip_address'] = await read_string(packet)
    return session
