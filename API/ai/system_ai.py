import signal
import time
from ai.models.svd.svd_model import SVDModel
from ai.utils.types_model import TypesModel, UtilsTypeModel
from ai.utils.logger import LoggerAI
from utils.config import Config

class SystemAI:

    def __init__(self) -> None:
        pass

    def run(self):
        LoggerAI().get_logger().log_info("Hệ thống AI đang được chạy!")
        config = Config("ai_config.yml").get_nested_value("system.recommend_ai")
        if config == None:
            raise Exception("Lỗi không thể tìm thấy dữ liệu để huấn luyện AI!")
        list_types_model = UtilsTypeModel().get_list_types_model()
        for model_type in list_types_model:
            list_models = config[model_type]
            for case, value in list_models.items():
                if model_type == TypesModel.SVD_TYPE.value:
                    SVDModel(case, value).run()

        def signal_handler(sig, frame):
            LoggerAI().get_logger().log_info("Chương trình đang dừng!")
            exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        LoggerAI().get_logger().log_info("Chương trình đang chạy... Nhấn Ctrl+C để dừng.\n")

        while True:
            time.sleep(1)
