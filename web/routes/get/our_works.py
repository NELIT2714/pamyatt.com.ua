import math

from web import app, templates, db
from fastapi import Request, Query

from web.functions import get_cart_products_amount, get_category_childs


@app.get("/our-works/")
async def our_works_page(request: Request, page: int = Query(1, gt=0)):
    per_page = 21
    offset = (page - 1) * per_page

    works = list(db["slider"].find({}).skip(offset).limit(per_page))

    total_works = db["slider"].count_documents({})
    total_pages = math.ceil(total_works / per_page)

    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    return templates.TemplateResponse("our_works.html", {
        "request": request,
        "works": works,
        "categories": list(db["categories"].find({})),
        "cart_len": get_cart_products_amount(request),
        "total_pages": total_pages,
        "current_page": page,
        "categories1": categories1,
        "categories2": categories2
    })
