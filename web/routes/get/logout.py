from fastapi import Request
from fastapi.responses import RedirectResponse

from web import app, db


@app.get("/logout")
async def logout(request: Request):
    session_token = request.cookies.get("session_token")
    db["sessions"].delete_one({"token": session_token})

    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session_token")

    return response
