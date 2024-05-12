import json

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse

from web import app, db
from web.functions import hash_password, generate_token


@app.post("/admin/create-admin/")
async def admin_create(request: Request):
    if request.method == "POST":
        form = await request.form()

        username = form.get("username")
        password = form.get("password")
        repeated_password = form.get("repeat-password")

        if not username and password and repeated_password:
            return JSONResponse({"success": False, "message": "Не всі поля форми були заповнені"})

        if not repeated_password == password:
            return JSONResponse({"success": False, "message": "Повторений пароль введено невірно"})

        db["users"].insert_one({
            "username": username,
            "password": hash_password(password),
            "admin": True
        })

        response = JSONResponse({"success": True, "redirect_url": "/admin/"})
        generate_token(username, response)
        return response
