import uvicorn
from logging import Logger
from app.utils.logger import LoggerServer
from utils import Config
from app.main import app

config = Config().get("app_settings")
if config == None:
    raise Exception("Dữ liệu cấu hình không thể tìm thấy!")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config["port"])
    LoggerServer().get_logger().log_info("\n\n")