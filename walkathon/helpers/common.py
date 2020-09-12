from ..clients.firebase import send_message
from datetime import datetime, timedelta


def handle_model_update(page):
    message = {
        'data': {
            'refresh_app_page': str(page),
        },
        'topic': 'dev_walkathon_global'
    }

    send_message(message, True)


def iso_string_to_datetime(iso_date_string):
    return datetime.strptime(iso_date_string, "%a, %d %b %Y %H:%M:%S %Z") + timedelta(hours=2)
