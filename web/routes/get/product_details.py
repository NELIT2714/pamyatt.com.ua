from typing import List

from web import app, templates, db
from fastapi import Request, Depends
from bson import ObjectId

from web.functions import get_category_childs, get_social_links, get_cart_products_amount


@app.get("/category/{category_url}/product/{product_url}")
async def product_page(request: Request, category_url: str, product_url: str, social_links: List[dict] = Depends(get_social_links)):
    category = db["categories"].find_one({"url": category_url})
    product = db["products"].find_one({"url": product_url})

    if category and product:
        return templates.TemplateResponse("product_details.html", {
            "request": request,
            "category": category,
            "product": product,
            "social_links": social_links,
            "categories": list(db["categories"].find({})),
            "cart_len": get_cart_products_amount(request)
        })


@app.get("/category/{category_url}/{sub_category_url}/product/{product_url}")
def product_page_sub(request: Request, category_url: str, sub_category_url: str, product_url: str, social_links: List[dict] = Depends(get_social_links)):
    category = db["categories"].find_one({"url": category_url})
    sub_category = db["sub_categories"].find_one({"url": sub_category_url})
    product = db["products"].find_one({"url": product_url})

    if category and product and sub_category:
        return templates.TemplateResponse("product_details.html", {
            "request": request,
            "category": category,
            "sub_category": sub_category,
            "product": db["products"].find_one({"_id": product["_id"]}),
            "social_links": social_links,
            "categories": list(db["categories"].find({})),
            "cart_len": get_cart_products_amount(request)
        })


@app.get("/product/{product_id}/")
def product_page_id(request: Request, product_id: str, social_links: List[dict] = Depends(get_social_links)):
    product = db["products"].find_one({"_id": ObjectId(product_id)})

    product_changed = {
        "_id": product["_id"],
        "name": product["name"],
        "description": product["description"].replace("\n", "<br>"),
        "image": product["image"],
        "price": product["price"],
        "url": product["url"],
        "category_id": product["category_id"],
        "options": product["options"]
    }

    print(product["description"])

    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    if product:
        return templates.TemplateResponse("product_details.html", {
            "request": request,
            "product": product_changed,
            "social_links": social_links,
            "categories": list(db["categories"].find({})),
            "cart_len": get_cart_products_amount(request),
            "categories1": categories1,
            "categories2": categories2
        })
