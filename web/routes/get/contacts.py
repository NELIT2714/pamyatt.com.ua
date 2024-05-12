from web import app, templates, db
from fastapi import Request

from web.functions import get_cart_products_amount, get_category_childs


@app.get("/contacts/")
async def contacts_page(request: Request):
    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    return templates.TemplateResponse("contacts.html", {
        "request": request,
        "categories1": categories1,
        "categories2": categories2,
        "cart_len": get_cart_products_amount(request)
    })
