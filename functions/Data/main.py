import os
import pandas as pd
import subprocess

def process_csv_and_execute():
    """
    Esta função realiza os seguintes passos:
    1. Percorre o diretório 'extracted_csv' para carregar os arquivos CSV.
    2. Concatena os DataFrames com as colunas necessárias.
    3. Ordena e filtra os dados de acordo com os critérios definidos.
    4. Salva o DataFrame filtrado em um arquivo CSV.
    5. Executa o arquivo 'Search.py' usando subprocess.
    """
    # Diretório onde os arquivos CSV extraídos estão armazenados
    extract_dir = os.path.join(os.getcwd(), 'extracted_csv')

    # Lista para armazenar todos os DataFrames de cada arquivo CSV
    dataframes = []

    # Carregar e concatenar todos os arquivos CSV em um único DataFrame
    for file in os.listdir(extract_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(extract_dir, file)
            
            try:
                # Tenta ler o arquivo CSV com encoding 'latin1' e ignora linhas com problemas
                df = pd.read_csv(file_path, delimiter=';', encoding='latin1', on_bad_lines="skip")
                
                # Verifica se as colunas necessárias estão no arquivo
                if 'Data_de_Referencia' in df.columns and 'Codigos_assuntos' in df.columns:
                    dataframes.append(df)
                else:
                    print(f"Arquivo {file_path} ignorado: colunas necessárias ausentes.")
            except pd.errors.ParserError:
                print(f"Erro ao ler o arquivo: {file_path}. O arquivo foi ignorado.")
                continue

    # Verifica se há dados concatenados
    if dataframes:
        # Concatenar todos os DataFrames em um único DataFrame
        dataset = pd.concat(dataframes, ignore_index=True)

        # Ordenar o DataFrame pela coluna 'Data_de_Referencia' do mais novo para o mais velho
        # Convertendo a coluna para datetime para garantir a ordenação correta
        dataset['Data_de_Referencia'] = pd.to_datetime(dataset['Data_de_Referencia'], errors='coerce')
        dataset = dataset.sort_values(by='Data_de_Referencia', ascending=False)

        # Filtrar as linhas onde a coluna 'Codigos_assuntos' contém o código 14012
        filtered_dataset = dataset[dataset['Codigos_assuntos'].astype(str).str.contains('14012', na=False)]

        # Selecionar apenas as colunas 'Tribunal', 'Data_de_Referencia' e 'Processo'
        filtered_dataset = filtered_dataset[['Tribunal', 'Data_de_Referencia', 'Processo']]

        # Exibir o DataFrame filtrado e com as colunas selecionadas
        print(filtered_dataset)

        # Salvar o DataFrame filtrado como um arquivo CSV
        filtered_dataset.to_csv('filtered_dataset.csv', index=False)
    else:
        print("Nenhum arquivo com a estrutura esperada foi encontrado.")

    # Executar o arquivo Search.py em sequência
    try:
        subprocess.run(['python', 'Search.py'], check=True)
        print("Search.py executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar Search.py: {e}")

if __name__ == '__main__':
    process_csv_and_execute()
