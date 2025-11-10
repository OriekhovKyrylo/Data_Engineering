from lec02.job1.dal import local_disk, sales_api



def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    # TODO: implement me
    print(f"Fetching sales data for date: {date}")
    sales_data = sales_api.get_sales(date=date)
    print(f"Received {len(sales_data)} records")


    # 2. save data to disk
    print(f"Saving data to: {raw_dir}")
    local_disk.save_to_disk(sales_data,raw_dir)
    print("\tI'm in get_sales(...) function!")
