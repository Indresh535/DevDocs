from fastapi import APIRouter, BackgroundTasks, Request
from app.services.clickhouse_service import insert_event
from datetime import datetime

router = APIRouter()

@router.post("/log")
async def log_event(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    event_data = {
        "event_type": body["event_type"],
        "event_name": body["event_name"],
        "event_value": body["event_value"],
        "event_starttime": body.get("event_starttime", datetime.now()),
        "event_endtime": body.get("event_endtime", datetime.now()),
        "event_lat": body["event_lat"],
        "event_lang": body["event_lang"],
        "user_browser": body["user_browser"],
        "user_ip": request.client.host,
        "user_os": body["user_os"],
    }
    background_tasks.add_task(insert_event, event_data)
    return {"status": "success", "event_id": event_data["event_type"]}
