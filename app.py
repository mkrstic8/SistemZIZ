from flask import Flask, render_template_string
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus


app = Flask(__name__)






        
client = MongoClient(uri, server_api=ServerApi('1'))

# Izaberi bazu i kolekciju
db = client["db_ZIZ"]
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