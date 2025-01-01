from fastapi import APIRouter
from typing import Union
from fastapi import Depends
from utils import Config
from app.schemas.error import ErrorResponse
from app.schemas.suggestions import SuggestionsResponse
from app.dependencies.auth_dependency import auth_dependency

router = APIRouter()

@router.get(
    "/recommend-like-category/{categoryId}/{num_recommendations}",
    response_model=Union[SuggestionsResponse, ErrorResponse],
    dependencies=[Depends(auth_dependency)],
)
async def recommend_like_category(categoryId: str, num_recommendations: int = 5):
    from app.db.mysql import SQLProvider

    config_data = Config().get_nested_value(
        "system.recommends_available.recommend_like_category"
    )
    if config_data is None:
        return {"error": "Không tìm thấy mô hình AI"}

    sql_provider = SQLProvider()
    query_string = "SELECT * FROM " + config_data["name_table_target"]
    query_string += " WHERE "
    query_string += config_data["category_column"]
    query_string += " = '"
    query_string += str(categoryId)
    query_string += "' LIMIT "
    query_string += str(num_recommendations)
    products = sql_provider.execute_query(query_string)
    return {"suggestions": products}