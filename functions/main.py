inputs = ['tribunal','indicador','grau','UF','Órgão']

from Data.main import process_csv_and_execute
from WebScraper.main import runWebScraper
from Unzip.main import unzip

def main():
    runWebScraper()
    unzip()
    process_csv_and_execute()

if __name__ == '__main__':
    main()
