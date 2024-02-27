from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka.consumer import KafkaConsumer
import json
import threading

app = Flask(__name__)
socketio = SocketIO(app, debug=True, async_mode='threading', cors_allowed_origins='*')
messages_lock = threading.Lock()

# Configuration du consommateur Kafka
bootstrap_servers = 'localhost:9092'
topic_name = 'crypto'

messages = []

def consume_messages():
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        group_id='crypto_group',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda x: x.decode('utf-8')
    )

    for message in consumer:
        try:
            crypto_data = json.loads(message.value)
            new_message = f"Nom: {crypto_data['crypto_name']}, Prix: {crypto_data['price']}"
            messages.append(new_message)
            socketio.emit('new_message', {'message': new_message}, namespace='/test')
        except json.decoder.JSONDecodeError as e:
            print(f"Erreur de décodage JSON: {e}")

        # Commit manuel de l'offset
        consumer.commit()

# Démarrer le consommateur dans un thread séparé
thread = threading.Thread(target=consume_messages)
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print("Client connected")
    with messages_lock:
        for message in messages:
            socketio.emit('new_message', {'message': message}, namespace='/test')

if __name__ == '__main__':
    socketio.run(app, debug=True)
