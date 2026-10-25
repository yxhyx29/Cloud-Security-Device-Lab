
# Cloud Security Device Lab

A cybersecurity homelab project that simulates an IP camera streaming environment and monitors RTSP service availability using Python, FastAPI and MediaMTX.

Built on Kali Linux in VirtualBox to develop practical skills in networking, service monitoring, troubleshooting and incident investigation.

## Project Overview

This lab consists of three main components:

1. **MediaMTX** — hosts an RTSP streaming service for a simulated IP camera.
2. **Python Monitoring Agent** — checks RTSP TCP connectivity every 10 seconds and reports the result.
3. **FastAPI Controller** — receives device heartbeats and exposes their latest status through a REST API.

FFmpeg generates synthetic camera footage, allowing video streaming to be tested without physical camera hardware.

## Architecture

```text
FFmpeg (Simulated Camera)
           |
           | H.264 over RTSP/TCP
           v
MediaMTX Streaming Server
     127.0.0.1:8554
           ^
           | TCP connectivity checks
           |
    Python Monitoring Agent
           |
           | HTTP POST /heartbeat
           v
      FastAPI Controller
       127.0.0.1:8000
           |
           | HTTP GET /devices
           v
      Device Status JSON
```

The monitoring agent checks whether the RTSP server's TCP port is reachable. It does not inspect the video stream itself.

## Technologies Used

- Python
- FastAPI and Uvicorn
- Kali Linux
- VirtualBox
- MediaMTX
- FFmpeg and FFprobe
- RTSP, TCP/IP and HTTP
- tcpdump
- Git

## Repository Structure

```text
cloud-security-device-lab/
├── agent.py
├── app.py
├── requirements.txt
├── config/
│   └── mediamtx.yml
├── docs/
│   ├── tcp-connectivity-test.md
│   ├── rtsp-stream-test.md
│   └── failure-recovery-test.md
├── .gitignore
└── README.md
```

## Prerequisites

- Linux environment (tested on Kali Linux)
- Python 3
- FFmpeg and FFprobe
- MediaMTX v1.21.2
- Git

MediaMTX is downloaded separately. Its executable is not included in this repository.

## Installation

Clone the repository:

```bash
git clone <YOUR-REPOSITORY-URL>
cd cloud-security-device-lab
```

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Install FFmpeg if necessary:

```bash
sudo apt update
sudo apt install ffmpeg
```

Download MediaMTX v1.21.2 from its official GitHub releases page:

https://github.com/bluenviron/mediamtx/releases

Extract the Linux AMD64 executable into:

```text
tools/mediamtx/mediamtx
```

The tracked configuration file is located at `config/mediamtx.yml`.

## Running the Lab

Use separate terminals for the following components.

### 1. Start MediaMTX

```bash
./tools/mediamtx/mediamtx config/mediamtx.yml
```

The RTSP service listens on `127.0.0.1:8554`.

### 2. Start the FastAPI Controller

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start FastAPI:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Interactive API documentation is available at:

http://127.0.0.1:8000/docs

### 3. Start the Monitoring Agent

In another terminal:

```bash
source .venv/bin/activate
python agent.py
```

The agent checks the RTSP TCP port every 10 seconds and submits a heartbeat to the controller.

### 4. Publish a Simulated Camera Stream

In another terminal:

```bash
ffmpeg -nostdin -hide_banner -loglevel warning \
-re -f lavfi -i testsrc=size=320x180:rate=5 \
-t 60 -c:v libx264 -preset ultrafast \
-tune zerolatency -g 5 -keyint_min 5 \
-sc_threshold 0 -pix_fmt yuv420p \
-rtsp_transport tcp -f rtsp \
rtsp://127.0.0.1:8554/cam001
```

This publishes a 60-second synthetic H.264 video stream.

### 5. Check Device Status

```bash
curl http://127.0.0.1:8000/devices
```

Example response:

```json
{
  "devices": {
    "CAM-001": {
      "status": "online",
      "last_seen": "2026-10-25T10:35:56.210708+00:00",
      "seconds_since_heartbeat": 2.4
    }
  }
}
```

The timestamp and elapsed seconds will vary.

## Testing and Results

### TCP Connectivity

Captured local TCP traffic using tcpdump and investigated the TCP connection establishment process.

See [TCP Connectivity Test](docs/tcp-connectivity-test.md).

### RTSP Video Streaming

Successfully published an H.264 stream to MediaMTX, identified the video codec using FFprobe and decoded five frames using FFmpeg.

See [RTSP Streaming Test](docs/rtsp-stream-test.md).

### Failure and Recovery Simulation

Stopped the MediaMTX service to simulate an outage.

The monitoring agent reported the service as offline, and FastAPI recorded the status change.

After restarting MediaMTX, the agent automatically resumed online heartbeats without requiring an agent restart.

See [Failure and Recovery Test](docs/failure-recovery-test.md).

## Limitations

- The agent checks TCP port availability, not actual camera video health.
- Device information is stored in memory and is lost when FastAPI restarts.
- No authentication or encryption is implemented for the monitoring API.
- The lab uses localhost and is not designed for public network exposure.
- No persistent alerting or notification mechanism is implemented.

## Potential Improvements

- Verify RTSP stream availability using application-layer checks.
- Store device events in a database.
- Implement an alerting system for outages.
- Add authentication and secure communications.
- Develop a monitoring dashboard.
- Support multiple simulated cameras.

## Skills Demonstrated

- Linux command-line administration
- Python scripting and API development
- TCP/IP and RTSP troubleshooting
- Network packet capture and analysis
- Automated service availability monitoring
- Controlled failure and recovery testing
- Git version control
- Technical documentation

## Disclaimer

This project is an educational cybersecurity homelab. It is not a production-grade camera security or monitoring platform.
