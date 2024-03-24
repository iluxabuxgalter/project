
import dotenv
from dotenv import load_dotenv
load_dotenv()

import os

import pymysql

def load_database():
    try:
        database = pymysql.connect(
            host=os.getenv('DATABASE_IP'),
            port=int(os.getenv('DATABASE_IP_PORT')),
            user=os.getenv('DATABASE_NAME'),
            password=os.getenv('DATABASE_NAME_PASSWORD'),
            database=os.getenv('DATABASE_NAME')
        )
        return database
    except Exception as error:
        print(error)
        ... # add error process

def load_database_users_id():
    try:
        database = load_database()
        with database.cursor() as cursor:
            select = """
            SELECT user_id FROM table1
            """
            cursor.execute(select)
        database_users_id_list = [row[0] for row in cursor.fetchall()]
        return database_users_id_list
    except Exception as error:
        print(error)
        ... # add error process

def load_database_managers_id():
    try:
        database = load_database()
        database_users_id_list, database_managers_id_list = load_database_users_id(), []
        for user_id in database_users_id_list:
            with database.cursor() as cursor:
                select = """
                SELECT status FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result = cursor.fetchone()[0]
            if result == 'client (manager)':
                database_managers_id_list.append(user_id)
        return database_managers_id_list
    except Exception as error:
        print(error)
        ... # add error process
