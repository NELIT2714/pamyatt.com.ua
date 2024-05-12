from web import app, templates, admin_templates, db
from fastapi import Request
from fastapi.responses import RedirectResponse

from web.functions import get_session


@app.get("/admin/slider/")
async def slider_admin(request: Request):
    if not await get_session(request):
        return RedirectResponse("/", status_code=302)

    return admin_templates.TemplateResponse("slider.html", {
        "request": request,
        "slider_images": list(db["slider"].find({}))
    })
