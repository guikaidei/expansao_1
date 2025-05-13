inputs = ['tribunal','indicador','grau','UF','Órgão']

from Data.main import process_csv_and_execute
from WebScraper.main import runWebScraper
from Unzip.main import unzip
from Search.main import consultar_processos
from PDF.main import main as processar_pdfs

def main():
    runWebScraper()
    unzip()
    process_csv_and_execute()
    consultar_processos()
    processar_pdfs()

if __name__ == '__main__':
    main()
