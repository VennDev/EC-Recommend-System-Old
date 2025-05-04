import asyncio
from fastapi import APIRouter
from typing import Union
from utils import Config
from fastapi import Depends
from concurrent.futures import ProcessPoolExecutor
from app.schemas.error import ErrorResponse
from app.schemas.suggestions import SuggestionsResponse
from app.dependencies.auth_dependency import auth_dependency
from ai.models.svd import SVDModel

router = APIRouter()
executor = ProcessPoolExecutor()


@router.get(
    "/recommend-ai/{type_model}/{name_model}/{needed}/{num_recommendations}",
    response_model=Union[SuggestionsResponse, ErrorResponse],
    dependencies=[Depends(auth_dependency)],
)
async def recommend_ai(
    type_model: str, name_model: str, needed: str, num_recommendations: int = 5
):
    config_data_model = Config("ai_config.yml").get_nested_value(
        f"system.recommend_ai.{type_model}.{name_model}"
    )
    if config_data_model is None:
        return {"error": "Không tìm thấy mô hình AI"}

    model = SVDModel(name_model, config_data_model)

    async def run_model_recommend():
        return await model.recommend(needed, num_recommendations)

    result = await asyncio.to_thread(asyncio.run, run_model_recommend())

    return {"suggestions": result}

