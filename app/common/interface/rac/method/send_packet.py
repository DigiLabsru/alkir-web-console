class SendPacket():
    def send_packet(writer, packet):
        header, body = packet.get_parts()
        writer.write(header)
        writer.write(body)
