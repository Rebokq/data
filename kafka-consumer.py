from kafka.consumer import KafkaConsumer
import json
from pymongo import MongoClient

# Configuration du consommateur Kafka
bootstrap_servers = 'localhost:9092'
topic_name = 'crypto'

# Configuration de la connexion à MongoDB
mongo_client = MongoClient('mongodb://localhost:27017')
db = mongo_client['crypto_db']
collection = db['crypto_collection']

# Initialiser le consommateur Kafka
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_servers,
    group_id='unique_crypto_group_id',
    client_id='unique_client_id',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda x: x.decode('utf-8')
)

# Lire et traiter les messages du topic Kafka
for message in consumer:
    try:
        crypto_data = json.loads(message.value)
        print(f"Nom: {crypto_data['crypto_name']}, Nom Complet: {crypto_data['crypto_full_name']},  Prix: {crypto_data['price']}, Image: {crypto_data['image_url']}")

        # Rechercher un document avec le même nom de crypto dans la collection
        existing_document = collection.find_one({'crypto_name': crypto_data['crypto_name']})

        if existing_document:
            # Mise à jour du document existant avec les nouvelles données
            collection.update_one(
                {'crypto_name': crypto_data['crypto_name']},
                {'crypto_full_name': crypto_data['crypto_full_name']},
                {'$set': {'price': crypto_data['price']}},
                {'image_url': crypto_data['image_url']},


            )
        else:
            # Insérer le nouveau document s'il n'existe pas
            collection.insert_one(crypto_data)

        # Marquer le message comme consommé manuellement
        consumer.commit()
    except json.decoder.JSONDecodeError as e:
        print(f"Erreur de décodage JSON: {e}")
    except Exception as ex:
        print(f"Erreur lors de l'insertion/mise à jour dans la base de données: {ex}")

# Fermer le consommateur Kafka
consumer.close()
