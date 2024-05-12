import uuid

from fastapi import Request
from starlette.responses import RedirectResponse

from web import app, db, admin_templates
from web.functions import download_file, get_category_childs
from bson import ObjectId

from transliterate import translit, get_available_language_codes


@app.post("/admin/category/add/")
async def add_new_category(request: Request):
    form = await request.form()

    category_name = form.get("category_name")
    category_image = form.get("category_image")
    sub_category_check = form.get("sub_category_check")

    if category_name and category_image:
        if sub_category_check:
            category_id = form.get("sub_category")
            parent_category = db["categories"].find_one({"_id": ObjectId(category_id)})

            if parent_category:
                if category_image:
                    filename = await download_file(category_image, ["png", "jpeg", "jpg", "svg", "webp"])

                    if filename["success"]:
                        db["sub_categories"].insert_one({
                            "name": category_name,
                            "image": filename["file_name"],
                            "url": translit(category_name.lower().replace(" ", "-"), "ru", reversed=True),
                            "parent_id": ObjectId(parent_category["_id"])
                        })

                        return RedirectResponse("/admin/", status_code=302)
                    else:
                        return {"success": False, "message": filename["message"]}
        else:
            if category_image:
                filename = await download_file(category_image, ["png", "jpeg", "jpg", "svg", "webp"])

                if filename["success"]:
                    db["categories"].insert_one({
                        "name": category_name,
                        "image": filename["file_name"],
                        "url": translit(category_name.lower().replace(" ", "-"), "ru", reversed=True)
                    })

                    return RedirectResponse("/admin/", status_code=302)
                else:
                    return {"success": False, "message": filename["message"]}
            else:
                return {"success": False, "message": "Картинка категории не выбрана"}

    else:
        return {"success": False, "message": "хїуй"}
