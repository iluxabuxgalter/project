
import aiogram
from aiogram import Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import dotenv
from dotenv import load_dotenv
load_dotenv()

import os

import project.cogs.cogs_database
from project.cogs.cogs_database import load_database, load_database_users_id, load_database_managers_id

async def users_menu(message: Message):
    if message.chat.type == 'private':
        try:
            user_id = str(message.from_user.id)
            database_users_id_list, database_managers_id_list = load_database_users_id(), load_database_managers_id()
            if user_id in database_users_id_list:
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(KeyboardButton('c.s. menu')).add(KeyboardButton('c.s. information')).add(KeyboardButton('c.s. card'))
                if user_id in database_managers_id_list:
                    markup.add(KeyboardButton('manager\'s menu'))
                await message.answer('menu is called up',
                                     reply_markup=markup)
            else:
                await message.answer('to continue - /start')
        except Exception as error:
            print(error)
            ... # add error process

async def users_menu_c_s_menu(message: Message):
    if message.chat.type == 'private':
        try:
            user_id = str(message.from_user.id)
            database = load_database()
            database_managers_id_list = load_database_managers_id()
            with database.cursor() as cursor:
                select = """
                SELECT guide1 FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result = cursor.fetchone()[0]
            if result == 0:
                with database.cursor() as cursor:
                    update = """
                    UPDATE table1 SET guide1 = %s WHERE user_id = %s
                    """
                    update_values = (1, user_id)
                    cursor.execute(update, update_values)
                database.commit()
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('c.s. menu')).add(KeyboardButton('c.s. information')).add(KeyboardButton('c.s. card'))
            if user_id in database_managers_id_list:
                markup.add(KeyboardButton('manager\'s menu'))
            await message.answer(f'<a href="{os.getenv("TELEGRAPH_2")}">c.s. menu</a>',
                                 reply_markup=markup)
            if result == 0:
                await message.answer('c.s. information about location',
                                     reply_markup=markup)
                await message.answer_location(latitude=float(os.getenv('LATITUDE')), longitude=float(os.getenv('LONGITUDE')))
        except Exception as error:
            print(error)
            ... # add error process

async def users_menu_c_s_information(message: Message):
    if message.chat.type == 'private':
        try:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('c.s. information about location')).add(KeyboardButton('back'))
            await message.answer(f'<a href="{os.getenv("TELEGRAPH_3")}">c.s. information</a>',
                                 reply_markup=markup)
        except Exception as error:
            print(error)
            ... # add error process

async def users_menu_c_s_information_about_location(message: Message):
    if message.chat.type == 'private':
        try:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('c.s. information about location')).add(KeyboardButton('back'))
            await message.answer(f'c.s. information about location',
                                 reply_markup=markup)
            await message.answer_location(latitude=float(os.getenv('LATITUDE')), longitude=float(os.getenv('LONGITUDE')))
        except Exception as error:
            print(error)
            ... # add error process

def load_users(bot_dp: Dispatcher):
    bot_dp.register_message_handler(users_menu, text=['back'])
    bot_dp.register_message_handler(users_menu_c_s_menu, text=['c.s. menu'])
    bot_dp.register_message_handler(users_menu_c_s_information, text=['c.s. information'])
    bot_dp.register_message_handler(users_menu_c_s_information_about_location, text=['c.s. information about location'])
