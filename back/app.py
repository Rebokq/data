from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from pymongo import MongoClient
import json
from flask_cors import cross_origin

app = Flask(__name__)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/api', methods=['GET'])
@cross_origin()
def get_crypto_data():
    print("Received GET request for crypto_data")

    mongo_client = MongoClient('mongodb://localhost:27017')
    db = mongo_client['crypto_db']
    collection = db['crypto_collection']

    # Récupérer toutes les données de la collection
    crypto_data = list(collection.find({}, {'_id': 0}))

    return jsonify(crypto_data)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    send_crypto_data()

def send_crypto_data():
    mongo_client = MongoClient('mongodb://localhost:27017')
    db = mongo_client['crypto_db']
    collection = db['crypto_collection']

    # Récupérer toutes les données de la collection
    crypto_data = list(collection.find({}, {'_id': 0}))

    # Envoyer les données aux clients connectés via WebSocket
    socketio.emit('crypto_data', json.dumps(crypto_data))

if __name__ == '__main__':
    app.debug = True

    socketio.run(app, debug=True)
