import json
import secrets
import hashlib
import uuid
from datetime import datetime, timedelta

from web import db


def generate_token(username, resp):
    token = secrets.token_urlsafe(100)
    expire_at = datetime.utcnow() + timedelta(hours=24)
    db["sessions"].insert_one({"token": token, "username": username, "expireAt": expire_at})
    resp.set_cookie(key="session_token", value=token)


def hash_password(user_password):
    with open("config.json") as config_file:
        config = json.load(config_file)

    password = str(user_password)
    password = password + config["web"]["password-salt"]
    password_bytes = password.encode("utf-8")
    hashed_password = hashlib.sha256(password_bytes).hexdigest()

    return str(hashed_password)


async def download_file(file, allowed_extensions):
    file_name = str(uuid.uuid4().hex)
    file_extension = file.filename.split(".")[-1]

    if file_extension in allowed_extensions:
        with open(f"web/assets/users_uploads/{file_name}.{file_extension}", "wb") as opened_file:
            opened_file.write(await file.read())

        return {"success": True, "file_name": f"{file_name}.{file_extension}"}
    else:
        return {"success": False, "message": "Неверное расширение файла"}


def get_category_childs():
    categories = db["categories"].find({})

    result = []
    for category in categories:
        category_obj = {
            "_id": category["_id"],
            "name": category["name"],
            "image": category["image"],
            "url": category["url"]
        }
        sub_categories = db["sub_categories"].find({"parent_id": category["_id"]})
        category_obj["childs"] = list(sub_categories)
        result.append(category_obj)

    return result


def get_social_links():
    social_links_db = list(db["social_networks"].find({}))
    social_links_dict = {}

    if social_links_db:
        for link in social_links_db:
            social_links_dict[link["type"]] = link["url"]

    return social_links_dict


def get_cart_products_amount(request):
    cart = request.cookies.get("cart")

    if not cart:
        cart_str = []
    else:
        cart_str = json.loads(cart)

    cart_len = 0
    for item in cart_str:
        cart_len += item["amount"]

    return cart_len


async def get_session(request):
    auth_token = request.cookies.get("session_token")
    if auth_token:
        session = db["sessions"].find_one({"token": auth_token})
        if session:
            return True
    return False

