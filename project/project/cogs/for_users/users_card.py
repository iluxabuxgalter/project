
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import dotenv
from dotenv import load_dotenv
load_dotenv()

import os

import time

import random

import PIL
from PIL import Image, ImageDraw, ImageFont

import project.cogs.cogs_database
from project.cogs.cogs_database import load_database, load_database_users_id

async def users_c_s_card(message: Message):
    if message.chat.type == 'private':
        try:
            user_id = str(message.from_user.id)
            database = load_database()
            with database.cursor() as cursor:
                select = """
                SELECT guide2 FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result = cursor.fetchone()[0]
            if result == 0:
                with database.cursor() as cursor:
                    update = """
                    UPDATE table1 SET guide2 = %s WHERE user_id = %s
                    """
                    update_values = (1, user_id)
                    cursor.execute(update, update_values)
                database.commit()
            with database.cursor() as cursor:
                select = """
                SELECT status FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_status = cursor.fetchone()[0]
            with database.cursor() as cursor:
                select = """
                SELECT points FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_status_points = cursor.fetchone()[0]
            image = Image.open('project/cogs/project_cogs/image.png')
            image_draw = ImageDraw.Draw(image)
            image_draw.text((350, -10), str(time.strftime('%d.%m.%Y %H:%M')), fill=(0, 0, 0), font=ImageFont.truetype('project/cogs/project_cogs/image_font.ttf', 70))
            image_draw.text((350, 270), user_id, fill=(0, 0, 0), font=ImageFont.truetype('project/cogs/project_cogs/image_font.ttf', 70))
            image_draw.text((105, 160), result_status, fill=(0, 0, 0), font=ImageFont.truetype('project/cogs/project_cogs/image_font.ttf', 70))
            image_draw.text((450, 160), result_status_points, fill=(0, 0, 0), font=ImageFont.truetype('project/cogs/project_cogs/image_font.ttf', 70))
            image.save(f'project/cogs/for_users/cogs/cache/{user_id}.png', quality = 95), image.close()
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('c.s. card giveaway')).add(KeyboardButton('back'))
            await message.answer(f'c.s. card (you\'re link for invite - <code>https:/t.me/projectv1alphabot?start={user_id}</code>)',
                                 reply_markup=markup)
            with open(f'project/cogs/for_users/cogs/cache/{user_id}.png', 'rb') as file:
                await message.answer_photo(file)
            if result == 0:
                await message.answer(f'<a href="{os.getenv("TELEGRAPH_4")}">c.s. card and c.s. card giveaway</a>')
            os.remove(f'project/cogs/for_users/cogs/cache/{user_id}.png')
        except Exception as error:
            print(error)
            ... # add error process

def load_database_users_giveaway_id():
    try:
        database = load_database()
        with database.cursor() as cursor:
            select = """
            SELECT user_id FROM table2
            """
            cursor.execute(select)
        database_users_giveaway_id_list = [row[0] for row in cursor.fetchall()]
        return database_users_giveaway_id_list
    except Exception as error:
        print(error)
        ... # add error process

async def users_c_s_card_giveaway(message: Message):
    if message.chat.type == 'private':
        try:
            user_id = str(message.from_user.id)
            database = load_database()
            database_users_giveaway_id_list = load_database_users_giveaway_id()
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('c.s. card giveaway')).add(KeyboardButton('back'))
            if user_id in database_users_giveaway_id_list:
                await message.answer('c.s. card giveaway you\'re already there',
                                     reply_markup=markup)
            else:
                with database.cursor() as cursor:
                    insert = """
                    INSERT IGNORE INTO table2 (user_id) VALUES (%s)
                    """
                    insert_values = (user_id)
                    cursor.execute(insert, insert_values)
                database.commit()
                await message.answer('c.s. card giveaway you\'re there')
        except Exception as error:
            print(error)
            ... # add error process

async def users_c_s_card_giveaway_(bot: Bot):
    try:
        database = load_database()
        database_users_id_list = load_database_users_id()
        with database.cursor() as cursor:
            select = """
            SELECT COUNT(*) FROM table2
            """
            cursor.execute(select)
        for user_id in database_users_id_list:
            await bot.send_message(user_id, text='you\'re already in giveaway?')
    except Exception as error:
        print(error)
        ... # add error process

async def users_c_s_card_giveaway_result(bot: Bot):
    try:
        database = load_database()
        database_users_giveaway_id_list = load_database_users_giveaway_id()
        user_id_win = random.choice(database_users_giveaway_id_list)
        with database.cursor() as cursor:
            select = """
            SELECT points FROM table1 WHERE user_id = %s
            """
            select_values = (user_id_win)
            cursor.execute(select, select_values)
        result = int(cursor.fetchone()[0])
        with database.cursor() as cursor:
            update = """
            UPDATE table1 SET points = %s WHERE user_id = %s
            """
            update_values = (str(result + 500), user_id_win)
            cursor.execute(update, update_values)
        database.commit()
        with database.cursor() as cursor:
            truncate = """
            TRUNCATE TABLE table2
            """
            cursor.execute(truncate)
        database.commit()
        for user_id in database_users_giveaway_id_list:
            if user_id == user_id_win:
                await bot.send_message(user_id, text='you\'re won in giveaway (+500 points)')
            else:
                await bot.send_message(user_id, text='you\'re didn\'t won in giveaway')
    except Exception as error:
        print(error)
        ... # add error process

def load_users_users_card(bot_dp: Dispatcher):
    bot_dp.register_message_handler(users_c_s_card, text=['c.s. card'])
    bot_dp.register_message_handler(users_c_s_card_giveaway, text=['c.s. card giveaway'])
