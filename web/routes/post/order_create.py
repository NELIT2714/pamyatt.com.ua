import json

from bson import ObjectId
from fastapi import Request
from starlette.responses import RedirectResponse
from transliterate import translit

from bot import bot
from web import app, db
from web.functions import download_file


@app.post("/order/create/")
async def order_create(request: Request):
    form_data = await request.form()

    with open("config.json", encoding="utf-8") as config_file:
        config = json.load(config_file)

    cart = request.cookies.get("cart")
    cart_json = json.loads(cart)

    if cart_json:
        cart_str = ""
        cart_price = 0
        for item in cart_json:
            item_in_db = db["products"].find_one({"_id": ObjectId(item["id"])})
            product_url = f"{request.base_url}product/{item_in_db['_id']}"

            if item.get("selected_option", False):
                option = item_in_db["options"][item["selected_option"]]
                cart_str += f"Назва: {item_in_db['name']} ({item_in_db['_id']})\nКількість: {item['amount']}\nЦіна: {str(int(item_in_db['options'][item['selected_option']]['option_price']) * int(item['amount']))}\nВаріант: {option['option_name']}\nUrl: {product_url}\n\n"
                cart_price += item_in_db['options'][item['selected_option']]['option_price'] * item['amount']
            else:
                cart_str += f"Назва: {item_in_db['name']} ({item_in_db['_id']})\nКількість: {item['amount']}\nЦіна: {str(int(item_in_db['price']) * int(item['amount']))}\nUrl: {product_url}\n\n"
                cart_price += item_in_db['price'] * item['amount']

        await bot.send_message(
            chat_id=config["bot"]["chat_id"],
            text=f"Ім'я: {form_data['first_name']}\nПрізвище: {form_data['last_name']}\nEmail: {form_data['email']}\nТелефон: {form_data['tel']}\n\nКошик: {cart_str}\n\nЗагальна сума кошика: {cart_price} UAH"
        )

    return RedirectResponse("/", status_code=302)
