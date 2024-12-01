import os
import json
import datetime
from time import sleep
from selenium import webdriver
from functions import send_email
from functions import break_lines
from functions import veriry_keywords
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=chrome_options
)


def load_results():
    attempts = 0
    while attempts <= 4:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[text()='Mais Comunicados']")
                )
            )
            sleep(2)
            button.click()
            print("Mais resultados carregados")
            attempts += 1
        except:
            print("Botão 'Mais Comunicados' não encontrado.")
            break


def load_last_results():
    try:
        with open("last-results.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_results(results):
    with open("last-results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


def is_older_than_10_days(date_text):
    try:
        date_obj = datetime.datetime.strptime(date_text, "%d/%m/%Y")
        return (datetime.datetime.now() - date_obj).days > 10
    except:
        return False


def main():
    driver.get("https://aguasdorio.com.br/comunicados/")
    new_results = []

    try:
        load_results()

        div_elements = driver.find_elements(
            By.XPATH, '//div[@data-component="card-news"]'
        )

        print(f"{len(div_elements)} comunicados carregados")

        last_results = [
            result
            for result in load_last_results()
            if not is_older_than_10_days(result["data"])
        ]

        keywords = os.getenv("KEYWORDS").split(",")
        if keywords:
            print("Procurando por...")
            for word in keywords:
                print(word)
        else:
            print("Não há palavras chave especificadas")
            exit()

        for div_element in div_elements:
            try:
                h5_element = div_element.find_element(
                    By.XPATH, './/h5[contains(@class, "card-title")]'
                )
                title_text = h5_element.text

                span_element = div_element.find_element(
                    By.XPATH, './/span[contains(@class, "date")]'
                )
                date_text = span_element.text

                paragraph_elements = div_element.find_elements(
                    By.XPATH, './/div[contains(@class, "card-text")]//p'
                )

                paragraph_texts = [p.text for p in paragraph_elements]
                full_text = break_lines((" ".join(paragraph_texts)), 150)

                match = veriry_keywords(keywords, title_text, full_text)

                if not match:
                    continue

                email = {
                    "titulo": title_text,
                    "data": date_text,
                    "texto": full_text,
                }

                if any(result["titulo"] == title_text for result in last_results):
                    print(f"{title_text}... já está nos resultados")
                    continue

                new_results.append(email)

                send_email(
                    "Comunicados Águas do Rio",
                    f"Título: {title_text}\n\nData: {date_text}\n\nTexto: {full_text}\n\n---------------------------\n\n",
                    os.getenv("EMAIL_RECEIVER"),
                )
            except Exception as e:
                print(f"Erro ao buscar elementos dentro da div: {e}")

        if new_results:
            last_results.extend(new_results)
            save_results(last_results)
            print("Arquivo JSON atualizado com novos resultados.")

    except Exception as e:
        print(f"Elemento não encontrado ou ocorreu um erro: {e}")


if __name__ == "__main__":
    main()
