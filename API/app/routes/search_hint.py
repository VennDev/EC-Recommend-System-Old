from fastapi import APIRouter
from typing import Union
from app.schemas.error import ErrorResponse
from app.schemas.suggestions import SuggestionsResponse
from app.utils.router_sample import process_simple_recommend_router

router = APIRouter()

@router.get(
    "/search-hint/{key_words}/{num_recommendations}", 
    response_model=Union[SuggestionsResponse, ErrorResponse],
)
async def search_hint_product(key_words: str, num_recommendations: int = 5):
    return process_simple_recommend_router("search_hint", num_recommendations, key_words)