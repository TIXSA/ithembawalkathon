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
    apns = messaging.APNSConfig(
        fcm_options=messaging.APNSFCMOptions(
            image=notification['image'],
        ),
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                content_available=True,
                mutable_content=True,
                sound='default'
            )
        ),
        headers={
            'apns-push-type': 'background',
            'apns-priority': '5',
            'apns-topic': 'org.reactjs.native.avon.IthembaWalkathon'
        }
    )
    notification = messaging.Notification(
        title=notification['title'],
        body=notification['body'],
        image=notification['image'],
    )
    android = messaging.AndroidConfig(
        priority='high'
    )

    return messaging.Message(
        data=message['data'],
        notification=notification,
        topic=message['topic'],
        android=android,
        apns=apns
    )


def build_refresh_message(message):
    apns = messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                content_available=True,
                mutable_content=True,
            )
        ),
        headers={
            'apns-push-type': 'background',
            'apns-priority': '5',
            'apns-topic': 'org.reactjs.native.avon.IthembaWalkathon'
        }
    )

    android = messaging.AndroidConfig(
        priority='high'
    )

    return messaging.Message(
        data=message['data'],
        topic=message['topic'],
        android=android,
        apns=apns
    )


def send_message(message, refresh=None):
    try:
        if refresh:
            messaging.send(build_refresh_message(message))
        else:
            messaging.send(build_message(message))

    except exceptions.FirebaseError as ex:
        print('Error message:', ex)
        print('Error code:', ex.code)
        print('HTTP response:', ex.http_response)
