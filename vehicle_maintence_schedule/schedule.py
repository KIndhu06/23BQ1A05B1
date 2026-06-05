import requests

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyM2JxMWEwNWIxQHZ2aXQubmV0IiwiZXhwIjoxNzgwNjQwNjI5LCJpYXQiOjE3ODA2Mzk3MjksImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiI2MDMyODZmYS1lNzViLTQ3ODYtOGE0OS05MDRkZDBiMTNlYTciLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJrb25kYXBhdHVyIGluZGh1IG5hZ2EgbWFuaSIsInN1YiI6ImY5OWZlOWIzLWYyNmQtNGI0MC1iODY3LWE0MTdkMmM2NDY3ZSJ9LCJlbWFpbCI6IjIzYnExYTA1YjFAdnZpdC5uZXQiLCJuYW1lIjoia29uZGFwYXR1ciBpbmRodSBuYWdhIG1hbmkiLCJyb2xsTm8iOiIyM2JxMWEwNWIxIiwiYWNjZXNzQ29kZSI6IlFRZEVZeSIsImNsaWVudElEIjoiZjk5ZmU5YjMtZjI2ZC00YjQwLWI4NjctYTQxN2QyYzY0NjdlIiwiY2xpZW50U2VjcmV0IjoicnNLREtScUpCS3F4cUJWeCJ9.CFU3UYxlCX8dlFbwmgoCo8GaEmHMle5DE0XrHPCvyoY"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_depots():
    url = "http://4.224.186.213/evaluation-service/depots"
    response = requests.get(url, headers=headers)
    print(f"Depots status: {response.status_code}")
    print(f"Depots raw: {response.text[:200]}")
    return response.json()

def get_vehicles():
    url = "http://4.224.186.213/evaluation-service/vehicles"
    response = requests.get(url, headers=headers)
    print(f"Vehicles status: {response.status_code}")
    print(f"Vehicles raw: {response.text[:200]}")
    return response.json()

def knapsack(vehicles, max_hours):
    n = len(vehicles)
    dp = [[0] * (max_hours + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        duration = vehicles[i-1]["Duration"]
        impact = vehicles[i-1]["Impact"]
        for w in range(max_hours + 1):
            dp[i][w] = dp[i-1][w]
            if duration <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-duration] + impact)

    selected = []
    w = max_hours
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(vehicles[i-1])
            w -= vehicles[i-1]["Duration"]

    return dp[n][max_hours], selected

def main():
    print("Fetching depots and vehicles...\n")
    
    depots_data = get_depots()
    vehicles_data = get_vehicles()
    
    depots = depots_data.get("depots", [])
    vehicles = vehicles_data.get("vehicles", [])

    print(f"\nTotal Depots  : {len(depots)}")
    print(f"Total Vehicles: {len(vehicles)}\n")

    for depot in depots:
        depot_id = depot["ID"]
        max_hours = depot["MechanicHours"]

        best_score, selected = knapsack(vehicles, max_hours)

        print(f"Depot {depot_id} — Mechanic Hours: {max_hours}")
        print(f"Max Impact Score : {best_score}")
        print(f"Vehicles Selected: {len(selected)}")
        for v in selected:
            print(f"   TaskID: {v['TaskID']} | Duration: {v['Duration']}h | Impact: {v['Impact']}")
        print()

if __name__ == "__main__":
    main()