# import argparse
# /workspaces/alkir-web-rac/!clear_python_rac/source/com/_1c/v8/ibis/internal/admin/ServiceUtils.java - описание ответов на java
import asyncio
import struct
import uuid
from pprint import pp


async def ras_command(ras_args):
    # установка соединения
    pass
    reader, writer = await asyncio.open_connection(
        host=ras_args['ras_host'],
        port=ras_args['ras_port']
        # ras_args.ras_host, ras_args.ras_port
    )
    # инициация подключения. делаем пакет для подключения и пытаемся цепанутся
    data = struct.pack(">ihh", 475223888, 256, 256)  # magic numbers voodoo numbers
    writer.write(data)
    # создаем пакет подключения
    packet = Packet(PacketType.CONNECT)
    packet.append_raw(b'\x01')
    packet.append(b'connect.timeout')
    packet.append_raw(ParamType.INT.value + struct.pack(">i", 2000))
    send_packet(writer, packet)
    # чтение ответа
    packet_type, packet_array = await read_packet(reader)
    assert packet_type == PacketType.CONNECT_ACK
    assert len(packet_array) == 0
    # SERVICE_VERSIONS = Arrays.asList("3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0", "11.0", "12.0", "13.0", "14.0", "15.0", "16.0");
    packet = Packet(PacketType.ENDPOINT_OPEN)
    packet.append(b'v8.service.Admin.Cluster')
    packet.append(b'50.0')
    send_packet(writer, packet)
    packet_type, packet_array = await read_packet(reader)
    assert packet_type == PacketType.ENDPOINT_OPEN_ACK
    assert packet_array[0] == b'v8.service.Admin.Cluster'
    assert packet_array[1] == b'10.0'
    endpoint_id = packet_array[2]
    pass
    # формируем пакет чтобы запросить нужные нам данные - тут запрашиваем данные по кластеру
    packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_CLUSTERS_REQUEST)
    # отправляем в RAS запрос
    send_packet(writer, packet)
    # читаем ответ от RAS и его форматируем
    packet_type, packet_array = await read_packet(reader)
    assert packet_type == PacketType.ENDPOINT_MESSAGE
    pp(packet_array)

    if (hasattr(ras_args, 'agent_user') and hasattr(ras_args, 'agent_pwd')
            and ras_args.agent_user is not None and ras_args.agent_pwd is not None):
        packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.AUTHENTICATE_AGENT_REQUEST)
        packet.append(ras_args.agent_user.encode())
        packet.append(ras_args.agent_pwd.encode())
        send_packet(writer, packet)
        packet_type, packet_array = await read_packet(reader)
        assert packet_type == PacketType.ENDPOINT_MESSAGE

    if (hasattr(ras_args, 'cluster_user') and hasattr(ras_args, 'cluster_pwd')
            and ras_args.cluster_user is not None and ras_args.cluster_pwd is not None):
        packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.AUTHENTICATE_REQUEST)
        packet.append_raw(uuid.UUID(ras_args.cluster).bytes)
        packet.append(ras_args.cluster_user.encode())
        packet.append(ras_args.cluster_pwd.encode())
        send_packet(writer, packet)
        packet_type, packet_array = await read_packet(reader)
        assert packet_type == PacketType.ENDPOINT_MESSAGE

    if ras_args.command == 'agent':
        if ras_args.subcommand1 == 'admin':
            if ras_args.subcommand2 == 'list':
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_AGENT_ADMINS_REQUEST)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
                pp(packet_array)
            elif ras_args.subcommand2 == 'register':
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.REG_AGENT_ADMIN_REQUEST)
                user = {}
                user['name'] = ras_args.name
                user['descr'] = ras_args.descr
                user['password'] = ras_args.pwd
                user['password_auth_allowed'] = "pwd" in ras_args.auth
                user['sys_auth_allowed'] = "os" in ras_args.auth
                user['sys_user_name'] = ras_args.os_user
                write_user(user, packet)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
            elif ras_args.subcommand2 == 'remove':
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.UNREG_AGENT_ADMIN_REQUEST)
                packet.append(ras_args.name.encode())
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE

    if ras_args.command == 'cluster':
        if ras_args.subcommand1 == 'list':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_CLUSTERS_REQUEST)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            pp(packet_array)
        elif ras_args.subcommand1 == 'info' or ras_args.subcommand1 == 'update':
            cluster_id = uuid.UUID(ras_args.cluster).bytes
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_CLUSTER_INFO_REQUEST)
            packet.append_raw(cluster_id)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            if ras_args.subcommand1 == 'info':
                pp(packet_array)
            else:
                cluster = packet_array[0]
                if ras_args.lifetime_limit is not None:
                    cluster['lifetime-limit'] = ras_args.lifetime_limit
                if ras_args.expiration_timeout is not None:
                    cluster['expiration-timeout'] = ras_args.expiration_timeout
                if ras_args.name is not None:
                    cluster['name'] = ras_args.name
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.REG_CLUSTER_REQUEST)
                write_cluster(cluster, packet)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
        elif ras_args.subcommand1 == 'admin':
            if ras_args.subcommand2 == 'list':
                cluster_id = uuid.UUID(ras_args.cluster).bytes
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_CLUSTER_ADMINS_REQUEST)
                packet.append_raw(cluster_id)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
                pp(packet_array)
            elif ras_args.subcommand2 == 'register':
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.REG_CLUSTER_ADMIN_REQUEST)
                packet.append_raw(uuid.UUID(ras_args.cluster).bytes)
                user = {}
                user['name'] = ras_args.name
                user['descr'] = ras_args.descr
                user['password'] = ras_args.pwd
                user['password_auth_allowed'] = "pwd" in ras_args.auth
                user['sys_auth_allowed'] = "os" in ras_args.auth
                user['sys_user_name'] = ras_args.os_user
                write_user(user, packet)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
            elif ras_args.subcommand2 == 'remove':
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.UNREG_CLUSTER_ADMIN_REQUEST)
                packet.append_raw(uuid.UUID(ras_args.cluster).bytes)
                packet.append(ras_args.name.encode())
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE

    if ras_args.command == 'infobase':
        cluster_id = uuid.UUID(ras_args.cluster).bytes
        if ras_args.subcommand1 == 'summary' and ras_args.subcommand2 == 'list':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_INFOBASES_SHORT_REQUEST)
            packet.append_raw(cluster_id)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            pp(packet_array)

        if hasattr(ras_args, 'infobase_user') and hasattr(ras_args,
                                                          'infobase_pwd') and ras_args.infobase_user is not None and ras_args.infobase_pwd is not None:
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.ADD_AUTHENTICATION_REQUEST)
            packet.append_raw(cluster_id)
            packet.append(ras_args.infobase_user.encode())
            packet.append(ras_args.infobase_pwd.encode())
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE

        if ras_args.subcommand1 == 'create':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.CREATE_INFOBASE_REQUEST)
            packet.append_raw(cluster_id)
            infobase = {}
            infobase['infobase'] = uuid.UUID(int=0)
            infobase['date_offset'] = ras_args.date_offset
            infobase['dbms'] = ras_args.dbms
            infobase['db_name'] = ras_args.db_name
            infobase['db_password'] = ras_args.db_pwd.encode()
            infobase['db_server_name'] = ras_args.db_server
            infobase['db_user'] = ras_args.db_user
            infobase['denied_from'] = None
            infobase['denied_message'] = ''
            infobase['denied_parameter'] = ''
            infobase['denied_to'] = None
            infobase['descr'] = ras_args.descr
            infobase['locale'] = ras_args.locale
            infobase['name'] = ras_args.name
            infobase['permission_code'] = ''
            infobase['scheduled_jobs_denied'] = ras_args.scheduled_jobs_deny == 'on'
            infobase['security_level'] = ras_args.security_level
            infobase['sessions_denied'] = False
            infobase['license_distribution'] = int(ras_args.license_distribution == 'allow')
            infobase['external_connection_string'] = ""
            infobase['external_session_manager_required'] = False
            infobase['securirty_profile'] = ""
            infobase['safe_mode_securirty_profile'] = ""
            infobase['reserve_working_processes'] = False
            write_infobase(infobase, packet)
            packet.append_raw(write_int32(int(ras_args.create_database)))
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            pp(packet_array)

        if ras_args.subcommand1 == 'drop':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.DROP_INFOBASE_REQUEST)
            packet.append_raw(cluster_id)
            packet.append_raw(uuid.UUID(ras_args.infobase).bytes)
            mode = 0
            if ras_args.drop_database:
                mode = 1
            elif ras_args.clear_database:
                mode = 2
            packet.append_raw(write_int32(mode))
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE

        if ras_args.subcommand1 == 'info' or ras_args.subcommand1 == 'update':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_INFOBASE_INFO_REQUEST)
            packet.append_raw(cluster_id)
            packet.append_raw(uuid.UUID(ras_args.infobase).bytes)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            if ras_args.subcommand1 == 'update':
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.UPDATE_INFOBASE_REQUEST)
                packet.append_raw(cluster_id)
                infobase = packet_array[0]
                if ras_args.descr is not None:
                    infobase['descr'] = ras_args.descr
                if ras_args.denied_message is not None:
                    infobase['denied_message'] = ras_args.denied_message
                if ras_args.permission_code is not None:
                    infobase['permission_code'] = ras_args.permission_code
                if ras_args.sessions_deny in ['on', 'off']:
                    infobase['sessions_denied'] = ras_args.sessions_deny == 'on'
                if ras_args.scheduled_jobs_deny in ['on', 'off']:
                    infobase['scheduled_jobs_denied'] = ras_args.scheduled_jobs_deny == 'on'
                if ras_args.denied_from is not None:
                    infobase['denied_from'] = ras_args.denied_from
                if ras_args.denied_to is not None:
                    infobase['denied_to'] = ras_args.denied_to
                write_infobase(infobase, packet)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
            else:
                pp(packet_array)

    if ras_args.command == 'session':
        cluster_id = uuid.UUID(ras_args.cluster).bytes
        session_ids = []
        session_info = {}
        if ras_args.subcommand1 == 'list' or (ras_args.subcommand1 == 'terminate' and not ras_args.session):
            if hasattr(ras_args, 'infobase') and ras_args.infobase:
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_INFOBASE_SESSIONS_REQUEST)
                packet.append_raw(cluster_id)
                packet.append_raw(uuid.UUID(ras_args.infobase).bytes)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
                if ras_args.subcommand1 == 'list':
                    pp(packet_array)
                else:
                    session_ids.extend(
                        [session['session_id'].bytes for session in packet_array if session['app_id'] != 'RAS'])
                    session_info.update({session['session_id'].bytes: session for session in packet_array})
            else:
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_SESSIONS_REQUEST)
                packet.append_raw(cluster_id)
                send_packet(writer, packet)
                packet_type, packet_array = await read_packet(reader)
                assert packet_type == PacketType.ENDPOINT_MESSAGE
                if ras_args.subcommand1 == 'list':
                    pp(packet_array)
                else:
                    session_ids.extend(
                        [session['session_id'].bytes for session in packet_array if session['app_id'] != 'RAS'])
                    session_info.update({session['session_id'].bytes: session for session in packet_array})
        if ras_args.subcommand1 == 'terminate':
            if ras_args.session:
                session_id = uuid.UUID(ras_args.session).bytes
                session_ids.append(session_id)
            for session_id in session_ids:
                packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.TERMINATE_SESSION_REQUEST)
                packet.append_raw(cluster_id)
                packet.append_raw(session_id)
                if hasattr(ras_args, 'error_message') and ras_args.error_message:
                    packet.append(ras_args.error_message.encode())
                else:
                    packet.append(b'Session terminated by admin')
                send_packet(writer, packet)
                try:
                    packet_type, packet_array = await read_packet(reader)
                    assert packet_type == PacketType.ENDPOINT_MESSAGE
                    if session_id in session_info.keys():
                        print("Terminated session", uuid.UUID(bytes=session_id), session_info[session_id]['app_id'])
                    else:
                        print("Terminated session", uuid.UUID(bytes=session_id))
                except MessageException as e:
                    print("Can't terminate session", uuid.UUID(bytes=session_id), "-", e)

    if ras_args.command == 'server':
        cluster_id = uuid.UUID(ras_args.cluster).bytes
        if ras_args.subcommand1 == 'list':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_WORKING_SERVERS_REQUEST)
            packet.append_raw(cluster_id)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            pp(packet_array)
        elif ras_args.subcommand1 == 'info':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.GET_WORKING_SERVER_INFO_REQUEST)
            packet.append_raw(cluster_id)
            packet.append_raw(uuid.UUID(ras_args.server).bytes)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            pp(packet_array)
        elif ras_args.subcommand1 == 'remove':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.UNREG_WORKING_SERVER_REQUEST)
            packet.append_raw(cluster_id)
            packet.append_raw(uuid.UUID(ras_args.server).bytes)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            pp(packet_array)
        elif ras_args.subcommand1 == 'insert':
            packet = Packet(PacketType.ENDPOINT_MESSAGE, MessageType.REG_WORKING_SERVER_REQUEST)
            packet.append_raw(cluster_id)
            server = {}
            server['working_server_id'] = uuid.UUID(int=0)
            server['host_name'] = ras_args.agent_host
            server['main_port'] = ras_args.agent_port
            server['name'] = ras_args.name
            server['main_server'] = ras_args.using == 'main'
            server['safe_working_processes_memory_limit'] = ras_args.safe_working_processes_memory_limit
            server['safe_call_memory_limit'] = ras_args.safe_call_memory_limit
            server['infobases_per_working_process_limit'] = ras_args.infobases_limit
            server['working_process_memory_limit'] = ras_args.memory_limit
            server['connections_per_working_process_limit'] = ras_args.connections_limit
            server['cluster_main_port'] = ras_args.cluster_port
            server['dedicated_managers'] = ras_args.dedicate_managers == 'all'
            server['port_ranges'] = [(int(v.split(':')[0]), int(v.split(':')[1])) for v in ras_args.port_range]
            # version >= 8
            server['critical_processes_total_memory'] = ras_args.critical_total_memory
            server['temporary_allowed_processes_total_memory'] = ras_args.temporary_allowed_total_memory
            server['temporary_allowed_processes_total_memory_time_limit'] = ras_args.temporary_allowed_total_memory_time_limit
            write_server(server, packet)
            send_packet(writer, packet)
            packet_type, packet_array = await read_packet(reader)
            assert packet_type == PacketType.ENDPOINT_MESSAGE
            pp(packet_array)

    packet = Packet(PacketType.ENDPOINT_CLOSE)
    packet.append(pack_varint_base64(endpoint_id))
    send_packet(writer, packet)
    packet = Packet(PacketType.DISCONNECT)
    send_packet(writer, packet)


if __name__ == '__main__':
    # args = parser.parse_args()
    args = {
        # "ras_host": "172.16.237.150",
        # "ras_port": 1545
        "ras_host": "192.168.217.4",
        "ras_port": 1645
    }
    # 172.16.237.150 1545
    asyncio.run(ras_command(args))
