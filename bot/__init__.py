import json
import logging
import pymongo

from aiogram import Dispatcher, Bot

with open("config.json") as config_file:
    config = json.load(config_file)

bot = Bot(token=config["bot"]["token"])
dp = Dispatcher()

db_host, db_port, db_user, db_password, db_database = (config["database"]["host"],
                                                       config["database"]["port"],
                                                       config["database"]["user"],
                                                       config["database"]["password"],
                                                       config["database"]["database"])

client = pymongo.MongoClient(f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/")
db = client[db_database]


async def run_bot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


from bot.commands import getChatId
