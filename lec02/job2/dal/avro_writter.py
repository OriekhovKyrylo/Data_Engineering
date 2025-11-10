"""
Write data to Avro format
"""
import os
import shutil
from typing import List, Dict, Any
from fastavro import writer, parse_schema


def save_to_avro(data: List[Dict[str, Any]], path: str) -> None:
    """
    Save data to Avro format with idempotency (clear directory first)
    """
    # clear directory before writing
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    # extract date from directory name
    date = os.path.basename(path)
    file_name = f'sales_{date}.avro'
    file_path = os.path.join(path, file_name)


    schema = {
        'type': 'record',
        'name': 'Sales',
        'fields': [
            {'name': 'client', 'type': 'string'},
            {'name': 'purchase_date', 'type': 'string'},
            {'name': 'product', 'type': 'string'},
            {'name': 'price', 'type': 'int'},
        ]
    }

    parsed_schema = parse_schema(schema)

    #Write data to Avro

    with open(file_path, 'wb') as f:
        writer(f, parsed_schema, data)

    print(f"Avro data saved to {file_path}")