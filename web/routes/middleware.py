from fastapi import Request

from web import app, db, admin_templates
from web.functions import get_social_links


@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.url.path.startswith("/assets"):
        return await call_next(request)

    if request.method == "GET":
        admins_count = db["users"].count_documents({"admin": True})
        if admins_count == 0:
            return admin_templates.TemplateResponse("website_configuration.html", {"request": request, "url_for": app.url_path_for})

    response = await call_next(request)
    return response
