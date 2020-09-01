import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import exceptions

credentials_path = os.path.join(
    os.path.dirname(__file__),
    '../configs/ithemba-walkathon-dev-firebase-adminsdk-i2bp3-7b342a165e.json')
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred)


def build_message(message):
    notification = message['notification']
    notification = messaging.Notification(
        title=notification['title'],
        body=notification['body'],
        image=notification['image'],
    )
    return messaging.Message(
        data=message['data'],
        notification=notification,
        topic=message['topic']
    )


def send_message(message):
    try:
        messaging.send(build_message(message))
    except exceptions.FirebaseError as ex:
        print('Error message:', ex)
        print('Error code:', ex.code)
        print('HTTP response:', ex.http_response)
