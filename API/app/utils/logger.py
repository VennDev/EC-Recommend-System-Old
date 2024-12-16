from logger import Logger

class LoggerServer:

    def get_logger(self) -> Logger:
        return Logger("server/")