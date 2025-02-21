import os
import fitz  # PyMuPDF
import re
import pandas as pd

def extrair_texto_pdf(arquivo_pdf):
    """
    Lê um arquivo PDF e retorna todo o texto concatenado.
    """
    texto_completo = ""
    with fitz.open(arquivo_pdf) as doc:
        for pagina in doc:
            texto_completo += pagina.get_text("text") + "\n"
    return texto_completo

def extrair_dados_texto(texto):
    """
    Extrai dados específicos do texto usando expressões regulares
    compatíveis com o conteúdo real do PDF.
    """
    # 1) Número do processo -> aparece como "Número do processo: 0000630-03.2024.5.08.0120"
    #    ou no final do PDF, ou "Ação Trabalhista - Rito Ordinário 0000630-03.2024.5.08.0120"
    #    Aqui optamos pelo que aparece no rodapé: "Número do processo: 0000630-03.2024.5.08.0120"
    match_num_processo = re.search(r"Número do processo:\s*([\d\.-]+)", texto)
    if not match_num_processo:
        # Se não achou, tenta capturar logo após "Ação Trabalhista - Rito Ordinário"
        match_num_processo = re.search(r"Ação Trabalhista - Rito Ordinário\s+([\d\.-]+)", texto)

    # 2) Data de início -> no texto: "Data da Autuação: 07/06/2024"
    match_data_inicio = re.search(r"Data da Autuação:\s*([\d/]+)", texto)

    # 3) Data da decisão -> "Documento assinado eletronicamente por ... em 30/12/2024"
    match_data_decisao = re.search(r"assinado eletronicamente por .* em\s*([\d/]+)", texto)

    # 4) Nome do favorecido (reclamante) -> "RECLAMANTE: ERNANDES BARRAL CAIANA"
    match_reclamante = re.search(r"RECLAMANTE:\s*([A-Z\s]+)", texto)

    # 5) Nome(s) da reclamada -> texto tem "RECLAMADO: BELEM BIOENERGIA..." e "RECLAMADO: TAUA..."
    #    Então vamos achar *todos* os RECLAMADO: e juntar em um campo só
    match_reclamadas = re.findall(r"RECLAMAD[OA]:\s*([A-Z\s/\.\-]+)", texto)

    # 6) Órgão julgador -> no seu PDF aparece "2ª VARA DO TRABALHO DE ANANINDEUA"
    #    então podemos tentar capturar essa frase:
    match_orgao = re.search(r"(\d+ª VARA DO TRABALHO DE [A-Z\s]+)", texto)

    # 7) Juíza (relator) -> o PDF mostra "Juíza do Trabalho Titular\nRENATA PLATON ANJOS"
    match_juiza = re.search(r"Juíza do Trabalho Titular\s+([A-Z\s]+)", texto)

    # 8) Título judicial -> no texto há "S E N T E N Ç A". Se ela estiver presente, consideramos Sentença
    titulo_judicial = "Sentença" if "S E N T E N Ç A" in texto else None

    # 9) Cidade do processo originário -> ao final: "ANANINDEUA/PA, 30 de dezembro de 2024."
    #    Podemos capturar "ANANINDEUA/PA" usando regex:
    match_cidade = re.search(r"([A-Z]+/[A-Z]{2}),\s*\d{2}\s+de\s+\w+\s+de\s+\d{4}", texto)
    # 10) Honorários -> há trecho "fixo em 10% sobre o valor da sucumbência"
    #    Podemos fazer:
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
        # Se você quiser "Natureza do dano", teria de buscar algo que realmente exista no texto
        "Natureza do dano": None,
        # Ajuste se o texto contiver algo como "honorários de sucumbência" 
        "Honorários de sucumbência": match_honorarios.group(1)+"%" if match_honorarios else None
    }
    return dados_processados


# ---- Abaixo, seu fluxo principal para montar o DataFrame ----

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cria a lista de PDFs (todos os .pdf do diretório)
lista_pdf = [arquivo for arquivo in os.listdir(BASE_DIR) if arquivo.endswith(".pdf")]

for pdf in lista_pdf:
    pdf_path = os.path.join(BASE_DIR, pdf)
    texto = extrair_texto_pdf(pdf_path)
    
    # Mostra o texto só para debug (opcional)
    print(f"\n=== TEXTO DE {pdf} ===")
    print(texto)
    
    dados = extrair_dados_texto(texto)
    df = df._append(dados, ignore_index=True)

# Salva em CSV
df.to_csv("dados_extraidos.csv", index=False, sep=";", encoding="latin-1")
print("\n=== DataFrame final ===")
print(df)
