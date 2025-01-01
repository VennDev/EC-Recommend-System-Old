from typing import Any
from app.services.process_simple_re_service import process_data_simple_recommend
from app.services.process_query_service import process_query_with_rapidfuzz
from app.services.re_products_service import recommend_products_simple
from app.utils.logger import LoggerServer
from utils.config import Config

def process_simple_recommend_router(index_target: str, limit: int, input_data: Any):
    try:
        config_data = Config().get_nested_value(
            "system.recommends_available." + index_target
        )
        if not config_data:
            raise ValueError(f"Cấu hình {index_target} không tồn tại")

        columns_key = config_data.get("columns_key")
        if not columns_key or not isinstance(columns_key, list):
            raise ValueError("Cấu hình thiếu 'columns_key' hoặc không phải danh sách")

        data_input = process_data_simple_recommend(index_target)
        data = recommend_products_simple(index_target, columns_key, data_input, limit)
        if not data:
            return {"suggestions": []}

        data_column_key = [
            " ".join(str(value[key]) for key in columns_key if key in value)
            for value in data
        ]

        score_cutoff = config_data.get("score_cutoff", 30)
        suggestions = process_query_with_rapidfuzz(
            input_data, data_column_key, limit, score_cutoff
        )

        just_first_case = [suggestion[0] for suggestion in suggestions]
        list_suggestions = [
            item for item in data if " ".join(
                str(item[key]) for key in columns_key if key in item
            ) in just_first_case
        ]

        return {"suggestions": list_suggestions}
    except Exception as e:
        LoggerServer().log_error(
            "Đã có lỗi xảy ra trong quá trình xử lý hàm process_simple_recommend_router: "
            + str(e)
        )
        return {"error": str(e)}