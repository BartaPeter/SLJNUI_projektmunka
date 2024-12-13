import sqlite3
import pandas as pd

def convert_time_to_seconds(time_str):

    try:
        if isinstance(time_str, str):
            parts = time_str.split(":")
            if len(parts) == 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])
            elif len(parts) == 2:
                hours = 0
                minutes = int(parts[0])
                seconds = float(parts[1])
            else:
                return None
            return hours * 3600 + minutes * 60 + seconds
        return None
    except Exception as e:
        return None

def load_data(database_path):
    conn = sqlite3.connect(database_path)
    query = """
        SELECT
            Age,
            Weight,
            Height,
            Gender,
            Physical_History,
            Sleep_Duration,
            Distance,
            Calories,
            Time
        FROM running_data
    """
    data = pd.read_sql_query(query, conn)
    data['Time'] = data['Time'].apply(convert_time_to_seconds)
    data = data[(data['Distance'] > 0) & (data['Time'] > 0)]
    
    conn.close()
    return data
