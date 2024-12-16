from fastapi import APIRouter, Depends
from app.schemas.recommendations import RecommendationResponse
from app.services.re_products_service import recommend_products
from app.dependencies.auth_depend import auth_dependency
from .search_hint import get_products

router = APIRouter()


@router.get(
    "/re-products/{name}",
    response_model=RecommendationResponse,
    dependencies=[Depends(auth_dependency)],
)
async def get_recommended_products(name: str):
    """
    API gợi ý sản phẩm dựa theo tên nhập vào.
    """
    # sql_provider = SQLProvider()
    PRODUCTS = get_products()
    recommendations = recommend_products(name, PRODUCTS, limit=20)
    return {"recommendations": recommendations}
