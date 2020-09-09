from ..clients.firebase import send_message


def handle_stream_update_or_create(stream):
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
