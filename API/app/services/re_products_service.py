from typing import List
from rapidfuzz import process

def recommend_products(name: str, product_list: List[dict], limit: int = 5) -> List[dict]:
    """
    Hàm gợi ý sản phẩm dựa trên tên.
    """
    product_names = [product["title"] for product in product_list]
    matches = process.extract(name, product_names, limit=limit)
    recommendations = [
        product_list[product_names.index(match[0])] for match in matches
    ]
    return recommendations