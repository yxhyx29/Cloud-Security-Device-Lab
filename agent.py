
import json
import socket
import time
from urllib import request, error

DEVICE_ID = "CAM-001"
CAMERA_HOST = "127.0.0.1"
CAMERA_PORT = 8554
API_URL = "http://127.0.0.1:8000/heartbeat"
CHECK_INTERVAL = 10


def check_camera():
    try:
        with socket.create_connection(
            (CAMERA_HOST, CAMERA_PORT), timeout=3
        ):
            return "online"
    except OSError:
        return "offline"


def send_heartbeat(status):
    data = json.dumps({
        "device_id": DEVICE_ID,
        "status": status
    }).encode("utf-8")

    req = request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with request.urlopen(req, timeout=5) as response:
            print(f"Heartbeat sent: {status} (HTTP {response.status})")
    except (error.URLError, TimeoutError, OSError) as exc:
        print(f"Could not reach controller: {exc}")


def main():
    print(f"Monitoring {DEVICE_ID} every {CHECK_INTERVAL} seconds")
    try:
        while True:
            status = check_camera()
            send_heartbeat(status)
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
