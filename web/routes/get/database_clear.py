from fastapi import Request

from web import app, db


@app.get("/db")
async def database_clear():
    for coll in db.list_collection_names():
        db.drop_collection(coll)
        db.create_collection(coll)

    return "Бд очищена"