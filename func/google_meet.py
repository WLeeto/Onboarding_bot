from google_api.calendar import GoogleCalendar
from datetime import datetime, timedelta


def create_google_meet(start_datetime: datetime, headline: str) -> bool:
    """
    Creates google calendar meeting.
    """
    calendar_id = '27fb0cac1f3d69237dfda517ddfbbe14f96b005194efb51aa1154aeea535cdd9@group.calendar.google.com'
    # todo вынести в переменную окружения ?
    calendar = GoogleCalendar()
    end_datetime = start_datetime + timedelta(hours=2)
    description = 'Создано ботом Тимуром'
    calendar.add_calendar(calendar_id=calendar_id)
    calendar.add_event(calendar_id=calendar_id,
                       start_datetime=start_datetime,
                       end_datetime=end_datetime,
                       name=headline,
                       description=description)
    return True
