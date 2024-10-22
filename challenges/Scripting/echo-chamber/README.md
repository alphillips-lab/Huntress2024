# Echo Chamber

## Description

<small>Author: @JohnHammond#6971</small><br><br>Is anyone there? Is anyone there?  I'm sending myself the flag! I'm sending myself the flag! <br><br> <b>Download the file(s) below.</b>


## Files

* [echo_chamber.pcap](<files/echo_chamber.pcap>)

## Solution

This can be solved by reading a single byte from each ping packet on a single side of the transmission.

```python
import sys
from scapy.all import rdpcap, ICMP

def get_echo_requests(infile):
    packets = rdpcap(infile)
    echo_requests = b""
    for packet in packets:
        if packet.haslayer(ICMP) and packet[ICMP].type == 8:
            echo_requests += packet[ICMP].load[-1].to_bytes(1, "little")
    return echo_requests

out = get_echo_requests(sys.argv[1])
flag = b"flag{" + out.split(b"flag{")[1].split(b"}")[0] + b"}"
print(flag.decode())
```