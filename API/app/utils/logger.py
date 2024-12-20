from logger import Logger

class LoggerServer(Logger):

    def __init__(self, add_text = ""):
        super().__init__("server/", add_text)