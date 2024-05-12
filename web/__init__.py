import json
import pymongo

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")
templates = Jinja2Templates(directory="web/templates")
admin_templates = Jinja2Templates(directory="web/templates/admin")


with open("config.json") as config_file:
    config = json.load(config_file)

db_host, db_port, db_user, db_password, db_database = (config["database"]["host"],
                                                       config["database"]["port"],
                                                       config["database"]["user"],
                                                       config["database"]["password"],
                                                       config["database"]["database"])

client = pymongo.MongoClient(f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/")
db = client[db_database]

index_info = db["sessions"].index_information()
if not "expireAt_1" in index_info:
    db["sessions"].create_index("expireAt", expireAfterSeconds=86400)

from web.routes import middleware, errors, cart
from web.routes.post import admin_create, add_new_category, slider_controls, social_networks, admin_auth, category_delete, create_product, order_create
from web.routes.get import index, logout, contacts, admin, category, product_details, products, our_works, slider, search
