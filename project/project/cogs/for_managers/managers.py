
import aiogram
from aiogram import Dispatcher, types
from aiogram.types import Message

import project.cogs.cogs_database
from project.cogs.cogs_database import load_database_managers_id

async def managers_menu(message: Message):
    try:
        user_id = str(message.from_user.id)
        database_managers_id_list = load_database_managers_id()
        if user_id in database_managers_id_list:
            ...
    except Exception as error:
        print(error)
        ... # add error process

def load_managers(bot_dp: Dispatcher):
    bot_dp.register_message_handler(managers_menu, commands=['m_menu'])
