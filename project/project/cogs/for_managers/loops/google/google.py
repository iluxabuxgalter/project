
import google
from google import auth, oauth2
from google.auth import transport
from google.auth.transport import requests
from google.auth.transport.requests import Request
from google.oauth2 import credentials
from google.oauth2.credentials import Credentials

import google_auth_oauthlib
from google_auth_oauthlib import flow
from google_auth_oauthlib.flow import InstalledAppFlow

import googleapiclient
from googleapiclient import discovery
from googleapiclient.discovery import build

import dotenv
from dotenv import load_dotenv
load_dotenv()

import os

import project.cogs.cogs_database
from project.cogs.cogs_database import load_database, load_database_users_id

async def loop_google():
    credentials = None
    if os.path.exists('project/cogs/google_cogs/credentials_token.json'):
        credentials = Credentials.from_authorized_user_file('project/cogs/google_cogs/credentials.json', scopes=os.getenv('GOOGLE_SPREADSHEET_SCOPES'))
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            credentials_flow = InstalledAppFlow.from_client_secrets_file('project/cogs/google_cogs/credentials.json', scopes=os.getenv('GOOGLE_SPREADSHEET_SCOPES'))
            credentials = credentials_flow.run_local_server(port=0)
        with open('project/cogs/google_cogs/credentials_token.json', 'w') as file:
            file.write(credentials.to_json())
    try:
        database = load_database()
        database_users_id_list = load_database_users_id()
        sheets_service = build('sheets', 'v4', credentials=credentials)
        sheets = sheets_service.spreadsheets()
        for user_id in database_users_id_list:
            with database.cursor() as cursor:
                select = """
                SELECT id FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_id = cursor.fetchone()[0]
            with database.cursor() as cursor:
                select = """
                SELECT inviter_id FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_inviter_id = cursor.fetchone()[0]
            with database.cursor() as cursor:
                select = """
                SELECT invited FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_invited = cursor.fetchone()[0]
            with database.cursor() as cursor:
                select = """
                SELECT date FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_date = cursor.fetchone()[0]
            with database.cursor() as cursor:
                select = """
                SELECT name FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_name = cursor.fetchone()[0]
            with database.cursor() as cursor:
                select = """
                SELECT phone FROM table1 WHERE user_id = %s
                """
                select_values = (user_id)
                cursor.execute(select, select_values)
            result_phone = cursor.fetchone()[0]
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
            result_points = cursor.fetchone()[0]
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!A{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_id}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!B{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{user_id}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!C{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_inviter_id}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!D{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_invited}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!E{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_date}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!F{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_name}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!G{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_phone}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!H{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_status}']]}).execute()
            sheets.values().update(spreadsheetId=os.getenv('GOOGLE_SPREADSHEET'), range=f'sheet1!I{result_id + 1}', valueInputOption='USER_ENTERED',
                                   body={'values': [[f'{result_points}']]}).execute()
    except Exception as error:
        print(error)
        ... # add error process
