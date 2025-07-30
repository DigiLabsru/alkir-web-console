from ..data_method import write_bool, write_int32, write_int64, write_uint16
from .write_port_ranges import write_port_ranges


def write_server(server, packet):
    packet.append_raw(server['working_server_id'].bytes)
    packet.append(server['host_name'].encode())
    packet.append_raw(write_uint16(server['main_port']))
    packet.append(server['name'].encode())
    packet.append_raw(write_bool(server['main_server']))
    packet.append_raw(write_int64(server['safe_working_processes_memory_limit']))
    packet.append_raw(write_int64(server['safe_call_memory_limit']))
    packet.append_raw(write_int32(server['infobases_per_working_process_limit']))
    packet.append_raw(write_int64(server['working_process_memory_limit']))
    packet.append_raw(write_int32(server['connections_per_working_process_limit']))
    packet.append_raw(write_uint16(server['cluster_main_port']))
    packet.append_raw(write_bool(server['dedicated_managers']))
    write_port_ranges(server['port_ranges'], packet)
    # version >= 8
    packet.append_raw(write_int64(server['critical_processes_total_memory']))
    packet.append_raw(write_int64(server['temporary_allowed_processes_total_memory']))
    packet.append_raw(write_int64(server['temporary_allowed_processes_total_memory_time_limit']))
