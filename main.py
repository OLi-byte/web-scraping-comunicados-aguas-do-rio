import os
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
# chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=chrome_options
)


def load_results():
    for i in range(2):
        try:
            sleep(3)
            button = driver.find_element(
                By.XPATH, "//button[text()='Mais Comunicados']"
            )
            button.click()
            sleep(3)
            print("Mais resultados carregados")
        except:
            print("Erro ao carregar mais resultados")


def main():
    driver.get("https://aguasdorio.com.br/comunicados/")
    new_results = []

    try:
        load_results()

        div_elements = driver.find_elements(
            By.XPATH, '//div[@data-component="card-news"]'
        )

        print(f"{len(div_elements)} comunicados carregados")

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

                keywords = ["Grande Tijuca" "Tijuca", "Vila Isabel", "Capital"]

                match = veriry_keywords(keywords, title_text, full_text)

                if not match:
                    continue

                email = f"Título: {title_text}\n\nData: {date_text}\n\nTexto: {full_text}\n\n---------------------------\n\n"

                try:
                    with open("last-results.txt", "r", encoding="utf-8") as file:
                        last_results = file.read()
                except Exception as e:
                    print("Últimos resultados não encontrados...")
                    last_results = ""

                if title_text in last_results:
                    print(f"{title_text[:30]}... já está nos resultados")
                    continue

                new_results.append(email)

                send_email(
                    "Comunicados Águas do Rio", email, os.getenv("EMAIL_RECEIVER")
                )
            except Exception as e:
                print(f"Erro ao buscar elementos dentro da div: {e}")

        if new_results:
            with open("last-results.txt", "w", encoding="utf-8") as file:
                file.write("".join(new_results) + last_results)
            print("Arquivo atualizado com novos resultados.")

    except Exception as e:
        print(f"Elemento não encontrado ou ocorreu um erro: {e}")


if __name__ == "__main__":
    main()
