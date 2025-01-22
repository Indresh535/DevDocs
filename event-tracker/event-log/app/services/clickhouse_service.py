import uuid
from datetime import datetime
from clickhouse_connect import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(host=os.getenv("CLICKHOUSE_URL").split("//")[1])

def insert_event(event_data):
    query = """
        INSERT INTO event_manager (event_id, event_type, event_name, event_value, 
                                   event_starttime, event_endtime, event_lat, 
                                   event_lang, user_browser, user_ip, user_os)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    client.execute(
        query,
        [
            str(uuid.uuid4()),  # Event ID
            event_data["event_type"],
            event_data["event_name"],
            event_data["event_value"],
            event_data["event_starttime"],
            event_data["event_endtime"],
            event_data["event_lat"],
            event_data["event_lang"],
            event_data["user_browser"],
            event_data["user_ip"],
            event_data["user_os"],
        ],
    )
