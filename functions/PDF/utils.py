import os
import fitz  # PyMuPDF
import re
import pandas as pd

def extrair_texto_pdf(arquivo_pdf):
    texto_completo = ""
    with fitz.open(arquivo_pdf) as doc:
        for pagina in doc:
            texto_completo += pagina.get_text("text") + "\n"
    return texto_completo

def extrair_dados_texto(texto):
    # 1) Número do processo
    match_num_processo = re.search(r"Número do processo:\s*([\d\.-]+)", texto)
    if not match_num_processo:
        match_num_processo = re.search(r"Ação Trabalhista - Rito Ordinário\s+([\d\.-]+)", texto)

    # 2) Data de início
    match_data_inicio = re.search(r"Data da Autuação:\s*([\d/]+)", texto)

    # 3) Data da decisão
    match_data_decisao = re.search(r"assinado eletronicamente por .* em\s*([\d/]+)", texto)

    # 4) Nome do favorecido (reclamante)
    match_reclamante = re.search(r"RECLAMANTE:\s*([A-Z\s]+)", texto)

    # 5) Nome(s) da reclamada
    match_reclamadas = re.findall(r"RECLAMAD[OA]:\s*([A-Z\s/\.\-]+)", texto)

    # 6) Órgão julgador
    match_orgao = re.search(r"(\d+ª VARA DO TRABALHO DE [A-Z\s]+)", texto)

    # 7) Juíza (relator)
    match_juiza = re.search(r"Juíza do Trabalho Titular\s+([A-Z\s]+)", texto)

    # 8) Título judicial
    titulo_judicial = "Sentença" if "S E N T E N Ç A" in texto else None

    # 9) Cidade do processo originário
    match_cidade = re.search(r"([A-Z]+/[A-Z]{2}),\s*\d{2}\s+de\s+\w+\s+de\s+\d{4}", texto)
    
    # 10) Honorários
    match_honorarios = re.search(r"fixo em\s*(\d+)%\s*sobre o valor da sucumbência", texto, re.IGNORECASE)

    dados_processados = {
        "Número do processo": match_num_processo.group(1) if match_num_processo else None,
        "Data de início do processo": match_data_inicio.group(1) if match_data_inicio else None,
        "Data da decisão": match_data_decisao.group(1) if match_data_decisao else None,
        "Nome do favorecido": match_reclamante.group(1).strip() if match_reclamante else None,
        "Nome da reclamada": "; ".join(match_reclamadas) if match_reclamadas else None,
        "Órgão julgador": match_orgao.group(1) if match_orgao else None,
        "Juiz (relator)": match_juiza.group(1).strip() if match_juiza else None,
        "Título judicial": titulo_judicial,
        "Cidade do processo originário": match_cidade.group(1) if match_cidade else None,
        "Natureza do dano": None,
        "Honorários de sucumbência": match_honorarios.group(1)+"%" if match_honorarios else None
    }
    return dados_processados