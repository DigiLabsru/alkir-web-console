from ...common.interface.ras.ras import RasInterface


def del_sessions(session_to_kill, connect_info):
    try:
        rac = RasInterface(req=connect_info)
        rac.java_terminate_session(sid=session_to_kill['sid'])
        rac.close()
        return [False, ""]
    except Exception as ex:
        return [True, ex]
