import os
from pypdf import PdfReader

SOURCE_ROOT = "Baza_MPZP_*" # Szukamy we wszystkich folderach zaczynających się od Baza_
OUTPUT_ROOT = "PROCESSED_TEXT"

def wyciagnij_wszystko():
    print(">>> START AGRESYWNEJ EKSTRAKCJI <<<")
    
    # Lista wszystkich folderów źródłowych (ręczne obejście os.walk dla pewności)
    for root, dirs, files in os.walk("."):
        # Interesują nas tylko foldery z danymi, nie wynikowe
        if OUTPUT_ROOT in root or "python" in root.lower():
            continue
            
        if any(d.startswith("Baza_MPZP_") for d in root.split(os.sep)):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    
                    # Tworzymy bezpieczną ścieżkę docelową
                    rel_path = os.path.relpath(root, ".")
                    target_dir = os.path.join(OUTPUT_ROOT, rel_path)
                    
                    txt_path = os.path.join(target_dir, file.lower().replace(".pdf", ".txt"))

                    if not os.path.exists(txt_path):
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir, exist_ok=True)
                        
                        print(f"Przetwarzam: {file[:40]}...")
                        try:
                            reader = PdfReader(pdf_path)
                            full_text = ""
                            for page in reader.pages:
                                t = page.extract_text()
                                if t: full_text += t + "\n"
                            
                            with open(txt_path, "w", encoding="utf-8") as f:
                                if len(full_text.strip()) < 100:
                                    # TO KLUCZ: Zapisujemy informację, że to skan, 
                                    # żeby folder ISTNIAŁ w PROCESSED_TEXT
                                    f.write("--- SKAN / OBRAZ ---")
                                else:
                                    f.write(full_text)
                        except Exception as e:
                            print(f"  [!] Błąd przy {file}: {e}")

    print("\n>>> GOTOWE. Sprawdź teraz ilość folderów w PROCESSED_TEXT. <<<")

if __name__ == "__main__":
    wyciagnij_wszystko()