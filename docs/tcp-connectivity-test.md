
# TCP Connectivity Investigation

## Objective
Verify TCP connectivity between a simulated security device client and a local MediaMTX RTSP server.

## Lab Environment
- Operating system: Kali Linux (VirtualBox VM)
- Server: MediaMTX v1.21.2
- Server address: 127.0.0.1
- Server port: TCP 8554
- Packet capture tool: tcpdump
- Network interface: lo (loopback)

## Test Procedure
1. Started the MediaMTX server.
2. Confirmed that the RTSP listener was running.
3. Started tcpdump on the loopback interface.
4. Used Python's socket module to establish a TCP connection.
5. Saved and inspected the resulting packet capture.

## Results
- TCP connection: Successful
- Packets captured: 6
- Kernel packet drops: 0
- Client port: 35016
- Server port: 8554

## Packet Analysis
The capture showed a successful TCP three-way handshake:

1. SYN: Client requested a connection.
2. SYN-ACK: Server acknowledged the request.
3. ACK: Client completed the handshake.

The remaining packets showed the connection closing.

## Conclusion
TCP connectivity to the MediaMTX RTSP listening port was verified.

This test does not confirm successful RTSP video publishing or playback. Further application-layer testing is required.
