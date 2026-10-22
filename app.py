
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Cloud-Managed Security Device Lab",
    description="A local simulation of device health monitoring.",
    version="1.0.0",
)


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
    received_at = datetime.now(timezone.utc).isoformat()

    devices[heartbeat.device_id] = {
        "status": heartbeat.status,
        "last_seen": received_at,
    }

    return {
        "message": "Heartbeat received",
        "device_id": heartbeat.device_id,
        "status": heartbeat.status,
        "last_seen": received_at,
    }


@app.get("/devices")
def list_devices():
    return {"devices": devices}
