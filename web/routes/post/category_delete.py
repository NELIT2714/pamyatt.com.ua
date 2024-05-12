import json

from bson import ObjectId
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse

from web import app, db
from web.functions import hash_password, generate_token


@app.post("/admin/category/delete/")
async def sub_category_delete(request: Request):
    if request.method == "POST":
        form = await request.form()

        category_id = form.get("category_id")

        if category_id:
            db["categories"].delete_one({"_id": ObjectId(category_id)})

        return RedirectResponse("/admin/", status_code=302)


@app.post("/admin/sub-category/delete/")
async def sub_category_delete(request: Request):
    if request.method == "POST":
        form = await request.form()

        sub_category_id = form.get("sub_category_id")

        if sub_category_id:
            db["sub_categories"].delete_one({"_id": ObjectId(sub_category_id)})

        return RedirectResponse("/admin/", status_code=302)
