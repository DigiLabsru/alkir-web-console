from enum import Enum


class ParamType(Enum):
    UNKNOWN_TYPE = b'\x00'
    BOOLEAN = b'\x01'
    BYTE = b'\x02'
    SHORT = b'\x03'
    INT = b'\x04'
    LONG = b'\x05'
    FLOAT = b'\x06'
    DOUBLE = b'\x07'
    SIZE = b'\x08'
    NULLABLE_SIZE = b'\x09'
    STRING = b'\x0a'
    UUID = b'\x0b'
    TYPE = b'\x0c'
    ENDPOINT_ID = b'\x0d'
