import requests

response = requests.post(
    'http://localhost:8081/',
    json={
        'date': '2022-08-09',
        'raw_dir': 'E:/test_data/raw/sales/2022-08-09'
    }
)

print(response.status_code)
print(response.json())
