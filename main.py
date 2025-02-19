inputs = ['tribunal','indicador','grau','UF','Órgão']

from functions.Data.main import process_csv_and_execute
from functions.WebScraper.main import runWebScraper

def main():
    runWebScraper()
    process_csv_and_execute()