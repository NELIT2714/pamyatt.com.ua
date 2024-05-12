from bson import ObjectId
from fastapi import Request
from starlette.responses import RedirectResponse
from transliterate import translit

from web import app, db
from web.functions import download_file


@app.post("/admin/slider/add-image")
async def slider_controls(request: Request):
    form = await request.form()

    slider_image = form.get("slider_image")

    if slider_image:
        filename = await download_file(slider_image, ["png", "jpeg", "jpg", "svg", "webp"])

        if filename["success"]:
            db["slider"].insert_one({
                "image": filename["file_name"]
            })

            return RedirectResponse("/admin/slider/", status_code=302)


@app.post("/admin/slider/delete")
async def slider_admin_delete(request: Request):
    form = await request.form()

    slider_id = form.get("slider_id")

    if slider_id:
        db["slider"].delete_one({"_id": ObjectId(slider_id)})
        return RedirectResponse("/admin/slider/", status_code=302)
