import zipfile
import os
import shutil
import subprocess

def unzip(download_dir=None, extract_dir=None):
    """
    Descompacta arquivos .zip do diretório de downloads, extraindo apenas os arquivos .csv para
    o diretório especificado e, em seguida, executa o arquivo Data.py.
    
    Parâmetros:
        download_dir (str): Caminho para o diretório onde os arquivos .zip estão localizados.
                            Se None, usa a pasta 'downloads' no diretório atual.
        extract_dir (str): Caminho para o diretório onde os arquivos .csv serão extraídos.
                           Se None, usa a pasta 'extracted_csv' no diretório atual.
    """
    # Define os diretórios padrão, se não fornecidos
    if download_dir is None:
        download_dir = os.path.join(os.getcwd(), 'downloads')
    if extract_dir is None:
        extract_dir = os.path.join(os.getcwd(), 'extracted_csv')
    
    # Limpar a pasta extract_dir antes de descompactar
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)
    
    # Iterar sobre todos os arquivos .zip na pasta de downloads
    for file in os.listdir(download_dir):
        if file.endswith(".zip"):
            file_path = os.path.join(download_dir, file)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    # Verifica se o arquivo é um .csv antes de extrair
                    if member.endswith(".csv"):
                        zip_ref.extract(member, extract_dir)
                        print(f"Arquivo '{member}' extraído com sucesso em '{extract_dir}'.")
    
    print("Todos os arquivos .zip foram descompactados e arquivos .csv extraídos com sucesso.")
    
if __name__ == '__main__':
    unzip()