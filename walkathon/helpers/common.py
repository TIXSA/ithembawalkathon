from ..clients.firebase import send_message


def handle_model_update(page):
    message = {
        'data': {
            'refresh_app_page': str(page),
        },
        'topic': 'dev_walkathon_global'
    }

    send_message(message, True)
