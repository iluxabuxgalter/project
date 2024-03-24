
import aiogram
from aiogram import Dispatcher

import project.cogs.for_users.users
from project.cogs.for_users.users import load_users
import project.cogs.for_users.users_card
from project.cogs.for_users.users_card import load_users_users_card
import project.cogs.for_users.registration.registration
from project.cogs.for_users.registration.registration import load_users_registration
import project.cogs.for_users.loops.loops
from project.cogs.for_users.loops.loops import load_users_loops
import project.cogs.for_managers.managers
from project.cogs.for_managers.managers import load_managers
import project.cogs.for_managers.registration.registration
from project.cogs.for_managers.registration.registration import load_managers_registration
import project.cogs.for_managers.loops.loops
from project.cogs.for_managers.loops.loops import load_managers_loops

def load_cogs(bot_dp: Dispatcher):
    try:
        cogs = (
            load_users,
            load_users_users_card,
            load_users_registration,
            load_users_loops,
            load_managers,
            load_managers_registration,
            load_managers_loops,
        )
        for cog in cogs:
            cog(bot_dp)
    except Exception as error:
        print(error)
        ... # add error process
