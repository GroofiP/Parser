import json

import requests

APIKEY = "72546dWf3egSeQU0JHw4r0cTRCJ3nYJ8NdZBNuAtfZuiY9Cv7mSNpvrQ"

words = "Привет. Как твои дела?"

url = f"https://api.happi.dev/v1/language?text={words}&apikey={APIKEY}"
responce = requests.get(url)
data = responce.json()
with open('data_lang.json', 'w') as f:
    json.dump(data, f, indent=4)
language = data.get("langs")[0].get("name")
print(f"Это предложение написано на {language} языке ")
