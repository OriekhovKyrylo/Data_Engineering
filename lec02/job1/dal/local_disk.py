"""
Data access layer for saving JSON to local disk
"""
import json
import os
import shutil
from typing import List, Dict, Any


def save_to_disk(json_content: List[Dict[str, Any]], path: str) -> None:
    """
    Save JSON content to disk with idempotency.

    :param json_content: List of records to save
    :param path: Directory path where to save the file
    """
    date: str = os.path.basename(path)
    file_name: str = f'sales_{date}.json'

    # Idempotency: clear directory before writing
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    file_path: str = os.path.join(path, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)

    print(f"Sales data saved to {file_path}")