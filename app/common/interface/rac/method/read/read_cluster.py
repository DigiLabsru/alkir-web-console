from ..data_method import read_bool, read_int32, read_string, read_uint16, read_uuid


async def read_cluster(packet):
    cluster = {}
    cluster['cluster'] = read_uuid(packet)
    cluster['expiration-timeout'] = read_int32(packet)
    cluster['host'] = await read_string(packet)
    cluster['lifetime-limit'] = read_int32(packet)
    cluster['port'] = read_uint16(packet)
    cluster['max-memory-size'] = read_int32(packet)  # deprecated
    cluster['max-memory-time-limit'] = read_int32(packet)  # deprecated
    cluster['name'] = await read_string(packet)
    cluster['security-level'] = read_int32(packet)
    cluster['session-fault-tolerance-level'] = read_int32(packet)
    cluster['load-balancing-mode'] = 'performance' if read_int32(packet) == 0 else 'memory'
    cluster['errors-count-threshold'] = read_int32(packet)  # deprecated
    cluster['kill-problem-processes'] = int(read_bool(packet))
    cluster['kill-by-memory-with-dump'] = int(read_bool(packet))
    return cluster
