from django.forms import model_to_dict
from ..clients.firebase import send_message


def handle_stream_update_or_create(stream):
    print('hiiiii')
    print(model_to_dict(stream))
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
        'topic': 'walkathon_global'
    }

    send_message(message)
