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
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


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



def consultar_processos(csv_file='filtered_dataset.csv'):
    """
    Realiza consultas processuais no site do TRT8 a partir de um arquivo CSV.
    
    Parâmetros:
        csv_file (str): Caminho para o arquivo CSV contendo os dados filtrados.
                        O arquivo deve conter as colunas 'Tribunal' e 'Processo'.
                        
    Caso o arquivo não seja encontrado, a função exibirá uma mensagem de erro.
    """
    try:
        filtered_dataset = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_file}' não foi encontrado. Execute o arquivo Data.py antes de chamar essa função.")
        return

    # Configurar o WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    # Iterar sobre cada linha do DataFrame
    for index, row in filtered_dataset.iterrows():
        tribunal = row['Tribunal']
        processo = row['Processo']
        
        # Verifica se o tribunal é TRT8
        if tribunal == 'TRT8':
            driver.get('https://pje.trt8.jus.br/consultaprocessual/')
            time.sleep(3)  # Aguarda o carregamento da página

            try:
                # 1. Localiza o campo de entrada e envia o número do processo
                input_field = driver.find_element(By.XPATH, '//*[@id="nrProcessoInput"]')
                input_field.clear()
                input_field.send_keys(processo)
                input_field.send_keys(Keys.RETURN)
                
                time.sleep(10)  # Ajuste conforme a velocidade de carregamento
                print(f"Consulta realizada para o processo: {processo}")

                # 2. Aguarda mais alguns segundos para a página carregar completamente
                time.sleep(15)

                # 3. Extrai o ID único do final da URL (após o '#')
                current_url = driver.current_url
                print(f"URL atual: {current_url}")

                if '#' in current_url:
                    unique_id = current_url.split('#')[-1]  # Pega tudo após o '#'
                else:
                    print("URL não contém '#'. Não é possível extrair o ID.")
                    unique_id = None
                
                if unique_id:
                    try:
                        # 4. Montar o XPath com base nesse ID e clicar no elemento
                        xpath = f"//*[@id='doc_{unique_id}']/div"
                        elemento = driver.find_element(By.XPATH, xpath)
                        elemento.click()
                        print("Elemento encontrado e clicado com sucesso!")

                        # 5. Dar um tempo para o conteúdo (botão de download) carregar
                        time.sleep(3)

                        # 6. Localiza e clica no botão de download
                        try:
                            botao_download = driver.find_element(By.XPATH, "//*[@id='botoes-documento2']/button/span/i")
                            botao_download.click()
                            print("Download solicitado com sucesso!")
                            time.sleep(5)  # tempo para iniciar o download
                        except NoSuchElementException:
                            print("Não foi possível encontrar o botão de download.")
                    
                    except Exception as e:
                        print(f"Erro ao localizar elemento com o ID doc_{unique_id}: {e}")
                else:
                    print("Não foi possível extrair o ID da URL.")
            
            except Exception as e:
                print(f"Erro ao consultar o processo {processo}: {e}")

    # Fecha o navegador ao final das consultas
    driver.quit()

if __name__ == "__main__":
    consultar_processos("filtered_dataset.csv")

