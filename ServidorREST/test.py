import requests

url = "http://127.0.0.1:5000/api/favorites"

payload={}
headers = {
  'Content-Type': 'application/x-protobuf'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)