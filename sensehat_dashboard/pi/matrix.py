from flask import Flask, render_template, request
from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("./config/labo-i-firebase-adminsdk-nr652-7d2e873b71.json")

firebase_admin.initialize_app(cred)

#connect firestore

db = firestore.client()

def on_snapshot(doc_snapshot, changes, read_time):
  for doc in doc_snapshot:
    doc_dict = doc.to_dict()
    print(doc_dict)

# Get the pi ref
pi_ref = db.collection(COLLECTION_NAME).document(PI_ID)
pi_watch = pi_ref.on_snapshot(on_snapshot)

