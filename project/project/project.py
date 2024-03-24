
import aiogram
from aiogram import Bot, Dispatcher, executor, contrib
from aiogram.contrib import fsm_storage
from aiogram.contrib.fsm_storage import memory
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import dotenv
from dotenv import load_dotenv
load_dotenv()

import os

import apscheduler
from apscheduler import schedulers, triggers
from apscheduler.schedulers import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers import cron
from apscheduler.triggers.cron import CronTrigger

import time

import project.cogs.cogs
from project.cogs.cogs import load_cogs

import project.cogs.for_users.loops.loops
from project.cogs.for_users.loops.loops import loop_users_1, loop_users_2
import project.cogs.for_managers.loops.google.google
from project.cogs.for_managers.loops.google.google import loop_google

async def on_startup(bot_dp: Dispatcher):
    try:    
        load_cogs(bot_dp)
    except Exception as error:
        print(error)
        ... # add error process

def start():
    bot = Bot(os.getenv('TELEGRAM_TOKEN'), parse_mode='HTML')
    bot_dp = Dispatcher(bot, storage=MemoryStorage())
    scheduler_loop_users_1 = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler_loop_users_1_trigger = CronTrigger(hour=13, minute=55)
    scheduler_loop_users_1.add_job(loop_users_1, trigger=scheduler_loop_users_1_trigger, kwargs={'bot': bot}), scheduler_loop_users_1.start()
    scheduler_loop_users_2 = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler_loop_users_2_trigger = CronTrigger(hour=14, minute=00)
    scheduler_loop_users_2.add_job(loop_users_2, trigger=scheduler_loop_users_2_trigger, kwargs={'bot': bot}), scheduler_loop_users_2.start()
    # scheduler_loop_google = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler_loop_google_trigger = CronTrigger(hour=13, minute=45)
    # scheduler_loop_google.add_job(loop_google, trigger=scheduler_loop_google_trigger), scheduler_loop_google.start()
    executor.start_polling(bot_dp, on_startup=on_startup)
