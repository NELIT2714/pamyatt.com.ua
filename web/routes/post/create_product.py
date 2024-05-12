import json
from typing import List

from bson import ObjectId
from fastapi import Request, UploadFile
from fastapi.params import File, Form
from starlette.responses import JSONResponse
from transliterate import translit

from web import app, db
from web.functions import download_file


@app.post("/admin/products/new/")
async def create_product(request: Request):

    form_data = await request.form()

    product_name = form_data.get("product_name")
    product_description = form_data.get("product_description")
    product_price = form_data.get("product_price")
    product_category = form_data.get("product_category")
    product_main_image = form_data.get("product_main_image")
    product_additional_images = form_data.getlist("product_additional_images")

    product_options_json = form_data.get("product_options")
    product_options = json.loads(product_options_json)

    if product_name and product_price and product_category and product_main_image and product_description:
        main_image = await download_file(product_main_image, ["png", "jpeg", "jpg", "svg", "webp"])

        if main_image["success"]:

            additional_images = []
            product_options_arr = []

            if product_additional_images:
                for file in product_additional_images:
                    result = await download_file(file, ["png", "jpeg", "jpg", "svg", "webp"])
                    if result["success"]:
                        additional_images.append(result["file_name"])

            if product_options:
                for option in product_options:
                    option_name = option.split("-")[0]
                    option_price = option.split("-")[1]
                    product_options_arr.append({"option_name": option_name, "option_price": int(option_price)})

            db["products"].insert_one({
                "name": product_name,
                "description": product_description,
                "image": main_image["file_name"],
                "price": int(product_price),
                "url": translit(product_name, "ru", reversed=True).replace(" ", ","),
                "category_id": ObjectId(product_category),
                "additional_images": additional_images,
                "options": product_options_arr
            })

            return JSONResponse({"success": True, "redirect_url": "/admin/products/"})

        return JSONResponse({"success": False, "message": "Щось пішло не так :{"})

    return JSONResponse({"success": False, "message": "Не всі поля форми було заповнено"})

