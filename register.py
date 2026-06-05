import requests

url = "http://4.224.186.213/evaluation-service/register"

payload = {
    "email": "23BQ1A05B1@vvit.net",
    "name": "Kondapatur Indhu Naga Mani",
    "rollNo": "23BQ1A05B1",
    "accessCode": "QQdEYy",
    "mobileNo": "7842322191",
    "githubUsername": "KIndhu06"
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")