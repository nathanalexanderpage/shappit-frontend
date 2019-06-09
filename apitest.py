import requests

# resp = requests.get('https://api.github.com')
resp2 = requests.get('http://localhost:8000/customers/')
print(resp2.json())
