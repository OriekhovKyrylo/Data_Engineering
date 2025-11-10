"""
Read JSON files from disk
"""
import json
import os
from typing import List, Dict, Any


def read_json_from_disk(path: str) -> List[Dict[str, Any]]:
    """
    Read all JSON files from the specified directory
    """
    all_data = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory not found: {path}")

    # Find all JSON files in directory
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            file_path = os.path.join(path, filename)
            print(f"  Reading file: {filename}")

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # If it's a list - add all records
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)

    return all_data