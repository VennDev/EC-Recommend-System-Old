from logger import Logger

class LoggerAI(Logger):

    def __init__(self, add_text = ""):
        super().__init__("ai/", add_text)