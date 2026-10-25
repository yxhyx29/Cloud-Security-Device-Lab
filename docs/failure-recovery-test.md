
# RTSP Service Failure and Recovery Test

## Objective
Test whether the monitoring agent detects a loss of RTSP service availability and automatically recognises recovery.

## Environment
- Kali Linux running in VirtualBox
- MediaMTX RTSP server on port 8554
- Python monitoring agent
- FastAPI controller on port 8000
- Device identifier: CAM-001

## Methodology

1. Started MediaMTX and FastAPI.
2. Started the Python monitoring agent.
3. Confirmed that the agent reported online heartbeats every 10 seconds.
4. Queried the /devices API to verify the online status.
5. Terminated MediaMTX to simulate a service outage.
6. Observed the agent report offline heartbeats.
7. Queried /devices to verify that the controller recorded the offline status.
8. Restarted MediaMTX without restarting the agent.
9. Observed the agent resume online heartbeats.
10. Queried /devices to confirm successful recovery.

## Results

| Test | Observed result |
|---|---|
| Initial connectivity | Online, HTTP 200 |
| Service termination | Offline detected |
| Offline API verification | CAM-001 reported offline |
| Service restart | Online detected automatically |
| Recovery API verification | CAM-001 reported online |

## Technical Limitations

The agent checks TCP connectivity to the RTSP server.
It does not currently verify that a camera is actively
publishing video or that the video is valid.

Device status is stored in memory and will be lost when
the FastAPI controller restarts.

The experiment demonstrates local service availability
monitoring, not a production security monitoring system.

## Conclusion

The monitoring agent successfully detected the RTSP
service outage and subsequent recovery without requiring
an agent restart.

The FastAPI controller correctly recorded both status
transitions, demonstrating an automated service
availability monitoring workflow.
