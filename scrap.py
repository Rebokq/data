import requests
from bs4 import BeautifulSoup

# URL de la page que vous souhaitez scraper

url = 'https://www.coingecko.com/fr'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)

# Faire une requête GET à l'URL
response = requests.get(url)

# Vérifier si la requête a réussi (code d'état HTTP 200)
if response.status_code == 200:
    # Utilisation de Beautiful Soup pour analyser le HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Maintenant, vous pouvez extraire les informations comme dans l'exemple précédent
    nom_crypto_element = soup.select_one('td a div.tw-font-semibold')
    nom_crypto = nom_crypto_element.get_text(strip=True) if nom_crypto_element else "Nom non trouvé"

    prix_crypto_element = soup.select_one('td span[data-price-target="price"]')
    prix_crypto = prix_crypto_element.get_text(strip=True) if prix_crypto_element else "Prix non trouvé"

    # Affichage des résultats
    print(f"Nom de la cryptomonnaie : {nom_crypto}")
    print(f"Prix de la cryptomonnaie : {prix_crypto}")
else:
    print(f"Échec de la requête. Code d'état HTTP : {response.status_code}")
