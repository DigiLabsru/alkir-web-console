# app/core/java_runtime.py

import jpype

# AgentAdminConnectorFactory = None
# java_logger = None


def init_jvm(root_path):
    if not jpype.isJVMStarted():
        jpype.startJVM(
            classpath=[
                f"{root_path}/common/interface/ras/lib/*"
            ],
            convertStrings=True
        )
    # global AgentAdminConnectorFactory, java_logger
    AgentAdminConnectorFactory = jpype.JClass("com._1c.v8.ibis.admin.client.AgentAdminConnectorFactory")
    java_logger = jpype.JClass("java.util.logging.Logger").getLogger("")
    return {"AgentAdminConnectorFactory": AgentAdminConnectorFactory, "java_logger": java_logger}


def shutdown_jvm():
    jpype.shutdownJVM()
