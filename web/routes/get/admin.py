from fastapi import Request

from web import app, admin_templates, db
from web.functions import get_category_childs


@app.get("/admin/")
async def admin(request: Request):
    session_token = request.cookies.get("session_token")

    if session_token:
        user_session_token = db["sessions"].find_one({"token": session_token})

        if user_session_token:
            user_token = db["users"].find_one({"username": user_session_token["username"]})

            if not user_token:
                response = admin_templates.TemplateResponse("admin_login.html", {"request": request})
                response.delete_cookie("session_token")
                db["users"].delete_one(user_session_token)

                return response

            return admin_templates.TemplateResponse("admin_index.html", {
                "request": request,
                "categories": list(db["categories"].find({})),
                "sub_categories": list(db["sub_categories"].find()),
                "categories_childs": get_category_childs(),
                "slider_images": list(db["slider"].find({}))
            })
        else:
            response = admin_templates.TemplateResponse("admin_login.html", {"request": request})
            response.delete_cookie("session_token")
            return response
    else:
        return admin_templates.TemplateResponse("admin_login.html", {"request": request})



