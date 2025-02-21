import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
import shutil
import json
import base64
from Captcha.main import audio_to_text


def runSearch(numero_processo):
    # Configurações do WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    # Definir diretório de download
    download_dir = os.path.join(os.getcwd(), 'search_downloads')
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
        driver.get('https://pje.trt8.jus.br/consultaprocessual/')

        # 2. Selecionar o campo de busca com id
        search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'nrProcessoInput'))
        )
        print("Campo de busca encontrado.")

        # 3. Preencher o campo de busca com o número do processo
        search_field.send_keys(numero_processo)
        print("Número do processo preenchido.")

        # 4. Clicar no botão de busca
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnPesquisar'))
        )
        search_button.click()
        print("Botão de busca clicado.")

        # Espera para garantir que a página esteja totalmente carregada
        time.sleep(2)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'btnCarregarAudio'))
        )

        # 5. Passando pelo captcha
        bypass_captcha = False

        while not bypass_captcha:
            time.sleep(2)
            print("checando se o captcha foi resolvido...")

            # Verifica se o botão de audio do captcha está presente
            captcha_audio_button = driver.find_elements(By.ID, 'btnCarregarAudio')

            print(captcha_audio_button)
            
            # Verifica se o botão de recarregar o captcha está presente
            reload_button = driver.find_elements(By.ID, 'btnRecarregar')

            print(reload_button)

            time.sleep(2)

            if reload_button or captcha_audio_button:
                print("Captcha não resolvido.")

                if reload_button:
                    reload_button[0].click()
                elif captcha_audio_button:
                    captcha_audio_button[0].click()
                    
                print("Botão de recarregar clicado.")

                time.sleep(2)

                # Encontra a resposta da API com o áudio do captcha
                for request in driver.requests:
                    if "audio" in request.url:
                        print(f"URL: {request.url}")
                        print(f"Status Code: {request.response.status_code}")
                        response = request.response.body
                
                data = json.loads(response.decode("utf-8"))

                audio_base64 = data['audio']

                # Converter o áudio do captcha em texto
                captcha_text = audio_to_text(audio_base64)
                
                # transforma a lista em uma string de numeros e as letras maiusculas em minusculas
                captcha_text = ''.join(captcha_text).lower()
                print(f"Texto do captcha: {captcha_text}")

                captcha_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'captchaInput'))
                )

                # Preencher o campo de texto do captcha
                captcha_input.send_keys(captcha_text)
                print("Texto do captcha preenchido.")

                time.sleep(5) # Tirar depois

                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'btnEnviar'))
                )

                submit_button.click()
                print("Botão de enviar captcha clicado.")

            else:
                print("Captcha resolvido com sucesso.")
                bypass_captcha = True

        time.sleep(15) 

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    runSearch("0001199-25.2024.5.08.0113")