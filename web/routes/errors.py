from typing import List

from fastapi import Request, Depends
from starlette.exceptions import HTTPException as StarletteHTTPException

from web import templates, app, db
from web.functions import get_social_links, get_cart_products_amount


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException, social_links: List[dict] = Depends(get_social_links)):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "social_links": social_links,
            "categories": list(db["categories"].find({})),
            "cart_len": get_cart_products_amount(request)
        }, status_code=404)
