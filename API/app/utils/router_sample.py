from app.services.process_query_service import process_query_with_rapidfuzz
from app.services.process_simple_re_service import process_simple_recommend
from app.utils.logger import LoggerServer
from utils.config import Config

def process_simple_recommend_router(index_target: str, input_data: any):
    try:
        data = process_simple_recommend(index_target)
        if not data:
            return {"suggestions": []}

        config_data = Config().get_nested_value("system.recommend." + index_target)
        if not config_data:
            raise ValueError(f"Cấu hình {index_target} không tồn tại")

        column_key = config_data.get("column_key")
        if not column_key:
            raise ValueError("Cấu hình thiếu 'column_key'")

        data_column_key = [value.get(column_key) for value in data if column_key in value]
        
        limit = config_data.get("limit", 10)
        score_cutoff = config_data.get("score_cutoff", 10)

        suggestions = process_query_with_rapidfuzz(input_data, data_column_key, limit, score_cutoff)

        just_first_case = [suggestion[0] for suggestion in suggestions]
        list_suggestions = [item[column_key] for item in data if item[column_key] in just_first_case]
        return {"suggestions": list_suggestions}
    except Exception as e:
        LoggerServer().get_logger().log_error("Đã có lỗi xảy ra trong quá trình xử lý hàm process_simple_recommend_router: " + str(e))
        return {"error": str(e)}