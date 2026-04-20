import os
import requests
from bs4 import BeautifulSoup
import time

# KONFIGURACJA
BASE_URL = "https://architektura.um.warszawa.pl/plany-miejscowe-bemowo" # Tu wpiszemy konkretny adres
FOLDER_DOCS = "Baza_MPZP_Warszawa"

# Udajemy przeglądarkę, żeby serwer nas nie wyrzucił
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def stworz_strukture():
    if not os.path.exists(FOLDER_DOCS):
        os.makedirs(FOLDER_DOCS)
        print(f"Stworzono folder główny: {FOLDER_DOCS}")

def pobierz_liste_planow(url):
    print(f"Łączenie ze stroną: {url}...")
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # TU BĘDZIE LOGIKA WYCIĄGANIA LINKÓW Z TABELI
        return soup
    else:
        print(f"Błąd połączenia: {response.status_code}")
        return None

# TESTOWE URUCHOMIENIE
stworz_strukture()
# Tu wywołamy funkcję pobierania, gdy podasz strukturę tabeli