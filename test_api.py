import requests

url = "http://127.0.0.1:5000/get_form"
data = {
    "email": "test@example.com",
    "phone_number": "+7 123 456 78 90"
}

response = requests.post(url, data=data)
print(response.json())
