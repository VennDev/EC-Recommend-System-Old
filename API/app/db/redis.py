import redis
from utils import Config
from app.utils.logger import LoggerServer


class Redis:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_redis_connection():
        redis_config = Config().get("redis")
        if redis_config is None:
            LoggerServer().log_error("Dữ liệu cấu hình hệ thống không tồn tại")
            raise Exception("Dữ liệu cấu hình hệ thống không tồn tại")

        return redis.StrictRedis(
            host=redis_config["host"],
            port=redis_config["port"],
            password=redis_config["password"],
            ssl=redis_config["ssl"],
            decode_responses=True,
        )
