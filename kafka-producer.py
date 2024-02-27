from kafka.producer import KafkaProducer
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import uuid  # Importer la bibliothèque uuid


global_id = 0

def scrape_data():
    url = "https://www.binance.com/fr/markets/overview"

    # Utiliser le webdriver de Chrome en mode headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    # Charger la page
    driver.get(url)

    # Attendre un certain temps pour permettre au contenu de se charger
    time.sleep(5)

    # Obtenir le HTML de la page après que le contenu dynamique a eu le temps de se charger
    html = driver.page_source


    # Ajoutez ce print pour voir le HTML dans la console

  
    # Fermer le navigateur
    driver.quit()

    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Trouver tous les éléments avec la classe "css-cn2h2t"
    elements = soup.find_all(class_='css-cn2h2t')

    data_list = []

    for element in elements:
        # Extraire le nom (texte de la balise avec la classe "subtitle3")
        name_tag = element.find(class_='subtitle3')
        name = name_tag.get_text(strip=True) if name_tag else 'Nom non trouvé'

        # Extraire le nom comlplet
        name_complet_tag = element.find(class_='body3 line-clamp-1 truncate text-t-third css-vurnku')
        name_complet = name_complet_tag.get_text(strip=True) if name_complet_tag else 'Nom non trouvé'

        # Rechercher le prix en remontant dans la structure HTML
        price_tag = element.find_next(class_='css-18yakpx')
        price = price_tag.get_text(strip=True) if price_tag else 'Prix non trouvé'

        # Extraire le logo
       
        # Extraire le logo
        # Extraire le logo
        url = soup.select_one( "img.rounded-full.css-1movkv").get("src")
        print("URL:", url)

        # Extraire le logo
        image_tag = element.find('img', class_='rounded-full css-17hofng')
        print("Image tag:", image_tag)

        if image_tag and 'src' in image_tag.attrs:
            image_url = image_tag['src']
        else:
            image_url = 'URL de l\'image non trouvée'
            print("Image URL non trouvée")


    

        # Ajouter les données à la liste
        data_list.append({'crypto_name': name, 'crypto_full_name': name_complet, 'price': price, 'image_url': image_url})

    return data_list

# Configuration du producteur Kafka
bootstrap_servers = 'localhost:9092'  # Assurez-vous de mettre l'adresse correcte de votre cluster Kafka
topic_name = 'crypto'

# Initialiser le producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')  # Utiliser JSON pour la sérialisation
)

# Boucle infinie avec un délai de 30 secondes
while True:
    # Appeler la fonction scrape_data() pour obtenir les données
    crypto_data_list = scrape_data()

    # Envoyer chaque ensemble de données au topic Kafka
    for crypto_data in crypto_data_list:
         # Ajouter un ID unique à chaque ensemble de données
       # Incrémenter l'ID global
        global_id += 1
        crypto_data['id'] = global_id

        producer.send(topic_name, value=crypto_data)

    # Attendre 30 secondes avant de recommencer
    time.sleep(30)

# Notez que vous devrez gérer la fermeture propre du producteur Kafka lorsque vous souhaitez arrêter le script.
