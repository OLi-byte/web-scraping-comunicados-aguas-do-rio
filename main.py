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


def main():
    driver.get("https://aguasdorio.com.br/comunicados/")

    try:
        sleep(3)
        button = driver.find_element(By.XPATH, "//button[text()='Mais Comunicados']")
        button.click()
        sleep(3)

        div_elements = driver.find_elements(
            By.XPATH, '//div[@data-component="card-news"]'
        )

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

                print(f"Título: {title_text}")
                print(f"Data: {date_text}")
                print(f"Texto: {full_text}")

                body = f"Título: {title_text}\n\nData: {date_text}\n\nTexto: {full_text}\n\n---------------------------\n\n"

                with open("last-results.txt", "a", encoding="utf-8") as file:
                    file.write(body)

                print("-----")

                send_email(
                    "Comunicados Águas do Rio", body, os.getenv("EMAIL_RECEIVER")
                )
            except Exception as e:
                print(f"Erro ao buscar elementos dentro da div: {e}")

    except Exception as e:
        print(f"Elemento não encontrado ou ocorreu um erro: {e}")


if __name__ == "__main__":
    main()
