import zipfile
import os
import shutil
import subprocess

def unzip():
    # Diretório onde estão os arquivos baixados
    download_dir = os.path.join(os.getcwd(), 'downloads')

    # Diretório de destino para arquivos extraídos
    extract_dir = os.path.join(os.getcwd(), 'extracted_csv')

    # Limpar a pasta extract_dir antes de descompactar
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)  # Remove todos os arquivos e subpastas em extract_dir
    os.makedirs(extract_dir, exist_ok=True)  # Cria a pasta novamente, caso tenha sido removida

    # Iterar sobre todos os arquivos .zip na pasta de downloads
    for file in os.listdir(download_dir):
        if file.endswith(".zip"):
            file_path = os.path.join(download_dir, file)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    # Verificar se o arquivo é um .csv antes de extrair
                    if member.endswith(".csv"):
                        zip_ref.extract(member, extract_dir)
                        print(f"Arquivo '{member}' extraído com sucesso em '{extract_dir}'.")

    print("Todos os arquivos .zip foram descompactados e arquivos .csv extraídos com sucesso.")
