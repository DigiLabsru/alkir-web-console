from ..data_method import write_bool, write_int32, write_uint16


def write_cluster(cluster, packet):
    packet.append_raw(cluster['cluster'].bytes)
    packet.append_raw(write_int32(cluster['expiration-timeout']))
    packet.append(cluster['host'].encode())
    packet.append_raw(write_int32(cluster['lifetime-limit']))
    packet.append_raw(write_uint16(cluster['port']))
    packet.append_raw(write_int32(cluster['max-memory-size']))
    packet.append_raw(write_int32(cluster['max-memory-time-limit']))
    packet.append(cluster['name'].encode())
    packet.append_raw(write_int32(cluster['security-level']))
    packet.append_raw(write_int32(cluster['session-fault-tolerance-level']))
    packet.append_raw(write_int32(0 if cluster['load-balancing-mode'] == 'performance' else 1))
    packet.append_raw(write_int32(cluster['errors-count-threshold']))
    packet.append_raw(write_bool(cluster['kill-problem-processes']))
    packet.append_raw(write_bool(cluster['kill-by-memory-with-dump']))
