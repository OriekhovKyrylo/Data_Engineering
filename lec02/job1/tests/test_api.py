import requests
import os

# Встановіть токен
os.environ['AUTH_TOKEN'] = '2b8d97ce57d401abd89f45b0079d8790edd940e6'

AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
print(f"Token: {AUTH_TOKEN}")

# Тест 1: Без префіксу
print("\n=== Test 1: Without prefix ===")
response = requests.get(
    'https://fake-api-vycpfa6oca-uc.a.run.app/sales',
    headers={'Authorization': AUTH_TOKEN},
    params={'date': '2022-08-09', 'page': 1}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Тест 2: З префіксом Bearer
print("\n=== Test 2: With Bearer prefix ===")
response = requests.get(
    'https://fake-api-vycpfa6oca-uc.a.run.app/sales',
    headers={'Authorization': f'Bearer {AUTH_TOKEN}'},
    params={'date': '2022-08-09', 'page': 1}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Тест 3: Як параметр запиту
print("\n=== Test 3: As query parameter ===")
response = requests.get(
    'https://fake-api-vycpfa6oca-uc.a.run.app/sales',
    params={'date': '2022-08-09', 'page': 1, 'token': AUTH_TOKEN}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Тест 4: Інший заголовок
print("\n=== Test 4: X-API-Token header ===")
response = requests.get(
    'https://fake-api-vycpfa6oca-uc.a.run.app/sales',
    headers={'X-API-Token': AUTH_TOKEN},
    params={'date': '2022-08-09', 'page': 1}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")