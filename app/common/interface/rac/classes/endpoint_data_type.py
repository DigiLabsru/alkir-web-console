from enum import Enum


class EndpointDataType(Enum):
    VOID_MESSAGE = b'\x00'
    MESSAGE = b'\x01'
    EXCEPTION = b'\xff'
