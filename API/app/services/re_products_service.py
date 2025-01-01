from typing import List
from rapidfuzz import process

def recommend_products_simple(
    name: str, 
    index_selected: List[str], 
    product_list: List[dict], 
    limit: int = 5
) -> List[dict]:
    products_target = [
        " ".join(str(product[key]) for key in index_selected if key in product) 
        for product in product_list
    ]
    matches = process.extract(name, products_target, limit=limit)
    recommendations = [
        product_list[products_target.index(match[0])] for match in matches
    ]
    return recommendations