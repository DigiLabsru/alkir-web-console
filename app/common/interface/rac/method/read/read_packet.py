import io

from ...classes.endpoint_data_type import EndpointDataType
from ...classes.message_exception import MessageException
from ...classes.message_type import MessageType
from ...classes.packet_type import PacketType
from ..data_method import (
    read_bytes,
    read_string,
    read_uuid,
    unpack_varint_base64,
    unpack_varint_base128,
)
from .read_cluster import read_cluster
from .read_infobase import read_infobase
from .read_infobase_short import read_infobase_short
from .read_server import read_server
from .read_session import read_session
from .read_user import read_user


async def read_packet(reader):
    packet_type = PacketType(await reader.read(1))
    packet_size = await unpack_varint_base128(reader)
    packet_data = (await reader.readexactly(packet_size))
    packet = io.BytesIO(packet_data)
    packet_array = []
    if packet_type == PacketType.ENDPOINT_OPEN_ACK:
        packet_array.append(await read_bytes(packet))
        packet_array.append(await read_bytes(packet))
        packet_array.append(await unpack_varint_base64(packet))
    elif packet_type == PacketType.ENDPOINT_FAILURE:
        service_id = await read_string(packet)
        version = await read_string(packet)
        version
        endpoint_id = await unpack_varint_base128(packet)
        class_cause = await read_bytes(packet)
        class_cause
        message = await read_string(packet)
        raise MessageException(service_id, message)
    elif packet_type == PacketType.ENDPOINT_MESSAGE:
        endpoint_id = await unpack_varint_base128(packet)
        endpoint_id
        endpoint_format = packet.read(2)
        endpoint_format
        endpoint_data_type = EndpointDataType(packet.read(1))
        if endpoint_data_type == EndpointDataType.EXCEPTION:
            service_id = await read_string(packet)
            message = await read_string(packet)
            raise MessageException(service_id, message)
        if endpoint_data_type == EndpointDataType.MESSAGE:
            raw_ras_data_type = packet.read(1)
            ras_data_type = MessageType(raw_ras_data_type)
            if ras_data_type == MessageType.GET_CLUSTER_INFO_RESPONSE:
                cluster = await read_cluster(packet)
                packet_array.append(cluster)
            elif ras_data_type == MessageType.GET_INFOBASE_INFO_RESPONSE:
                infobase = await read_infobase(packet)
                packet_array.append(infobase)
            elif ras_data_type == MessageType.GET_WORKING_SERVER_INFO_RESPONSE:
                server = await read_server(packet)
                packet_array.append(server)
            elif ras_data_type in [MessageType.CREATE_INFOBASE_RESPONSE, MessageType.REG_WORKING_SERVER_RESPONSE]:
                packet_array.append(read_uuid(packet))
            else:
                ras_data_count = await unpack_varint_base128(packet)
                for ras_data_number in range(ras_data_count):
                    if ras_data_type == MessageType.GET_CLUSTERS_RESPONSE:
                        cluster = await read_cluster(packet)
                        packet_array.append(cluster)
                    elif ras_data_type == MessageType.GET_INFOBASES_SHORT_RESPONSE:
                        infobase = await read_infobase_short(packet)
                        packet_array.append(infobase)
                    elif ras_data_type in [MessageType.GET_INFOBASE_SESSIONS_RESPONSE,
                                           MessageType.GET_SESSIONS_RESPONSE]:
                        session = await read_session(packet)
                        packet_array.append(session)
                    elif ras_data_type in [MessageType.GET_CLUSTER_ADMINS_RESPONSE,
                                           MessageType.GET_AGENT_ADMINS_RESPONSE]:
                        user = await read_user(packet)
                        packet_array.append(user)
                    elif ras_data_type == MessageType.GET_WORKING_SERVERS_RESPONSE:
                        server = await read_server(packet)
                        packet_array.append(server)

    return packet_type, packet_array
