import os
import time
from dotenv import load_dotenv
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
load_dotenv()

SANITA_PUGLIA_URL = "https://www.sanita.puglia.it/servizialcittadino/#/RicercaPrenotazioneDematerializzata?azienda=regionale"
CODICE_FISCALE = os.getenv('CODICE_FISCALE')
TESSERA_SANITARIA = os.getenv('TESSERA_SANITARIA')
NUMERO_RICETTA = os.getenv('NUMERO_RICETTA')


def is_ready(driver: WebDriver):
    return len(driver.find_elements(By.TAG_NAME, "circle")) == 0 and browser.execute_script(
        r"""return document.readyState === 'complete'""")


options = webdriver.ChromeOptions()
options.add_argument("--headless")
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

print("Loading page")
browser.get(SANITA_PUGLIA_URL)
WebDriverWait(browser, 30).until(is_ready)

print("Verifying identity")
button = browser.find_element(By.CLASS_NAME, "buttonaccesso_disattivo")
button.click()
input_element = browser.find_element(By.NAME, "codiceFiscale")
input_element.send_keys(CODICE_FISCALE)
input_element = browser.find_element(By.NAME, "numeroTessera")
input_element.send_keys(TESSERA_SANITARIA)
button = browser.find_element(By.XPATH, '//button[text()=" Verifica "]')
button.click()
WebDriverWait(browser, 30).until(is_ready)

try:
    browser.find_element(By.XPATH, '//div[text()=" Codice Fiscale e Numero Tessera validi "]')
except NoSuchElementException:
    print("Error: validazione codice fiscale/tessera sanitaria")
    exit()

print("Entering patient data")
input_element = browser.find_element(By.NAME, "numeroRicetta")
input_element.send_keys(NUMERO_RICETTA)
browser.find_element(By.ID, "checkboxID").click()  # Tutte le ASL
button = browser.find_element(By.XPATH, '//button[text()=" Cerca "]')
button.click()

print("Looking for reservations...")
try:
    WebDriverWait(browser, 90).until(is_ready)
except TimeoutException:
    print("Error: caricamento prenotazione non andato a buon fine")
    exit()

browser.find_element(By.ID, "mat-select-0").click()
browser.find_element(By.ID, "mat-option-2").click()
time.sleep(2)
if len(browser.find_elements(By.TAG_NAME, "app-table")) == 0:
    print("Error: tabella prenotazioni non trovata")
    exit()

print("Reservations loaded:")
print("")
elements = browser.find_elements(By.CLASS_NAME, "passaggioriga")
new_reservations = []
for element in elements:
    element_text = element.text.split("\n")
    string = element_text[1] + ": " + element_text[4] + " - " + element_text[5]
    print(string)
browser.close()
