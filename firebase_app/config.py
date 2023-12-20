import firebase_admin
from firebase_admin import credentials, auth


creds = credentials.Certificate({
    'type': 'service_account',

})
