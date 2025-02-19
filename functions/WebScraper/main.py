import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from WebScraper.utils import *
import os
import shutil

def runWebScraper():
    # Configurações do WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    # Definir diretório de download
    download_dir = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Limpar a pasta de downloads antes de iniciar o processo de webscraping
    if os.path.exists(download_dir):
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove arquivos e links
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove diretórios
            except Exception as e:
                print(f"Erro ao excluir o arquivo {file_path}: {e}")


    prefs = {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    }
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=options)

    try:
        # 1. Entrar no link
        driver.get('https://justica-em-numeros.cnj.jus.br/painel-estatisticas/')

        # 2. Aguardar que a página carregue completamente
        time.sleep(15)  # Espera para garantir que a página esteja totalmente carregada

        # 3. Tentar encontrar o iframe e mudar para ele
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
            driver.switch_to.frame(iframe)
            print("Mudança para o iframe do Power BI bem-sucedida.")
        except:
            print("Erro: iframe do Power BI não encontrado.")
            driver.quit()
            exit()  # Sai do script se o iframe não for encontrado  

        # 4. Tentar encontrar o botão "Downloads" dentro do iframe usando o XPath fornecido
        try:
            # Clique no botão de Downloads
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[4]/transform/div/div[3]/div/div/visual-modern/div/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[11]/div'))
            ).click()
            print("Botão de Downloads encontrado e clicado.")
        except:
            print("Erro: O botão de Downloads não foi encontrado ou não pôde ser clicado.")
            driver.quit()
            exit()  # Sai do script se o botão não for encontrado

        getGrau(driver, '')
        getIndicador(driver, '')
        getTribunal(driver, '')

        driver.switch_to.default_content()

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    runWebScraper()