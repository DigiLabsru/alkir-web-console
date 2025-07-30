from ..data_method import pack_varint_base128, write_uint16


def write_port_ranges(ranges_array, packet):
    packet.append_raw(pack_varint_base128(len(ranges_array)))
    for port_range in ranges_array:
        packet.append_raw(write_uint16(port_range[1]))
        packet.append_raw(write_uint16(port_range[0]))
