from fastapi import APIRouter
from app.schemas.suggestions import SuggestionsResponse
from app.services.search_hint_service import get_products, hint_search

router = APIRouter()

@router.get("/search-product/{key_words}", response_model=SuggestionsResponse)
async def search_product(key_words: str):
    products = get_products()
    flattened = [value for row in products for value in row.values()]
    suggestions = hint_search(key_words, flattened)
    return {"suggestions": suggestions}
