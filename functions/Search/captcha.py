import whisper
import base64
import re
import os
import json 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def audio_to_text(audio_base64):
    # Ensure the temp_audio directory exists
    os.makedirs("temp_audio", exist_ok=True)
    
    # Decode the base64 audio
    audio_bytes = base64.b64decode(audio_base64)
    
    # Save the audio to a file
    with open("temp_audio/download.wav", "wb") as file:
        file.write(audio_bytes)
    
    # Load the Whisper model and transcribe the audio
    model = whisper.load_model("turbo")
    result = model.transcribe("temp_audio/download.wav")
    
    print(result["text"])
    
    # Extract alphanumeric characters for the captcha
    captcha_text = re.findall(r'\b[A-Z]\b|\d+', result["text"])
    
    # Delete the temporary audio file
    os.remove("temp_audio/download.wav")
    
    return captcha_text

def download_sentenca(driver):
    """
    Faz o download da sentença, identificando o ID único após o '#' na URL.
    Em seguida, localiza o botão de download e o aciona.
    """
    current_url = driver.current_url
    print(f"URL atual: {current_url}")

    if '#' in current_url:
        unique_id = current_url.split('#')[-1]  # Pega tudo após o '#'
    else:
        print("URL não contém '#'. Não é possível extrair o ID.")
        unique_id = None

    if unique_id:
        try:
            # Clica no "cartão" que contém o documento
            xpath = f"//*[@id='doc_{unique_id}']/div"
            elemento = driver.find_element(By.XPATH, xpath)
            elemento.click()
            print("Elemento encontrado e clicado com sucesso!")
            time.sleep(3)
            try:
                # Localiza e clica no botão de download
                botao_download = driver.find_element(By.XPATH, "//*[@id='botoes-documento2']/button/span/i")
                botao_download.click()
                print("Download solicitado com sucesso!")
                time.sleep(5)  # Tempo para iniciar o download
            except NoSuchElementException:
                print("Não foi possível encontrar o botão de download.")
        except Exception as e:
            print(f"Erro ao localizar elemento com o ID doc_{unique_id}: {e}")
    else:
        print("Não foi possível extrair o ID da URL.")


def resolver_captcha(driver):
    """
    Tenta resolver o captcha utilizando o áudio.
    Espera pelos botões (áudio/recarregar), obtém o áudio via requests,
    converte para texto e envia a resposta.
    """
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'btnCarregarAudio'))
        )
    except:
        print("Botão de áudio do captcha não encontrado; possivelmente já está resolvido.")

    bypass_captcha = False
    while not bypass_captcha:
        time.sleep(2)
        print("Checando se o captcha foi resolvido...")
        captcha_audio_button = driver.find_elements(By.ID, 'btnCarregarAudio')
        reload_button = driver.find_elements(By.ID, 'btnRecarregar')
        print(f"captcha_audio_button: {captcha_audio_button}, reload_button: {reload_button}")
        time.sleep(2)

        if reload_button or captcha_audio_button:
            print("Captcha não resolvido. Tentando novamente...")
            if reload_button:
                reload_button[0].click()
            elif captcha_audio_button:
                captcha_audio_button[0].click()
            time.sleep(2)

            response = None
            requests = driver.requests
            requests.reverse()
            # Procura pela request que contenha "audio" na URL
            for request in requests:
                if "audio" in request.url and request.response:
                    print(f"URL de áudio: {request.url}")
                    print(f"Status Code: {request.response.status_code}")
                    response = request.response.body
                    break
            

            if response is None:
                print("Nenhuma resposta de áudio encontrada.")
                continue

            try:
                data = json.loads(response.decode("utf-8"))
            except Exception as e:
                print(f"Erro ao decodificar resposta de áudio: {e}")
                continue

            audio_base64 = data.get('audio')
            if not audio_base64:
                print("Áudio não encontrado na resposta JSON.")
                continue

            # Converte o áudio para texto e formata
            captcha_text = audio_to_text(audio_base64)
            captcha_text = ''.join(captcha_text).lower()
            print(f"Texto do captcha: {captcha_text}")

            try:
                captcha_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'captchaInput'))
                )
                captcha_input.clear()
                captcha_input.send_keys(captcha_text)
                print("Texto do captcha preenchido.")
                time.sleep(5)
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'btnEnviar'))
                )
                submit_button.click()
                print("Botão de enviar captcha clicado.")
            except Exception as e:
                print(f"Erro ao enviar captcha: {e}")
        else:
            print("Captcha resolvido com sucesso.")
            bypass_captcha = True
