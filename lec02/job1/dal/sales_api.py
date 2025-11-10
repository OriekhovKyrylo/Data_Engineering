import os
from typing import List, Dict, Any
import requests

API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'


def get_sales(date: str) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param date: date to retrieve the data from
    :return: list of records
    """
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

    if not AUTH_TOKEN:
        raise ValueError("AUTH_TOKEN environment variable is not set")

    all_data = []
    page = 1

    while True:
        print(f"  Requesting page {page}...")  # Діагностика

        response = requests.get(
            API_URL,
            headers={"Authorization": AUTH_TOKEN},
            params={"date": date, "page": page}
        )

        # Перевіряємо статус код
        print(f"  Status code: {response.status_code}")

        # Якщо помилка - виходимо
        if response.status_code != 200:
            print(f"  ERROR: {response.text}")
            break

        data = response.json()
        print(f"  Received: {len(data) if isinstance(data, list) else 'not a list'} records")

        # Перевіряємо чи це список і чи він не пустий
        if not isinstance(data, list) or len(data) == 0:
            print("  No more data, stopping.")
            break

        all_data.extend(data)
        page += 1

        # Запобіжник від нескінченного циклу (максимум 1000 сторінок)
        if page > 1000:
            print("  WARNING: Reached page limit 1000, stopping.")
            break

    print(f"  Total records fetched: {len(all_data)}")
    return all_data