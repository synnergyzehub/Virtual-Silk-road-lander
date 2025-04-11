
import requests

url = "http://localhost:5000/api/license/assign"
data = {
    "node": "Emperor: Tailoring Node",
    "licenseId": "EMP-TLR-0142",
    "assignedTo": "atelier@emperor.com",
    "role": "Designer",
    "moduleScope": "Tailoring"
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
