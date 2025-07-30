from data_method import (
    read_bool,
    read_int32,
    read_int64,
    read_string,
    read_uint16,
    read_uuid,
)

from .read_port_ranges import read_port_ranges


async def read_server(packet):
    server = {}
    server['working_server_id'] = read_uuid(packet)
    server['host_name'] = await read_string(packet)
    server['main_port'] = read_uint16(packet)
    server['name'] = await read_string(packet)
    server['main_server'] = read_bool(packet)
    server['safe_working_processes_memory_limit'] = read_int64(packet)
    server['safe_call_memory_limit'] = read_int64(packet)
    server['infobases_per_working_process_limit'] = read_int32(packet)
    server['working_process_memory_limit'] = read_int64(packet)
    server['connections_per_working_process_limit'] = read_int32(packet)
    server['cluster_main_port'] = read_uint16(packet)
    server['dedicated_managers'] = read_bool(packet)
    server['port_ranges'] = await read_port_ranges(packet)
    # version >= 8
    server['critical_processes_total_memory'] = read_int64(packet)
    server['temporary_allowed_processes_total_memory'] = read_int64(packet)
    server['temporary_allowed_processes_total_memory_time_limit'] = read_int64(packet)
    return server
