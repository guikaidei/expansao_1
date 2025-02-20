import os
import pandas as pd

def process_csv_and_execute(extract_dir=None, output_file='filtered_dataset.csv'):
    """
    Processa e concatena arquivos CSV de um diretório, filtra as linhas que contêm o código 14012 
    na coluna 'Codigos_assuntos', seleciona as colunas 'Tribunal', 'Data_de_Referencia' e 'Processo', 
    e salva o DataFrame resultante em um arquivo CSV.

    Parâmetros:
        extract_dir (str): Diretório onde os arquivos CSV extraídos estão armazenados.
                           Se None, utiliza o diretório 'extracted_csv' no diretório atual.
        output_file (str): Caminho/nome do arquivo CSV de saída. Padrão é 'filtered_dataset.csv'.

    Retorna:
        DataFrame: O DataFrame filtrado, caso os arquivos com a estrutura esperada sejam encontrados;
                   caso contrário, retorna None.
    """
    if extract_dir is None:
        extract_dir = os.path.join(os.getcwd(), 'extracted_csv')
    
    # Lista para armazenar os DataFrames de cada arquivo CSV
    dataframes = []
    
    # Iterar sobre todos os arquivos CSV no diretório
    for file in os.listdir(extract_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(extract_dir, file)
            try:
                # Tenta ler o arquivo CSV com encoding 'latin1' e ignora linhas com problemas
                df = pd.read_csv(file_path, delimiter=';', encoding='latin1', on_bad_lines="skip")
                
                # Verifica se as colunas necessárias estão presentes
                if 'Data_de_Referencia' in df.columns and 'Codigos_assuntos' in df.columns:
                    dataframes.append(df)
                else:
                    print(f"Arquivo {file_path} ignorado: colunas necessárias ausentes.")
            except pd.errors.ParserError:
                print(f"Erro ao ler o arquivo: {file_path}. O arquivo foi ignorado.")
                continue

    # Se houver arquivos válidos, concatena e processa os dados
    if dataframes:
        # Concatenar todos os DataFrames em um único DataFrame
        dataset = pd.concat(dataframes, ignore_index=True)

        # Converter a coluna 'Data_de_Referencia' para datetime e ordenar do mais novo para o mais antigo
        dataset['Data_de_Referencia'] = pd.to_datetime(dataset['Data_de_Referencia'], errors='coerce')
        dataset = dataset.sort_values(by='Data_de_Referencia', ascending=False)

        # Filtrar as linhas onde 'Codigos_assuntos' contém o código 14012
        filtered_dataset = dataset[dataset['Codigos_assuntos'].astype(str).str.contains('14012', na=False)]

        # Selecionar apenas as colunas desejadas
        filtered_dataset = filtered_dataset[['Tribunal', 'Data_de_Referencia', 'Processo']]

        # Exibir e salvar o DataFrame filtrado
        print(filtered_dataset)
        filtered_dataset.to_csv(output_file, index=False)
        print(f"DataFrame filtrado salvo em '{output_file}'.")
        return filtered_dataset
    else:
        print("Nenhum arquivo com a estrutura esperada foi encontrado.")
        return None

if __name__ == '__main__':
    process_csv_and_execute()   