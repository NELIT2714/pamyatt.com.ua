from typing import List

from web import app, templates, db
from fastapi import Request, Depends
from bson import ObjectId

from web.functions import get_category_childs, get_social_links, get_cart_products_amount


@app.get("/search")
async def search_products(request: Request, search_text: str):
    search_result = list(db["products"].find(
        {"name": {"$regex": search_text, "$options": 'i'}}
    ))

    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    return templates.TemplateResponse("products.html", {
        "request": request,
        "search_result": search_result,
        "categories": get_category_childs(),
        "products": search_result,
        "cart_len": get_cart_products_amount(request),
        "categories1": categories1,
        "categories2": categories2,
        "total_pages": 0
    })
