from selenium import webdriver
from functions import veriry_keywords
from selenium.webdriver.common.by import By
from functions import break_lines
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

driver.get("https://aguasdorio.com.br/comunicados/")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-component="card-news"]'))
    )

    div_elements = driver.find_elements(By.XPATH, '//div[@data-component="card-news"]')

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

            if paragraph_elements:
                paragraph_texts = [p.text for p in paragraph_elements]
                full_text = break_lines((" ".join(paragraph_texts)), 150)

                keywords = ["Grande Tijuca" "Tijuca", "Vila Isabel", "Capital"]

                match = veriry_keywords(keywords, title_text, full_text)

                if not match:
                    continue

                print(f"Título: {title_text}")
                print(f"Data: {date_text}")
                print(f"Texto: {full_text}")

                with open("last-results.txt", "a", encoding="utf-8") as file:
                    file.write(
                        f"Título: {title_text}\n\nData: {date_text}\n\nTexto: {full_text}\n\n---------------------------\n\n"
                    )
            else:
                print("Nenhum parágrafo encontrado na div com card-text.")

            print("-----")
        except Exception as e:
            print(f"Erro ao buscar elementos dentro da div: {e}")

except Exception as e:
    print(f"Elemento não encontrado ou ocorreu um erro: {e}")
finally:
    driver.quit()
