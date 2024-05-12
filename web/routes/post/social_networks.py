from fastapi import Request

from web import app, db


@app.post("/admin/change/social-networks/")
async def social_networks(request: Request):
    form = await request.form()

    instagram_url = form.get("instagram")
    telegram_url = form.get("telegram")
    facebook_url = form.get("facebook")
    tiktok_url = form.get("tiktok")

    if instagram_url and telegram_url and facebook_url and tiktok_url:
        social_networks_urls = {
            "instagram": instagram_url,
            "telegram": telegram_url,
            "facebook": facebook_url,
            "tiktok": tiktok_url
        }

        for key, value in social_networks_urls.items():
            if db["social_networks"].find_one({"type": key}) is None:
                db["social_networks"].insert_one({
                    "type": key,
                    "url": value
                })
            else:
                db["social_networks"].update_one(
                    {"type": key},
                    {"$set": {"url": value}}
                )

        return {"success": True, "message": "Ссылки на соц.сети обновлены"}
