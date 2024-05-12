from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse

from web import app, admin_templates, db
from web.functions import generate_token, hash_password, get_category_childs


@app.post("/admin/auth/")
async def admin_auth(request: Request):
    form = await request.form()

    username = form.get("username")
    password = form.get("password")
    hashed_password = hash_password(password)

    admin = db["users"].find_one({"username": username})

    if admin:
        if hashed_password == admin["password"]:
            response = JSONResponse({"success": True, "redirect_url": "/admin/"})
            generate_token(username, response)
            return response

        return JSONResponse({"success": False, "message": "Неправильний логін або пароль"})

    return JSONResponse({"success": False, "message": "Неправильний логін або пароль"})
