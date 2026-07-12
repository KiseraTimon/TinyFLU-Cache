# utilities/time_utils.py
from datetime import datetime

def timestp() -> str:
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def get_timestamp_id() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")