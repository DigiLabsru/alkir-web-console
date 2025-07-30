class MessageException(BaseException):
    def __init__(self, service_id, message):
        self.service_id = service_id
        self.message = message
        super().__init__(self.service_id + ": " + self.message)
