import uvicorn
from utils import Config
from ai.system_ai import SystemAI
from app.main import app

config = Config().get("app_settings")
if config == None:
    raise Exception("Dữ liệu cấu hình không thể tìm thấy!")

def run_system_ai():
    SystemAI().run()

if __name__ == "__main__":
    run_system_ai()
    uvicorn.run(app, host="0.0.0.0", port=config["port"])