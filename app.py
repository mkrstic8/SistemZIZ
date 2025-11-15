from flask import Flask, render_template_string
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

    
    
load_dotenv()

app = Flask(__name__)





MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER")
MONGO_DB = os.environ.get("MONGO_DB")

encoded_password = quote_plus(MONGO_PASSWORD)

uri = f"mongodb+srv://{MONGO_USER}:{encoded_password}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"

        
client = MongoClient(uri, server_api=ServerApi('1'))

# Izaberi bazu i kolekciju
db = client[MONGO_DB]
prisustvo = db["PrisustvoNastavnika"]

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) # Allow requests from Next.js

# @app.route("/api/data")
# def get_data():
#     return {"message": "Milance"} testing api


@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ZIZ Sistem</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
            .btn { 
                display: inline-block; 
                padding: 15px 30px; 
                background-color: #4CAF50; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Dobrodošli u Sistem ZIZ</h1>
        <p>Flask aplikacija je pokrenuta uspešno! ✅</p>
        <p>MongoDB konekcija će biti testirana posebno.</p>
        <a href="/test-db" class="btn">Testiraj MongoDB</a>
    </body>
    </html>
    """



@app.route('/unesi_fiksno')
def unesi_fiksno():
    uuid = "123e456789b12d3a456-426614174000"
    
    # Pronađi poslednji zapis za ovaj UUID (bilo kada u prošlosti)
    poslednji_zapis = prisustvo.find_one(
        {"uuid": uuid},
        sort=[("vreme", -1)]  # Sortiraj po vremenu opadajuće - da dobijemo najskoriji
    )
    
    # Ako postoji prethodni zapis, uzmi suprotni status od poslednjeg
    # Ako ne postoji (prvi put), podrazumevano je True (prisutan)
    if poslednji_zapis:
        novi_status = not poslednji_zapis["prisutan"]
    else:
        novi_status = True
    
    # Kreiraj novi dokument sa trenutnim vremenom
    dokument = {
        "uuid": uuid,
        "ime_prezime": "Milan Krstić",
        "katedra": "Tehničko obrazovanje",
        "prisutan": novi_status,
        "vreme": datetime.now()
    }
    
    # Ubaci novi dokument u kolekciju
    prisustvo.insert_one(dokument)
    
    status_tekst = "prisutan" if novi_status else "odsutan"
    return f"<h2>✅ Novi unos dodat! Status: {status_tekst}!</h2>"
# MARK: 01 rest api
#SETOVANJE RESTAPI 
@app.route("/api/users", methods=["GET"])
def get_users():
    # Vrati sve dokumente iz Prisustvo kolekcije
    data = list(prisustvo.find({}))  # izbacujemo Mongo _id  {"_id": 0},
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)

#MARK: 02 DEEPFACE
@app.route("/api/verify_face", methods=["POST"])
def verify_face():
    from deepface import DeepFace
    DeepFace.stream(db_path='User\Database',anti_spoofing=True, enable_face_analysis=True)# strimuje u realnom vremenu
    #dfs = DeepFace.find(img_path = "img1.jpg", db_path = 'User\Database') # pretraga slike

    # objs = DeepFace.analyze(
    #   img_path = 'img1.jpg', actions = ['age', 'gender', 'race', 'emotion']
    # )

# print (objs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)