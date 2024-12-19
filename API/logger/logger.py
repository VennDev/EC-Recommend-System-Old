from datetime import datetime
import os

class Logger:

    child_path = ""
    name_path = "logs/"
    add_text = ""

    def __init__(self, child_path = "", add_text = ""):
        self.child_path = child_path
        self.add_text = add_text
        self.name_path = f"logs/{child_path}"
    
    def set_add_text(self, add_text):
        self.add_text = add_text

    def log(self, text: str):
        os.makedirs(self.name_path, exist_ok=True)

        timestamp = datetime.now().strftime("%H:%M:%S")
        text = f"[{timestamp}] {text}"
        print(text)

        log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(f"{self.name_path}/{log_filename}", "a", encoding="utf-8") as file:
            file.write(text + "\n")

    def log_error(self, text: str):
        self.log("[ERROR] " + self.add_text + " " + text)

    def log_info(self, text: str):
        self.log("[INFO] " + self.add_text + " " + text)

    def log_warning(self, text: str):
        self.log("[WARNING] " + self.add_text + " " + text)

    def log_debug(self, text: str):
        self.log("[DEBUG] " + self.add_text + " " + text)

    def log_critical(self, text: str):
        self.log("[CRITICAL] " + self.add_text + " " + text)

    def log_exception(self, exception: Exception):
        self.log("[EXCEPTION] " + self.add_text + " " + str(exception))

    def log_traceback(self, traceback: str):
        self.log("[TRACEBACK] " + self.add_text + " " + traceback)

    def log_request(self, request: str):
        self.log("[REQUEST] " + self.add_text + " " + request)

    def log_response(self, response: str):
        self.log("[RESPONSE] " + self.add_text + " " + response)

    def log_line(self):
        self.log("-" * 25 + self.add_text + "-" * 25)
