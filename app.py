from flask import Flask, render_template_string
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

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
prisustvo = db["Prisustvo"]


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
    dokument = {
        "ime_prezime": "Milan Krstić",
        "katedra": "Tehničko obrazovanje",
        "prisutan": True,
        "vreme": datetime.now()
    }

    prisustvo.insert_one(dokument)
    return "<h2>✅ Fiksni unos uspešno dodat u kolekciju Prisustvo!</h2>"

# MARK: 01 rest api
#SETOVANJE RESTAPI 
@app.route("/api/users", methods=["GET"])
def get_users():
    # Vrati sve dokumente iz Prisustvo kolekcije
    docs = list(prisustvo.find({}, {"_id": 0}))  # izbacujemo Mongo _id
    return jsonify(docs)

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
# @app.route('/test-db')
# def test_db():
#     """Test MongoDB connection separately"""
#     try:
#         from pymongo.mongo_client import MongoClient
#         from pymongo.server_api import ServerApi
#         from urllib.parse import quote_plus
        
#         # Replace with your actual password
#         password = "Pskssp555"
#         encoded_password = quote_plus(password)
#         uri = f"mongodb+srv://mkrstic8_db_user:{encoded_password}@cluster0.pcrpliz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
#         client = MongoClient(uri, server_api=ServerApi('1'))
#         client.admin.command('ping')
        
#         return """
#         <!DOCTYPE html>
#         <html>
#         <head><title>Test DB</title></head>
#         <body>
#             <h1 style="color: green;">✅ MongoDB konekcija uspešna!</h1>
#             <p>Baza podataka je dostupna.</p>
#             <a href="/">Nazad na početnu</a>
#         </body>
#         </html>
#         """
        
#     except Exception as e:
#         return f"""
#         <!DOCTYPE html>
#         <html>
#         <head><title>Greška DB</title></head>
#         <body>
#             <h1 style="color: red;">❌ MongoDB greška: {str(e)}</h1>
#             <p>Proverite korisničko ime i lozinku.</p>
#             <a href="/">Nazad na početnu</a>
#         </body>
#         </html>
#         """

if __name__ == '__main__':
    app.run(debug=True, port=5000)