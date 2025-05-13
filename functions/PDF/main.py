import os
import pandas as pd
from .utils import extrair_texto_pdf, extrair_dados_texto

def processar_pdfs():
    colunas = [
        "Número do processo",
        "Data de início do processo",
        "Data da decisão",
        "Nome do favorecido",
        "Nome da reclamada",
        "Órgão julgador",
        "Juiz (relator)",
        "Título judicial",
        "Cidade do processo originário",
        "Natureza do dano",
        "Honorários de sucumbência"
    ]

    df = pd.DataFrame(columns=colunas)
    
    # Caminho para a pasta search_downloads
    downloads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "search_downloads")
    
    # Verifica se a pasta existe
    if not os.path.exists(downloads_dir):
        print(f"Pasta {downloads_dir} não encontrada")
        return df
    
    # Cria a pasta extracted_csv se não existir
    extracted_csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "extracted_csv")
    if not os.path.exists(extracted_csv_dir):
        os.makedirs(extracted_csv_dir)
    
    # Lista todos os PDFs na pasta search_downloads
    lista_pdf = [arquivo for arquivo in os.listdir(downloads_dir) if arquivo.endswith(".pdf")]
    
    print(f"Encontrados {len(lista_pdf)} arquivos PDF para processar")
    
    for pdf in lista_pdf:
        pdf_path = os.path.join(downloads_dir, pdf)
        try:
            texto = extrair_texto_pdf(pdf_path)
            dados = extrair_dados_texto(texto)
            df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
            print(f"Processado: {pdf}")
        except Exception as e:
            print(f"Erro ao processar {pdf}: {str(e)}")
    
    # Salva o DataFrame em CSV
    csv_path = os.path.join(extracted_csv_dir, "dados_extraidos.csv")
    df.to_csv(csv_path, index=False, sep=";", encoding="latin-1")
    print(f"Dados salvos em: {csv_path}")
    
    return df

def main():
    print("Iniciando processamento de PDFs...")
    df = processar_pdfs()
    print(f"Processamento concluído. Total de {len(df)} processos extraídos.")
    return df

if __name__ == "__main__":
    main()