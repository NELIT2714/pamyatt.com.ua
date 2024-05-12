from typing import List

from bson import ObjectId
from fastapi import Request, Depends
from starlette.responses import RedirectResponse

from web import app, admin_templates, db
from web.functions import get_social_links, get_session


@app.get("/admin/products/")
async def products(request: Request, social_links: List[dict] = Depends(get_social_links)):
    if not await get_session(request):
        return RedirectResponse("/", status_code=302)

    categories = list(db["categories"].aggregate([
        {
            "$lookup": {
                "from": "sub_categories",
                "localField": "_id",
                "foreignField": "parent_id",
                "as": "sub_categories"
            }
        },
        {
            "$match": {
                "sub_categories": []
            }
        },
        {
            "$addFields": {
                "type": "category"
            }
        }
    ]))

    sub_categories = list(db["sub_categories"].find({}))

    return admin_templates.TemplateResponse("products.html", {
        "request": request,
        "social_links": social_links,
        "categories_for_products": categories + sub_categories,
        "products": list(db["products"].find({}).sort([("_id", -1)]))
    })


@app.get("/product/edit/{product_id}")
async def product_edit_get(request: Request, product_id: str):
    if not await get_session(request):
        return RedirectResponse("/", status_code=302)

    return admin_templates.TemplateResponse("edit_product.html", {
        "request": request,
        "product": db["products"].find_one({"_id": ObjectId(product_id)})
    })


@app.post("/product/edit/")
async def product_edit_post(request: Request):
    form_data = await request.form()

    product_id = form_data.get("product_id")
    product_name = form_data.get("product_name")
    product_description = form_data.get("product_description")
    product_price = form_data.get("product_price")
    product_options = form_data.getlist("product_option[]")

    options = []
    option_index = 0
    while True:
        option_name = form_data.get(f"option_name_{option_index}")
        option_price = form_data.get(f"option_price_{option_index}")
        if option_name is None or option_price is None:
            break
        options.append({
            "option_name": option_name,
            "option_price": int(option_price)
        })
        option_index += 1

    for option in product_options:
        option_name = option.split("-")[0]
        option_price = option.split("-")[1]
        options.append({
            "option_name": option_name,
            "option_price": int(option_price)
        })

    db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {
            "name": product_name,
            "description": product_description,
            "price": product_price,
            "options": options
        }}
    )

    return RedirectResponse("/admin/products/", status_code=302)


@app.get("/product/delete/{product_id}")
async def product_edit_post(request: Request, product_id: str):
    if not await get_session(request):
        return RedirectResponse("/", status_code=302)

    if "session_token" in request.cookies:
        db["products"].delete_one({"_id": ObjectId(product_id)})
        return RedirectResponse("/admin/products/", status_code=302)
