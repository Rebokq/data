from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Informations du proxy
proxy_host = "127.0.0.1"
proxy_port = 8080

# Créer les options Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')

# Configurer le proxy
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = f"{proxy_host}:{proxy_port}"
proxy.ssl_proxy = f"{proxy_host}:{proxy_port}"
chrome_options.add_argument(f'--proxy-server={proxy.http_proxy}')

# Créer le webdriver
driver = webdriver.Chrome(options=chrome_options)

# Charger la page
url = "https://www.binance.com/fr/markets/overview"
driver.get(url)

# Attendre un certain temps pour permettre au contenu de se charger
time.sleep(5)

# Obtenir le HTML de la page après que le contenu dynamique a eu le temps de se charger
html = driver.page_source

# Fermer le navigateur
driver.quit()

# Utiliser BeautifulSoup pour analyser le HTML
soup = BeautifulSoup(html, 'html.parser')

# Trouver tous les éléments avec la classe "css-cn2h2t"
elements = soup.find_all(class_='css-cn2h2t')

for element in elements:
    # Extraire le nom (texte de la balise avec la classe "subtitle3")
    name_tag = element.find(class_='subtitle3')
    name = name_tag.get_text(strip=True) if name_tag else 'Nom non trouvé'

    # Rechercher le prix en remontant dans la structure HTML
    price_tag = element.find_next(class_='css-18yakpx')
    price = price_tag.get_text(strip=True) if price_tag else 'Prix non trouvé'

    # Imprimer le nom et le prix
    print(f'Nom: {name}, Prix: {price}')
