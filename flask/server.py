from flask import Flask, render_template, request
from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials, firestore

sense = SenseHat()

app = Flask(__name__)

sense_values = {
    'value' : '#000000',
    'type' : 'hex'
}

COLLECTION = 'raspberry'

DOCUMENT = 'lector-pi'

def hexToRgb(a):
    h = a.lstrip('#')
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb

@app.route('/')
def index():
    return 'Home. Please navigate to another route.'

@app.route('/hello')
def hello():
    return 'You have reached the Pi of Wouter Janssens'


@app.route('/sensehat', methods=['GET', 'POST'])



def sensehat():
    if(request.method == 'POST'):
        sense_values['value'] = request.form['senseColor']
        print(request.form['senseColor'])
        newPixels = hexToRgb(request.form['senseColor'])

        X = [newPixels[0], newPixels[1], newPixels[2]]  # Red
        O = [newPixels[0], newPixels[1], newPixels[2]] # White

        question_mark = [
        O, O, O, X, X, O, O, O,
        O, O, X, O, O, X, O, O,
        O, O, O, O, O, X, O, O,
        O, O, O, O, X, O, O, O,
        O, O, O, X, O, O, O, O,
        O, O, O, X, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, X, O, O, O, O
        ]
        sense.set_pixels(question_mark)

        #firebase
        cred = credentials.Certificate("./config/labo-i-firebase-adminsdk-nr652-7d2e873b71.json")
        appname = "Color App"
        firebase_admin.initialize_app(cred , "Wouter")

        #connect firestore
        db = firestore.client()

        waarden = {
        u'matrix' : {
            u'color' : {
                u'type' : "hex",
                u'value' :  request.form['senseColor']

            },
            u'isOn' : "True"
        }
        }

        db.collection(COLLECTION).document(DOCUMENT).set(waarden)
        
    return render_template('sensehat.html', sense_values = sense_values )

# server consts

host = '192.168.0.244'
port = 8081
if __name__ == '__main__':
    app.run(host=host, port=port, debug= True)
    
    