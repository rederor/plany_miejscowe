import os
from pypdf import PdfReader

SOURCE_ROOT = "."  # Tu masz foldery Baza_MPZP_...
OUTPUT_ROOT = "PROCESSED_TEXT"

def napraw_baze():
    print(">>> START NAPRAWY: Wyciągam tekst z KAŻDEGO PDF-a <<<")
    
    for root, dirs, files in os.walk(SOURCE_ROOT):
        # Ignorujemy folder wynikowy i foldery systemowe
        if OUTPUT_ROOT in root or ".git" in root:
            continue
            
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                
                # Tworzymy ścieżkę docelową
                rel_path = os.path.relpath(root, SOURCE_ROOT)
                target_dir = os.path.join(OUTPUT_ROOT, rel_path)
                
                txt_name = file.lower().replace(".pdf", ".txt")
                txt_path = os.path.join(target_dir, txt_name)

                # JEŚLI PLIKU NIE MA - MIELIMY
                if not os.path.exists(txt_path):
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    
                    print(f"Dodaję brakujący: {file}")
                    try:
                        reader = PdfReader(pdf_path)
                        text = ""
                        for page in reader.pages:
                            t = page.extract_text()
                            if t: text += t + "\n"
                        
                        with open(txt_path, "w", encoding="utf-8") as f:
                            if len(text.strip()) < 100:
                                f.write("--- DO SPRAWDZENIA: PRAWDOPODOBNIE SKAN ---")
                            else:
                                f.write(text)
                    except:
                        print(f"  [BŁĄD] Plik uszkodzony: {file}")

    print("\n>>> KONIEC. Teraz sprawdź właściwości folderu PROCESSED_TEXT! <<<")

if __name__ == "__main__":
    napraw_baze()