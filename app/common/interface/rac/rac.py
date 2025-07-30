import socket

from ....common.schemas.request import BaseRequest, InfoBase
from .classes.packet import Packet
from .method.connect import Connection
from .method.send_packet import SendPacket


class RaсInterface(Connection, SendPacket, Packet):
    def __init__(self, req: BaseRequest | InfoBase, its_get_clusters: bool = False):
        self.ras_server: str = req.ras_server
        self.ras_port: int = req.ras_port
        self.cluster_admin: str = req.cluster_admin
        self.cluster_pwd: str = req.cluster_pwd
        self.central_admin: str = req.central_admin
        self.central_pwd: str = req.central_pwd
        self.timeout: str = req.timeout
        self.cluster_name: str = req.cluster_name
        self.cluster_id: str = req.cluster_id
        if isinstance(req, InfoBase):
            self.ib_admin: str = req.ib_admin
            self.ib_pwb: str = req.ib_pwb
            self.ib_id: str = req.ib_id
            self.ib_name: str = req.ib_name
        self.its_get_clusters = its_get_clusters
        self.reader = None
        self.writer = None
        self.endpoint_id = None
        try:
            with socket.create_connection((self.ras_server, self.ras_port), timeout=3):
                pass
        except (socket.timeout, ConnectionRefusedError, OSError):
            raise Exception(f"Не удалось установить сетевое соединение с {self.ras_server}:{self.ras_port}. Причины - сервер выключен, на указанном порту не запущена служба RAS, \
не открыт порт на целевом сервере в firewall, нет маршрута до целевого сервера.")
        try:
            pass
        except Exception:
            pass

    def close(self):
        if self.connector is not None:
            try:
                self.connector.shutdown()
            except Exception:
                pass
            finally:
                self.connector = None
