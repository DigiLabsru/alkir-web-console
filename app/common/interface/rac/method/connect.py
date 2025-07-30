import asyncio
import struct

from ..classes.packet_type import PacketType
from ..classes.param_type import ParamType


class Connection():
    async def connect(self):
        reader, writer = await asyncio.open_connection(
            host=self.ras_server,
            port=self.ras_port
        )
    # инициация подключения. делаем пакет для подключения и пытаемся цепанутся
        data = struct.pack(">ihh", 475223888, 256, 256)  # magic numbers voodoo numbers
        writer.write(data)
        # создаем пакет подключения
        packet = self.Packet(PacketType.CONNECT)
        packet.append_raw(b'\x01')
        packet.append(b'connect.timeout')
        packet.append_raw(ParamType.INT.value + struct.pack(">i", 2000))
        self.send_packet(writer, packet)
        # чтение ответа
        packet_type, packet_array = await self.read_packet(reader)
        pass
