"""
Business logic for converting JSON to Avro
"""
from lec02.job2.dal import local_disk, avro_writter


def convert_raw_to_stg(raw_dir: str, stg_dir: str) -> None:
    """
    Read JSON from raw_dir and write Avro to stg_dir
    """
    print(f"Reading JSON from: {raw_dir}")
    sales_data = local_disk.read_json_from_disk(raw_dir)
    print(f"Loaded {len(sales_data)} records")

    print(f"Writing Avro to: {stg_dir}")
    avro_writter.save_to_avro(sales_data, stg_dir)
    print("Conversion completed!")