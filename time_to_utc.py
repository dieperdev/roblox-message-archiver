from datetime import datetime

def convert_timestamp_to_utc(timestamp: str) -> float | int:
    try:
        date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

    return date.timestamp()
