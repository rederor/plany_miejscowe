import os
import ssl

# 1. To są "bezpieczniki" dla standardowego SSL Pythona
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl._create_default_https_context = ssl._create_unverified_context

# 2. TO JEST KLUCZ: Wyłączenie weryfikacji w bibliotekach HTTP (httpx, requests)
os.environ['SSL_CERT_FILE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''
# Wymuszenie na bibliotece httpx (używanej przez Gemini), by nie sprawdzała certyfikatów
os.environ['HTTPX_VERIFY'] = 'False' 

from google import genai

# --- KONFIGURACJA ---
# Klient musi być teraz "czysty", bez dodatkowych opcji, które wywalają błąd
client = genai.Client(api_key="****")

# Reszta kodu...

# --- KONFIGURACJA ---
# client = genai.Client(api_key="********")
# MODEL_ID = "gemini-2.5-flash" # To jest aktualny standard w 2026
MODEL_ID = "gemini-2.5-flash-lite"
FOLDER_BASE = "PROCESSED_TEXT"

def uruchom_analize():
    # 1. WYBÓR DZIELNICY
    dzielnice = [d for d in os.listdir(FOLDER_BASE) if os.path.isdir(os.path.join(FOLDER_BASE, d))]
    print("\n🏙️  Dostępne dzielnice:")
    for i, d in enumerate(dzielnice):
        print(f"[{i}] {d.replace('Baza_MPZP_', '')}")
    
    wybor_dz = int(input("\nPodaj numer dzielnicy: "))
    sciezka_dzielnicy = os.path.join(FOLDER_BASE, dzielnice[wybor_dz])

    # 2. WYBÓR FOLDERU PLANU
    plany_foldery = [f for f in os.listdir(sciezka_dzielnicy) if os.path.isdir(os.path.join(sciezka_dzielnicy, f))]
    print(f"\n📄 Plany w {dzielnice[wybor_dz]}:")
    for i, f in enumerate(plany_foldery):
        print(f"[{i}] {f}")
    
    wybor_pl = int(input("\nPodaj numer folderu planu: "))
    sciezka_planu = os.path.join(sciezka_dzielnicy, plany_foldery[wybor_pl])

    # 3. ZNALEZIENIE PLIKU .TXT
    pliki_txt = [f for f in os.listdir(sciezka_planu) if f.endswith('.txt')]
    if not pliki_txt:
        print("❌ Nie znalazłem pliku .txt!")
        return
    
    wybrany_plik = os.path.join(sciezka_planu, pliki_txt[0])

    # 4. CZYTANIE I ANALIZA
    with open(wybrany_plik, 'r', encoding='utf-8') as f:
        tresc_planu = f.read()

    print(f"\n✅ Wczytano: {pliki_txt[0]}")
    symbol = input("🔍 Symbol terenu: ")
    pytanie = input("❓ Pytanie: ")

    prompt = f"Jesteś urbanistą. Analizujesz MPZP dla terenu {symbol}. Pytanie: {pytanie}. Bazuj tylko na tym tekście:\n\n{tresc_planu}"

    print("\n🧠 Gemini (v2.0) analizuje...")
    try:
        # Nowy sposób wywoływania w bibliotece google-genai
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        print("\n" + "="*60 + "\n" + response.text + "\n" + "="*60)
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    uruchom_analize()
