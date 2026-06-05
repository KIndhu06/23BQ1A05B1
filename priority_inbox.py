import requests
from datetime import datetime

# Your credentials
CLIENT_ID = "f99fe9b3-f26d-4b40-b867-a417d2c6467e"
CLIENT_SECRET = "rsKDKRqJBKqxqBVx"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyM2JxMWEwNWIxQHZ2aXQubmV0IiwiZXhwIjoxNzgwNjM4MTYwLCJpYXQiOjE3ODA2MzcyNjAsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiI0NjhiOTRlYi1lYjBkLTRiNDUtYjY1OC0zMTgwYzAyMjdhODYiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJrb25kYXBhdHVyIGluZGh1IG5hZ2EgbWFuaSIsInN1YiI6ImY5OWZlOWIzLWYyNmQtNGI0MC1iODY3LWE0MTdkMmM2NDY3ZSJ9LCJlbWFpbCI6IjIzYnExYTA1YjFAdnZpdC5uZXQiLCJuYW1lIjoia29uZGFwYXR1ciBpbmRodSBuYWdhIG1hbmkiLCJyb2xsTm8iOiIyM2JxMWEwNWIxIiwiYWNjZXNzQ29kZSI6IlFRZEVZeSIsImNsaWVudElEIjoiZjk5ZmU5YjMtZjI2ZC00YjQwLWI4NjctYTQxN2QyYzY0NjdlIiwiY2xpZW50U2VjcmV0IjoicnNLREtScUpCS3F4cUJWeCJ9.bWTZwP9xDMxLXToXXQFdYWiBZ9uyFdI194fM9rsOieY"

# Priority weights
WEIGHTS = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

def get_priority_score(notification):
    type_weight = WEIGHTS.get(notification["Type"], 0)
    timestamp = datetime.strptime(notification["Timestamp"], "%Y-%m-%d %H:%M:%S")
    now = datetime.utcnow()
    hours_old = (now - timestamp).total_seconds() / 3600
    recency_score = max(0, 100 - hours_old)
    return (type_weight * 50) + recency_score

def get_top_notifications(n=10):
    url = "http://4.224.186.213/evaluation-service/notifications"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    
    data = response.json()
    notifications = data["notifications"]
    print(f"Total fetched: {len(notifications)}")
    
    # Score each
    for notif in notifications:
        notif["score"] = get_priority_score(notif)
    
    # Sort highest first
    sorted_notifications = sorted(
        notifications,
        key=lambda x: x["score"],
        reverse=True
    )
    
    return sorted_notifications[:n]

def display_notifications(notifications):
    print("\n===== TOP 10 PRIORITY NOTIFICATIONS =====\n")
    for i, notif in enumerate(notifications, 1):
        print(f"{i}. [{notif['Type']}] {notif['Message']}")
        print(f"   Timestamp     : {notif['Timestamp']}")
        print(f"   Priority Score: {round(notif['score'], 2)}")
        print(f"   ID            : {notif['ID']}")
        print()

if __name__ == "__main__":
    top = get_top_notifications(10)
    display_notifications(top)