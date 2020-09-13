from ithemba_walkathon.env import GLOBAL_TOPIC
from ..clients.firebase import send_message


def handle_system_message_update(system_message):
    message = {
        'notification': {
            'title': system_message.title,
            'body':  system_message.message,
            'image': system_message.image_url,
        },
        'data': {
            'message_pk': str(system_message.pk),
            'title': str(system_message.title),
            'body': str(system_message.message),
            'image': str(system_message.image_url),
        },
        'topic': GLOBAL_TOPIC
    }

    send_message(message)
