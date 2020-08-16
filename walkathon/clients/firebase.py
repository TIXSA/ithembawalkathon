import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('../configs/ithemba-walkathon-dev-firebase-adminsdk-i2bp3-7b342a165e.json')
firebase_admin.initialize_app(cred)
