import json
from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import Request
from fastapi.responses import RedirectResponse
from pymongo import database
from starlette.responses import JSONResponse

from web import app, admin_templates, db, templates
from web.functions import generate_token, hash_password, get_category_childs, get_cart_products_amount


@app.get("/cart/")
async def cart_page(request: Request):
    if not request.cookies.get("cart"):
        cart_str = []
    else:
        cart = request.cookies.get("cart")
        cart_str = json.loads(cart)

    cart = []
    for item in cart_str:
        product = db["products"].find_one({"_id": ObjectId(item["id"])})
        if product:
            product["selected_option"] = item["selected_option"]
            product["amount"] = item["amount"]
            cart.append(product)

    cart_price = 0
    for item in cart:
        if not item["options"] == []:
            cart_price += int(item["options"][item["selected_option"]]["option_price"]) * int(item["amount"])
        else:
            cart_price += int(item["price"]) * int(item["amount"])

    categories = get_category_childs()

    half_length = len(categories) // 2
    categories1 = categories[:half_length]
    categories2 = categories[half_length:]

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart": cart,
        "cart_price": cart_price,
        "categories": list(db["categories"].find({})),
        "cart_len": get_cart_products_amount(request),
        "categories1": categories1,
        "categories2": categories2
    })


@app.post("/cart/add/")
async def add_product_to_cart(request: Request):
    form_data = await request.form()

    product_id = form_data.get("product_id")
    option = form_data.get("selected-option")
    amount_index = form_data.get("amount_index")

    if not option:
        option = 0

    cart_data = json.loads(request.cookies.get("cart", "[]"))

    product = db["products"].find_one({"_id": ObjectId(product_id)})

    if product:
        product_id_str = str(product["_id"])
        option_id = int(option)

        already_in_cart = False
        for item in cart_data:
            if item["id"] == product_id_str and item["selected_option"] == option_id:
                item["amount"] += int(amount_index)
                already_in_cart = True
                break

        if not already_in_cart:
            product_in_cart = {
                "id": product_id_str,
                "amount": int(amount_index),
                "selected_option": option_id
            }
            cart_data.append(product_in_cart)

        current_datetime = datetime.now(timezone.utc)
        expires_datetime = current_datetime + timedelta(days=365)

        response = RedirectResponse(url="/cart/", status_code=302)
        response.set_cookie("cart", value=json.dumps(cart_data), expires=expires_datetime)

        return response


@app.get("/cart/delete/{product_id}")
async def delete_product_from_cart(request: Request, product_id: str):
    cart = request.cookies.get("cart")
    cart_str = json.loads(cart)

    updated_cart = []

    for item in cart_str:
        if item.get("id") == product_id:
            continue
        updated_cart.append(item)

    current_datetime = datetime.now(timezone.utc)
    expires_datetime = current_datetime + timedelta(days=365)

    response = RedirectResponse(url="/cart/", status_code=302)
    response.set_cookie("cart", value=json.dumps(updated_cart), expires=expires_datetime)
    return response


@app.post("/cart/change-amount/")
async def change_amount_cart(request: Request):
    form_data = await request.form()

    product_id = form_data.get("product_id")
    amount_index = int(form_data.get("amount"))
    action = form_data.get("action")

    cart_data = json.loads(request.cookies.get("cart"))

    for item in cart_data:
        if item["id"] == product_id:
            if action == "subtract":
                item["amount"] = max(item["amount"] - 1, 1)
            elif action == "add":
                item["amount"] = min(item["amount"] + 1, 20)
            break

    current_datetime = datetime.now(timezone.utc)
    expires_datetime = current_datetime + timedelta(days=365)

    response = JSONResponse({"success": True, "redirect_url": "/cart/"})
    response.set_cookie("cart", value=json.dumps(cart_data), expires=expires_datetime)
    return response
