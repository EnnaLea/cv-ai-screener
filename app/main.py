from app.core.email_scraper import EmailCVScraper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os


def main():
    # Chiedi le credenziali all'utente
    email = input("Inserisci la tua email Gmail: ")
    password = input("Inserisci la tua password: ")

    # Crea l'istanza dello scraper
    scraper = EmailCVScraper(email, password)

    try:
        # Prova il login
        if scraper.login():
            print("Login effettuato con successo!")

            # Crea la cartella per i download
            download_folder = "./cv_downloads"
            os.makedirs(download_folder, exist_ok=True)

            # Scarica i CV
            downloaded_files = scraper.download_cvs(download_folder)

            if downloaded_files:
                print(f"Scaricati {len(downloaded_files)} CV:")
                for file in downloaded_files:
                    print(f"  - {file}")
            else:
                print("Nessun CV trovato nella mailbox")

        else:
            print("Login fallito. Controlla le credenziali e riprova.")

    except Exception as e:
        print(f"Si è verificato un errore: {e}")

    finally:
        # Chiudi il browser
        scraper.close()
        print("Browser chiuso.")


if __name__ == "__main__":
    main()