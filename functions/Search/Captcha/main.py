import whisper
import base64
import re
import os

def audio_to_text(audio_base64):
    # Decodificando o audio base64
    audio_bytes = base64.b64decode(audio_base64)

    with open("temp_audio/download.wav", "wb") as file:
        file.write(audio_bytes)

    # Carregando o modelo de reconhecimento de voz
    model = whisper.load_model("turbo")
    result = model.transcribe("temp_audio/download.wav")

    print(result["text"])

    captcha_text = re.findall(r'\b[A-Z]\b|\d+', result["text"])

    #deletando o arquivo de audio da pasta temp_audio
    os.remove("temp_audio/download.wav")

    return captcha_text
