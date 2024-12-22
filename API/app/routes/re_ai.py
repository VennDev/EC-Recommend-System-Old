from fastapi import APIRouter
from typing import Union
from utils import Config
from app.schemas.error import ErrorResponse
from app.schemas.suggestions import SuggestionsResponse
from ai.models.svd import SVDModel

router = APIRouter()

@router.get(
    "/recommend-ai/{type_model}/{name_model}/{needed}/{num_recommendations}", 
    response_model=Union[SuggestionsResponse, ErrorResponse],
)
async def recommend_ai(type_model: str, name_model: str, needed: str, num_recommendations: int = 5):
    config_data_model = Config("ai_config.yml").get_nested_value(f"system.recommend_ai.{type_model}.{name_model}")
    if config_data_model == None:
        return {"error": "Không tìm thấy mô hình AI"}
    model = SVDModel(name_model, config_data_model)
    result = await model.recommend(needed, num_recommendations)
    return {"suggestions": result}