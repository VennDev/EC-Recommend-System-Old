from logger import Logger

class LoggerAI:

    def get_logger(self, add_text = "") -> Logger:
        return Logger("ai/", add_text)