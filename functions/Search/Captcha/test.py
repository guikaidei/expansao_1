import whisper
import requests
import json
import base64

processo = 782471

url = f"https://pje.trt8.jus.br/pje-consulta-api/api/captcha?idProcesso={processo}&audio=true"

response = requests.get(url)

data = json.loads(response.content.decode("utf-8"))

print(data['audio'][0:10])

audio_base64 = data['audio']

audio_bytes = base64.b64decode(audio_base64)

with open("temp_audio/download.wav", "wb") as file:
    file.write(audio_bytes)

model = whisper.load_model("turbo")
result = model.transcribe("download.wav")
print(result["text"])

