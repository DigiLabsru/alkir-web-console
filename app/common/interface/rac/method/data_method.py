
import datetime
import io
import struct
import uuid


def pack_varint_base64(val):
    total = b''
    while val >= 0x40:
        bits = val & 0x3F
        val >>= 6
        total += struct.pack('B', (0x40 | bits))
    bits = val & 0x3F
    total += struct.pack('B', bits)
    return total


def pack_varint_base128(val):
    total = b''
    while val >= 0x80:
        bits = val & 0x7F
        val >>= 7
        total += struct.pack('B', (0x80 | bits))
    bits = val & 0x7F
    total += struct.pack('B', bits)
    return total


async def unpack_varint_base64(stream):
    total = 0
    shift = 0
    val = 0x40
    while val & 0x40:
        if type(stream) is io.BytesIO:
            data = stream.read(1)
        else:
            data = await stream.read(1)
        if data == b'':
            return None
        unpacked_data = struct.unpack('B', data)
        val = unpacked_data[0]
        total |= ((val & 0x3F) << shift)
        shift += 6
    return total


async def unpack_varint_base128(stream):
    total = 0
    shift = 0
    val = 0x80
    while val & 0x80:
        if type(stream) is io.BytesIO:
            data = stream.read(1)
        else:
            data = await stream.read(1)
        if data == b'':
            return None
        unpacked_data = struct.unpack('B', data)
        val = unpacked_data[0]
        total |= ((val & 0x7F) << shift)
        shift += 7
    return total


def varint_prefixed_data_base64(data):
    return pack_varint_base64(len(data)) + data


def read_uuid(reader):
    return uuid.UUID(bytes=reader.read(16))


def read_uint16(reader):
    return struct.unpack('>H', reader.read(2))[0]


def write_uint16(value):
    return struct.pack('>H', value)


def read_int32(reader):
    return struct.unpack('>i', reader.read(4))[0]


def write_int32(value):
    return struct.pack('>i', value)


def read_int64(reader):
    return struct.unpack('>q', reader.read(8))[0]


def write_int64(value):
    return struct.pack('>q', value)


async def read_bytes(reader):
    return reader.read(await unpack_varint_base64(reader))


async def read_string(reader):
    return (await read_bytes(reader)).decode()


def read_bool(reader):
    return reader.read(1) == b'\x01'


def write_bool(value):
    return b'\x01' if value == 1 or value is True else b'\x00'


def read_double(reader):
    return struct.unpack('>d', reader.read(8))[0]


def write_double(value):
    return struct.pack('>d', value)


def age_delta():
    return 621355968000000


def date_from_int64(value):
    if not value:
        return None
    return datetime.datetime.fromtimestamp((value - age_delta()) / 10000, datetime.timezone.utc)


def date_to_int64(value):
    if not value:
        return 0
    return int(value.timestamp() * 10000 + age_delta())
