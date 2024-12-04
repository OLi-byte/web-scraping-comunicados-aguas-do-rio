import os
import json
import datetime
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from functions import send_email, veriry_keywords
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=chrome_options
)

load_dotenv()


def load_results():
    attempts = 0
    max_attempts = 2
    while attempts < max_attempts:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[text()='Mais Comunicados']")
                )
            )
            sleep(2)
            button.click()
            print(f"Mais resultados carregados ({attempts + 1}/{max_attempts})")
            attempts += 1
        except Exception:
            print("Botão 'Mais Comunicados' não encontrado.")
            break


def save_results(results):
    with open("last-results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    print("Arquivo JSON atualizado com novos resultados.")


def is_date_today(date_text):
    try:
        date_obj = datetime.datetime.strptime(date_text, "%d/%m/%Y").date()
        return datetime.datetime.now().date() == date_obj
    except ValueError:
        return False


def extract_comunicado_data(div_element):
    try:
        title = div_element.find_element(
            By.XPATH, './/h5[contains(@class, "card-title")]'
        ).text
        date = div_element.find_element(
            By.XPATH, './/span[contains(@class, "date")]'
        ).text
        paragraphs = div_element.find_elements(
            By.XPATH, './/div[contains(@class, "card-text")]//p'
        )
        full_text = " ".join(p.text for p in paragraphs)
        return {"titulo": title, "data": date, "texto": full_text}
    except Exception as e:
        print(f"Erro ao extrair dados da div: {e}")
        return None


def main():
    driver.get("https://aguasdorio.com.br/comunicados/")
    print("Página carregada: Comunicados Águas do Rio")

    load_results()

    div_elements = driver.find_elements(By.XPATH, '//div[@data-component="card-news"]')
    print(f"{len(div_elements)} comunicados encontrados.")

    keywords = os.getenv("KEYWORDS", "").split(", ")

    if not keywords:
        print("Nenhuma palavra-chave especificada.")
        return

    print("Procurando por palavras-chave:")
    for word in keywords:
        print(f"- {word}")

    for div_element in div_elements:
        comunicado_data = extract_comunicado_data(div_element)

        if not comunicado_data:
            continue

        title = comunicado_data["titulo"]
        date = comunicado_data["data"]
        text = comunicado_data["texto"]

        if not is_date_today(date):
            continue

        if veriry_keywords(keywords, title, text):
            send_email(
                title=title,
                subject="Comunicados Águas do Rio",
                body=f"Título: {title}\n\nData: {date}\n\nTexto: {text}\n\n---------------------------\n",
                to_emails=os.getenv("EMAIL_RECEIVER"),
            )


if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
