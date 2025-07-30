from ..method.data_method import pack_varint_base128, varint_prefixed_data_base64
from .packet_type import PacketType


class Packet():
    def __init__(self, packet_type, message_type=None):
        self.data = []
        self.type = packet_type
        if packet_type == PacketType.ENDPOINT_MESSAGE:
            self.append_header()
            self.append_raw(message_type.value)

    def append(self, element):
        self.data.append(varint_prefixed_data_base64(element))

    def append_raw(self, element):
        self.data.append(element)

    def append_header(self):
        self.append_raw(b'\x01\x00\x00\x01')

    def get_parts(self):
        body = b''.join(self.data)
        if self.type != PacketType.ENDPOINT_MESSAGE:
            body += b'\x80'
        packet_length = pack_varint_base128(len(body))
        header = self.type.value + packet_length
        return header, body
