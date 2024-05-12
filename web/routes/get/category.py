import json
import math
from typing import List

from fastapi import Query

from web import app, templates, db
from fastapi import Request, Depends
from bson import ObjectId

from web.functions import get_category_childs, get_social_links, get_cart_products_amount, get_session


@app.get("/category/{category_url}/")
async def category_page(request: Request, category_url: str, page: int = Query(1, gt=0)):
    category = db["categories"].find_one({"url": category_url})

    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    if category:
        sub_categories = list(db["sub_categories"].find({"parent_id": category["_id"]}))

        if not sub_categories:
            per_page = 21
            offset = (page - 1) * per_page

            products = list(db["products"].find({"category_id": category["_id"]}).skip(offset).limit(per_page))

            total_products = db["products"].count_documents({"category_id": category["_id"]})
            total_pages = math.ceil(total_products / per_page)

            return templates.TemplateResponse("products.html", {
                "request": request,
                "category": category,
                "categories": categories,
                "products": products,
                "categories1": categories1,
                "categories2": categories2,
                "cart_len": get_cart_products_amount(request),
                "current_page": page,
                "total_pages": total_pages,
                "session": await get_session(request)
            })
        else:
            return templates.TemplateResponse("category.html", {
                "request": request,
                "category": category,
                "categories": categories,
                "sub_categories": sub_categories,
                "categories1": categories1,
                "categories2": categories2,
                "cart_len": get_cart_products_amount(request)
            })


@app.get("/category/{category_url}/{sub_category_url}/")
async def sub_category_page(request: Request, category_url: str, sub_category_url: str, page: int = Query(1, gt=0)):
    category = db["categories"].find_one({"url": category_url})
    sub_category = db["sub_categories"].find_one({"url": sub_category_url})

    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    if category and sub_category:
        if sub_category["parent_id"] == category["_id"]:
            per_page = 21
            offset = (page - 1) * per_page

            products = list(db["products"].find({"category_id": sub_category["_id"]}).skip(offset).limit(per_page))

            total_products = db["products"].count_documents({"category_id": sub_category["_id"]})
            total_pages = math.ceil(total_products / per_page)

            return templates.TemplateResponse("products.html", {
                "request": request,
                "category": category,
                "products": products,
                "sub_category": sub_category,
                "categories": get_category_childs(),
                "cart_len": get_cart_products_amount(request),
                "current_page": page,
                "total_pages": total_pages,
                "categories1": categories1,
                "categories2": categories2,
                "session": await get_session(request)
            })
    else:
        return "Категорія відсутня!"
