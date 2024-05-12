from typing import List

from web import app, templates, db, config
from fastapi import Request, Depends

from web.functions import get_social_links, get_cart_products_amount, get_category_childs


@app.get("/")
async def root(request: Request, social_links: List[dict] = Depends(get_social_links)):
    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "categories": list(db["categories"].find({})),
        "categories1": categories1,
        "categories2": categories2,
        "slider_images": list(db["slider"].find({}).limit(int(config["web"]["slider"]["limit"]))),
        "social_links": social_links,
        "cart_len": get_cart_products_amount(request)
    })
