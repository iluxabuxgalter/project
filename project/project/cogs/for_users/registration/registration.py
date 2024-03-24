
import aiogram
from aiogram import Dispatcher, types, dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State

import dotenv
from dotenv import load_dotenv
load_dotenv()

import os

import json

import time

import project.cogs.cogs_database
from project.cogs.cogs_database import load_database, load_database_users_id, load_database_managers_id

class RegistrationProcess(StatesGroup):
    registration_phone_number = State()

async def start(message: Message, state: FSMContext):
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
                with open('project/cogs/for_users/registration/registration_cogs/registration_list.json', 'r+') as file:
                    registration_list = json.load(file)
                registration_list[user_id] = {}
                registration_list[user_id]['registration_inviter_id'] = None
                if message.text[7:] != '':
                    registration_list[user_id]['registration_inviter_id'] = message.text[7:]
                registration_list[user_id]['registration_date'] = str(time.strftime('%d.%m.%Y'))
                registration_list[user_id]['registration_phone_number'] = None
                registration_list[user_id]['registration_points'] = '250'
                with open('project/cogs/for_users/registration/registration_cogs/registration_list.json', 'w') as file:
                    json.dump(registration_list, file, indent=4)
                with open('project/cogs/project_cogs/image_start.png', 'rb') as file:
                    await message.answer_photo(file)
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(KeyboardButton('send phone number', request_contact=True))
                await message.answer(f'<a href="{os.getenv("TELEGRAPH_1")}">to continue</a> - send phone number',
                                     reply_markup=markup)
                await RegistrationProcess.registration_phone_number.set()
        except Exception as error:
            print(error)
            ... # add error process

async def start_registration(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        try:
            user_id = str(message.from_user.id)
            database = load_database()
            database_managers_id_list = load_database_managers_id()
            with open('project/cogs/for_users/registration/registration_cogs/registration_list.json', 'r+') as file:
                registration_list = json.load(file)
            registration_list[user_id]['registration_phone_number'] = message.contact.phone_number
            if registration_list[user_id]['registration_inviter_id'] != None:
                registration_list[user_id]['registration_points'] = '500'
                with open('project/cogs/for_users/registration/registration_cogs/registration_list.json', 'w') as file:
                    json.dump(registration_list, file, indent=4)
                with database.cursor() as cursor:
                    select = """
                    SELECT points FROM table1 WHERE user_id = %s
                    """
                    select_values = (registration_list[user_id]['registration_inviter_id'])
                    cursor.execute(select, select_values)
                result = int(cursor.fetchone()[0])
                with database.cursor() as cursor:
                    update = """
                    UPDATE table1 SET points = %s WHERE user_id = %s
                    """
                    update_values = (str(result + 250), registration_list[user_id]['registration_inviter_id'])
                    cursor.execute(update, update_values)
                with database.cursor() as cursor:
                    select = """
                    SELECT invited FROM table1 WHERE user_id = %s
                    """
                    select_values = (registration_list[user_id]['registration_inviter_id'])
                    cursor.execute(select, select_values)
                result = int(cursor.fetchone()[0])
                with database.cursor() as cursor:
                    update = """
                    UPDATE table1 SET invited = %s WHERE user_id = %s
                    """
                    update_values = (str(result + 1), registration_list[user_id]['registration_inviter_id'])
                    cursor.execute(update, update_values)
                database.commit()
                await message.answer('you\'ve been invited (+250 points)')
                await message.bot.send_message(registration_list[user_id]['registration_inviter_id'], text='you invited (+250 points)')
            with database.cursor() as cursor:
                insert = """
                INSERT IGNORE INTO table1 (user_id, inviter_id, invited, date, name, phone, status, points, guide1, guide2, guide3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                insert_values = (user_id, registration_list[user_id]['registration_inviter_id'], 0, registration_list[user_id]['registration_date'], '-', registration_list[user_id]['registration_phone_number'], 'client', registration_list[user_id]['registration_points'], 0, 0, 0)
                cursor.execute(insert, insert_values)
            database.commit()
            await message.bot.send_message(os.getenv('TELEGRAM_'), text=f"""
logs {time.strftime('%d.%m.%Y %H:%M')}

    user ({user_id}) is registered by {registration_list[user_id]['registration_inviter_id']}
                                      """)
            with open('project/cogs/for_users/registration/registration_cogs/registration_list.json', 'r+') as file:
                registration_list = json.load(file)
            del registration_list[user_id]
            with open('project/cogs/for_users/registration/registration_cogs/registration_list.json', 'w') as file:
                    json.dump(registration_list, file, indent=4)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('c.s. menu')).add(KeyboardButton('c.s. information')).add(KeyboardButton('c.s. card'))
            if user_id in database_managers_id_list:
                markup.add(KeyboardButton('manager\'s menu'))
            await message.answer('continue... menu is called up',
                                 reply_markup=markup)
            await state.finish()
        except Exception as error:
            await state.finish()
            print(error)
            ... # add error process

def load_users_registration(bot_dp: Dispatcher):
    bot_dp.register_message_handler(start, commands=['start'], state='*')
    bot_dp.register_message_handler(start_registration, content_types=types.ContentTypes.CONTACT, state=RegistrationProcess.registration_phone_number)
