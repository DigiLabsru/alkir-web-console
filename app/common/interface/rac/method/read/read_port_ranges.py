from ..data_method import read_uint16, unpack_varint_base128


async def read_port_ranges(packet):
    ranges_array = []
    ras_data_count = await unpack_varint_base128(packet)
    for ras_data_number in range(ras_data_count):
        port_max = read_uint16(packet)
        port_min = read_uint16(packet)
        ranges_array.append((port_min, port_max))
    return ranges_array
