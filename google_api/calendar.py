import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

from datetime import datetime


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = os.getcwd() + '\google_api\scopes.json'

    def __init__(self):
        crend = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=crend)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }
        return self.service.calendarList().insert(
            body=calendar_list_entry
        ).execute()

    def add_event(self, calendar_id: int,
                  start_datetime: datetime,
                  end_datetime: datetime,
                  name: str, description: str) -> None:
        body = {
            'summary': name,
            'description': description,
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Europe/Moscow',
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'Europe/Moscow',
            }
        }
        return self.service.events().insert(
            calendarId=calendar_id,
            body=body
        ).execute()