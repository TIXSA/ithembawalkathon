from ithemba_walkathon.env import GLOBAL_TOPIC
from ..clients.firebase import send_message


def handle_system_message_update(system_message, token=None):
    if system_message.message_sent or token:
        print('Sending message to.... ', GLOBAL_TOPIC)
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
        }
        if token:
            message['token'] = token
        else:
            message['topic'] = GLOBAL_TOPIC

        send_message(message)
    else:
        print('Will not send message', GLOBAL_TOPIC)
