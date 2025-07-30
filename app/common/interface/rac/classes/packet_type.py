from enum import Enum


class PacketType(Enum):
    NEGOTIATE = b'\x00'
    CONNECT = b'\x01'
    CONNECT_ACK = b'\x02'
    DISCONNECT = b'\x04'
    ENDPOINT_OPEN = b'\x0b'
    ENDPOINT_OPEN_ACK = b'\x0c'
    ENDPOINT_CLOSE = b'\x0d'
    ENDPOINT_MESSAGE = b'\x0e'
    ENDPOINT_FAILURE = b'\x0f'
    KEEP_ALIVE = b'\x10'
