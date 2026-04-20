import os
import requests
from bs4 import BeautifulSoup
import re
import time

# LISTA DZIELNIC (Bez Bemowa)
DZIELNICE = [
    "bielany", "mokotow", "ochota", "praga-poludnie", 
    "praga-polnoc", "rembertow", "srodmiescie", "targowek", "ursus", 
    "ursynow", "wawer", "wesola", "wilanow", "wlochy", "wola"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def clean_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', str(name)).strip()

def pobierz_dzielnice(dzielnica_name):
    url = f"https://architektura.um.warszawa.pl/{dzielnica_name}"
    base_dir = f"Baza_MPZP_{dzielnica_name.capitalize()}"
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    print(f"\n>>> ROZPOCZYNAM POBIERANIE DZIELNICY: {dzielnica_name.upper()} <<<")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f" [!] Błąd połączenia z {url}: {e}")
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    all_links = soup.find_all('a', href=True)
    
    znalezione = 0
    for link in all_links:
        href = link['href']
        if any(ext in href.lower() for ext in ['.pdf', '.tif', '.gml', '.png']):
            tekst_linku = link.get_text(strip=True) or "plik"
            rodzic = link.find_parent('div')
            tytul = "Nieznany_Plan"
            if rodzic:
                p_tag = rodzic.find('p')
                if p_tag:
                    tytul = p_tag.get_text(strip=True)[:80]
            
            folder_name = clean_filename(tytul)
            sciezka_folderu = os.path.join(base_dir, folder_name)
            
            if not os.path.exists(sciezka_folderu):
                os.makedirs(sciezka_folderu)

            ext = href.split('.')[-1].split('?')[0]
            nazwa_pliku = clean_filename(f"{tekst_linku}.{ext}")
            pelna_sciezka = os.path.join(sciezka_folderu, nazwa_pliku)

            if not os.path.exists(pelna_sciezka):
                try:
                    print(f"  -> [{dzielnica_name}] Pobieram: {tekst_linku}")
                    f_res = requests.get(href, headers=HEADERS, timeout=30)
                    with open(pelna_sciezka, 'wb') as f:
                        f.write(f_res.content)
                    znalezione += 1
                    time.sleep(0.1) # Mała przerwa dla serwera
                except:
                    print(f"     [!] Błąd pobierania: {href}")
    
    print(f" ZAKOŃCZONO {dzielnica_name.upper()}. Pobrano nowych plików: {znalezione}")

if __name__ == "__main__":
    for d in DZIELNICE:
        pobierz_dzielnice(d)
    print("\n==========================================")
    print("MISJA ZAKOŃCZONA: CAŁA WARSZAWA POBRANA!")
    print("==========================================")