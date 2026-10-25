# RTSP Streaming and Decoding Test

## Objective
Verify that a simulated IP camera can publish an H.264
video stream through MediaMTX and that an independent
RTSP client can receive and decode video frames.

## Lab Environment
- Operating system: Kali Linux (VirtualBox)
- Streaming server: MediaMTX
- Publisher: FFmpeg synthetic test pattern
- Client: FFprobe and FFmpeg
- RTSP endpoint: rtsp://127.0.0.1:8554/cam001

## Test Configuration
- Resolution: 320x180
- Frame rate: 5 FPS
- Codec: H.264
- Transport: RTSP over TCP
- Keyframe interval: 5 frames

## Results
1. MediaMTX accepted the published H.264 stream.
2. FFprobe identified the H.264 codec and 320x180 resolution.
3. The initial decoding attempt produced zero frames.
4. The publisher was reconfigured to provide frequent keyframes.
5. The second decoding attempt successfully decoded five frames.

## Evidence
Final FFmpeg output included:

frame=5
video:2KiB

## Conclusion
The simulated camera streaming pipeline successfully
delivered decodable video to an independent RTSP client.

This test also demonstrated the importance of keyframe
availability when joining an existing H.264 stream.
