from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials, firestore
import time
from datetime import datetime

# consts

COLLECTION = 'raspberry'

DOCUMENT = 'sensor-data'



#firebase
cred = credentials.Certificate("../config/labo-i-firebase-adminsdk-nr652-7d2e873b71.json")
firebase_admin.initialize_app(cred)


#connect firestore
db = firestore.client()

#sensehat

sense = SenseHat()

sense.set_imu_config(False, False, False)

sense.clear()

while True:
    waarden = {
        u'pressure' : sense.get_pressure(),
        u'temperature' : sense.get_temperature()
    }

    db.collection(COLLECTION).document(DOCUMENT).set(waarden)
    cTime = datetime.now()
    print('[{0}] Updated firestore with current environment values!'.format(cTime))
    # repeat every 2 minutes

    time.sleep(120)


