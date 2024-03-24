
import aiogram
from aiogram import Bot, Dispatcher

import project.cogs.for_users.users_card
from project.cogs.for_users.users_card import users_c_s_card_giveaway_, users_c_s_card_giveaway_result

async def loop_users_1(bot: Bot):
    await users_c_s_card_giveaway_(bot)

async def loop_users_2(bot: Bot):
    await users_c_s_card_giveaway_result(bot)

def load_users_loops(bot_dp: Dispatcher):
    ...
