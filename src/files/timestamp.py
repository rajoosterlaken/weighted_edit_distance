from datetime import datetime

def generate_timestamp(timestamp_format="{0:04} {1:02} {2:02} {3:02} {4:02} {5:02}"):
    """
    Generates a timestamp for the second this method was called.
    Returns as a string of the given format.
    """
    time = datetime.now()
    data = (time.year, time.month, time.day, time.hour, time.minute, time.second)
    return timestamp_format.format(*data) if timestamp_format else time