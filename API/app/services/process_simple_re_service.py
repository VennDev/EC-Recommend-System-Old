import json
from utils import Config
from datetime import timedelta
from app.db.redis import Redis
from app.utils.logger import LoggerServer 

def process_data_simple_recommend(index_data: str) -> any:
    from app.db.mysql import SQLProvider
    config_recommend = Config().get_nested_value("system.recommends_available")
    if not config_recommend:
        LoggerServer().log_error("Dữ liệu cài đặt của hệ thống recommend không được tìm thấy!")
        return []
    config_search_hint = config_recommend[index_data]
    redis_client = Redis.get_redis_connection()
    cache_key = config_search_hint["key_redis"]
    cached_data = redis_client.get(cache_key)
    if cached_data:
        LoggerServer().log_info("Đang lấy dữ liệu từ Redis...")
        if isinstance(cached_data, bytes):
            cached_data = cached_data.decode("utf-8")
        return json.loads(cached_data)
    else:
        sql_provider = SQLProvider()
        LoggerServer().log_info("Đang lấy dữ liệu từ MySQL...")
        products = sql_provider.execute_query(
            "SELECT "
            + ", ".join(config_search_hint["columns_target"])
            + " FROM "
            + config_search_hint["name_table_target"]
        )
        redis_client.setex(cache_key, timedelta(seconds=3600), json.dumps(products))
        return products