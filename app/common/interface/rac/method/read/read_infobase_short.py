from ..data_method import read_string, read_uuid


async def read_infobase_short(packet):
    infobase = {}
    infobase['infobase'] = read_uuid(packet)
    infobase['descr'] = await read_string(packet)
    infobase['name'] = await read_string(packet)
    return infobase
