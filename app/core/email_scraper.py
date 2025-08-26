from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


class EmailCVScraper:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        self._setup_browser()

    def _setup_browser(self):
        """Configura Chrome per evitare il blocco di Google"""
        chrome_options = webdriver.ChromeOptions()

        # Impostazioni per evitare il rilevamento come bot
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # User agent normale
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Altre impostazioni importanti
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1400,900")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

        # Nasconde l'identificazione come automation
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def login(self):
        """Login a Gmail con inserimento forzato della password"""
        try:
            # Vai alla pagina di login
            self.driver.get("https://accounts.google.com")
            time.sleep(3)

            # Inserisci email
            email_field = self.driver.find_element(By.NAME, "identifier")
            email_field.send_keys(self.email)
            time.sleep(1)

            # Clicca Avanti
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            time.sleep(3)

            # FORZA L'INSERIMENTO PASSWORD - SOLUZIONE SEMPLICE
            # Prova diversi selettori per il campo password
            password_selectors = [
                (By.NAME, "password"),
                (By.NAME, "Passwd"),
                (By.XPATH, "//input[@type='password']"),
                (By.XPATH, "//input[@aria-label='Inserisci la password']")
            ]

            password_field = None
            for selector_type, selector_value in password_selectors:
                try:
                    password_field = self.driver.find_element(selector_type, selector_value)
                    if password_field:
                        break
                except:
                    continue

            if not password_field:
                print("❌ Campo password non trovato")
                return False

            # Forza l'inserimento della password
            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(1)

            # Clicca Avanti
            password_next = self.driver.find_element(By.ID, "passwordNext")
            password_next.click()
            time.sleep(5)

            # Gestisci verifica 2FA se presente
            if self._check_2fa_required():
                print("📱 Verifica 2FA richiesta - conferma dal telefono")
                return self._handle_2fa()

            return "mail.google.com" in self.driver.current_url



        except Exception as e:
            print(f"Errore durante il login: {e}")
            return False

    def _check_2fa_required(self):
        """Controlla se è richiesta la verifica 2FA"""
        try:
            # Controlla elementi della pagina 2FA
            page_text = self.driver.page_source.lower()
            return any(word in page_text for word in ["verifica", "2-step", "two-step", "codice"])
        except:
            return False

    def _handle_2fa(self):
        """Gestisce la verifica 2FA in modo pulito"""
        print("👉 Conferma l'accesso dal tuo smartphone...")
        print("⏳ Attendo 30 secondi per la conferma...")

        # Attendi la conferma
        for _ in range(30):
            if "mail.google.com" in self.driver.current_url:
                print("✅ Login completato!")
                return True
            time.sleep(1)

        print("❌ Tempo scaduto - verifica non confermata")
        return False

    def download_cvs(self, download_folder="./cv_downloads"):
        """Scarica i CV dalla mailbox"""
        try:
            # Assicurati di essere nella pagina di Gmail
            if "mail.google.com" not in self.driver.current_url:
                self.driver.get("https://mail.google.com")
                time.sleep(3)

            # Cerca email con allegati
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys("has:attachment (cv OR curriculum OR resume)")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

            # Trova le email con allegati
            emails = self.driver.find_elements(By.XPATH, "//tr[.//text()['allegati' or 'attach']]")
            downloaded_files = []

            for i, email in enumerate(emails[:3]):  # Massimo 3 email per prova
                try:
                    email.click()
                    time.sleep(2)

                    # Trova il pulsante di download
                    download_btn = self.driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Scarica')]")
                    download_btn.click()
                    time.sleep(2)

                    downloaded_files.append(f"cv_{i + 1}.pdf")

                    # Torna indietro
                    self.driver.back()
                    time.sleep(2)

                except Exception as e:
                    continue

            return downloaded_files

        except Exception as e:
            print(f"Errore durante lo scaricamento: {e}")
            return []

    def close(self):
        """Chiude il browser"""
        try:
            self.driver.quit()
        except:
            pass