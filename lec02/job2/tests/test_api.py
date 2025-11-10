import requests

response = requests.post(
    'http://localhost:8082/',
    json={
        'raw_dir': 'E:/test_data/raw/sales/2022-08-09',
        'stg_dir': 'E:/test_data/stg/sales/2022-08-09'
    }
)

print(response.status_code)
print(response.json())