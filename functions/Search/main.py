import time
import os
import shutil
import re
import pandas as pd
from seleniumwire import webdriver  # Para capturar as requests (necessário para obter o áudio do captcha)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Search.captcha import *

def consultar_processos(csv_file='filtered_dataset.csv'):
    # Tenta ler o CSV
    try:
        filtered_dataset = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_file}' não foi encontrado.")
        return

    # Configurações do WebDriver (Selenium Wire para capturar as requests do áudio)
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    # Diretório de download
    download_dir = os.path.join(os.getcwd(), 'search_downloads')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Limpa a pasta de downloads antes de iniciar
    for file in os.listdir(download_dir):
        file_path = os.path.join(download_dir, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Erro ao excluir o arquivo {file_path}: {e}")

    # Preferências para download automático
    prefs = {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    }
    options.add_experimental_option('prefs', prefs)

    # Inicializa o driver
    driver = webdriver.Chrome(options=options)

    # Itera sobre cada processo do CSV
    for index, row in filtered_dataset.iterrows():
        tribunal = row['Tribunal']
        processo = row['Processo']

        print(f"\nIniciando consulta para o processo: {processo}")
        # Filtra apenas o TRT8
        if tribunal == 'TRT8':
            try:
                # Abre a página de consulta
                driver.get('https://pje.trt8.jus.br/consultaprocessual/')
                time.sleep(3)

                # Preenche o campo de busca
                input_field = driver.find_element(By.ID, 'nrProcessoInput')
                input_field.clear()
                input_field.send_keys(processo)
                input_field.send_keys(Keys.RETURN)
                time.sleep(10)
                print(f"Consulta realizada para o processo: {processo}")

                # Se a URL bater exatamente com 'detalhe-processo/<numero_processo>',
                # significa que há múltiplos graus (painel de escolha).
                current_url = driver.current_url
                print(f"URL atual: {current_url}")
                processo_limpo = re.sub(r'[.-]', '', processo)
                
                expected_multi_url = f"https://pje.trt8.jus.br/consultaprocessual/detalhe-processo/{processo_limpo}"
                print(expected_multi_url)
                if current_url == expected_multi_url:
                    print("Processo tem vários graus. Iniciando iteração sobre cada grau.")
                    try:
                        # Localiza o painel de escolha dos graus
                        div_painel = driver.find_element(By.ID, 'painel-escolha-processo')
                        botoes = div_painel.find_elements(By.CLASS_NAME, 'selecao-processo')
                        print(f"Quantidade de botões (graus) encontrados: {len(botoes)}")

                        # Para cada grau
                        for i in range(len(botoes)):
                            print(f"Clicando no botão de grau {i+1}")
                            botoes[i].click()
                            time.sleep(3)

                            # Em alguns casos, o captcha pode reaparecer
                            resolver_captcha(driver)


                            # Faz o download da sentença para este grau
                            download_sentenca(driver)
                            time.sleep(5)

                            # Se precisar voltar à tela anterior para escolher o próximo grau
                            # descomente a linha abaixo (depende de como o TRT8 funciona)
                            #
                            # driver.back()
                            # time.sleep(3)
                            # botoes = div_painel.find_elements(By.TAG_NAME, "button") 
                            # (reobter a lista de botões, caso seja necessário)
                    except Exception as e:
                        print(f"Erro ao iterar sobre os graus para o processo {processo}: {e}")
                else:
                    print("Processo tem apenas um grau. Prosseguindo para o download.")
                    # Caso de um único grau
                    download_sentenca(driver)
                    time.sleep(5)

            except Exception as e:
                print(f"Erro ao consultar o processo {processo}: {e}")

    driver.quit()


if __name__ == "__main__":
    consultar_processos("filtered_dataset.csv")
