
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Cloud-Managed Security Device Lab",
    description="A local simulation of device health monitoring.",
    version="1.0.0",
)

HEARTBEAT_TIMEOUT_SECONDS = 30

class Heartbeat(BaseModel):
    device_id: str
    status: str = "online"

devices = {}


@app.get("/")
def home():
    return {
        "project": "Cloud-Managed Security Device Lab",
        "message": "Cloud controller is running",
    }


@app.post("/heartbeat")
def receive_heartbeat(heartbeat: Heartbeat):
    received_at = datetime.now(timezone.utc)

    devices[heartbeat.device_id] = {
        "reported_status": heartbeat.status,
        "last_seen": received_at,
    }

    return {
        "message": "Heartbeat received",
        "device_id": heartbeat.device_id,
        "status": heartbeat.status,
        "last_seen": received_at.isoformat(),
    }


@app.get("/devices")
def list_devices():
    now = datetime.now(timezone.utc)
    device_list = {}

    for device_id, device in devices.items():
        seconds_since_heartbeat = (
            now - device["last_seen"]
        ).total_seconds()

        if seconds_since_heartbeat > HEARTBEAT_TIMEOUT_SECONDS:
            current_status = "offline"
        else:
            current_status = device["reported_status"]

        device_list[device_id] = {
            "status": current_status,
            "last_seen": device["last_seen"].isoformat(),
            "seconds_since_heartbeat": round(
                seconds_since_heartbeat, 1
            ),
        }

    return {"devices": device_list}
