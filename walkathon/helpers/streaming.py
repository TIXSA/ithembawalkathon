from ithemba_walkathon.env import GLOBAL_TOPIC
from ..clients.firebase import send_message


def handle_stream_update_or_create():
    message = {
        'notification': {
            'title': 'Hi Man',
            'body': 'Hi Man bodybodybody body body vbody body body',
            'image': '',
        },
        'data': {
            'fata': 'Hi Man',
            'man': 'Hi Man',
        },
        'topic': GLOBAL_TOPIC
    }

    send_message(message)
