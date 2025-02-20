import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
                # Localiza o campo de entrada do número do processo
                input_field = driver.find_element(By.XPATH, '//*[@id="nrProcessoInput"]')
                input_field.clear()
                input_field.send_keys(processo)
                input_field.send_keys(Keys.RETURN)
                
                print(f"Consulta realizada para o processo: {processo}")
                time.sleep(15)  # Aguarda o carregamento dos resultados
            except Exception as e:
                print(f"Erro ao consultar o processo {processo}: {e}")

    # Fecha o navegador ao final das consultas
    driver.quit()
