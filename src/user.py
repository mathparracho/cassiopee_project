import requests
import base64

with open("bumbum.png", "rb") as img:
    string = base64.b64encode(img.read()).decode('utf-8')

api_url = "http://localhost:8000/photo"
response = requests.post(url= api_url, json={'photo':string})

