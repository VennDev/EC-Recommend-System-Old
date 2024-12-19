from fastapi import APIRouter
from typing import Union
from app.schemas.error import ErrorResponse
from app.schemas.suggestions import SuggestionsResponse
from app.utils.router_sample import process_simple_recommend_router
from app.dependencies.auth_depend import auth_dependency
from fastapi import Depends

router = APIRouter()

@router.get(
    "/recommend-like-category/{categoryId}", 
    response_model=Union[SuggestionsResponse, ErrorResponse],
    dependencies=[Depends(auth_dependency)]
)
async def recommend_like_category(categoryId: str):
    return process_simple_recommend_router("recommend_like_category", categoryId)
