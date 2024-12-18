import json
from rapidfuzz import process
from utils import Config
from datetime import timedelta
from app.db.mysql import SQLProvider
from app.db.redis import Redis
from app.utils.logger import LoggerServer 

config_recommend = Config().get_nested_value("system.recommend")

def get_products():
    if not config_recommend:
        LoggerServer().get_logger().log_error("Dữ liệu cài đặt của hệ thống recommend không được tìm thấy!")
        return []
    config_search_hint = config_recommend["search_hint"]
    redis_client = Redis.get_redis_connection()
    cache_key = config_search_hint["key_redis"]
    cached_data = redis_client.get(cache_key)
    if cached_data:
        LoggerServer().get_logger().log_info("Đang lấy dữ liệu từ Redis...")
        if isinstance(cached_data, bytes):
            cached_data = cached_data.decode("utf-8")
        return json.loads(cached_data)
    else:
        sql_provider = SQLProvider()
        LoggerServer().get_logger().log_info("Đang lấy dữ liệu từ MySQL...")
        products = sql_provider.execute_query(
            "SELECT "
            + ", ".join(config_search_hint["columns_target"])
            + " FROM "
            + config_search_hint["name_table_target"]
        )
        redis_client.setex(cache_key, timedelta(seconds=3600), json.dumps(products))
        return products

def hint_search(query, product_list, n=5):
    results = process.extract(query, product_list, limit=n, score_cutoff=50)
    return [result[0] for result in results]
