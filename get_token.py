import requests

url = "http://4.224.186.213/evaluation-service/auth"

payload = {
    "email": "23BQ1A05B1@vvit.net",
    "name": "Kondapatur Indhu Naga Mani",
    "rollNo": "23BQ1A05B1",
    "accessCode": "QQdEYy",
    "clientID": "f99fe9b3-f26d-4b40-b867-a417d2c6467e",
    "clientSecret": "rsKDKRqJBKqxqBVx"
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")