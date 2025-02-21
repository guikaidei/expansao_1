import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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
