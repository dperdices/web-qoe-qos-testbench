# web-qoe-qos-testbench
A testbench made in mininet/containernet for web QoE-QoS correlation

## Requirements

- Containernet (https://github.com/containernet/containernet)

- docker

- priv-accept (as a submodule)

- tcpdump

## How to run it

```
optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to be tested
  -o OUTPUT_JSON, --output_json OUTPUT_JSON
                        Results of the test
  -p OUTPUT_PCAP, --output_pcap OUTPUT_PCAP
                        Pcap file captured near d2 (NAT)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout to close priv-accept (seconds)
  -cli, --cli           Open CLI after the tests
  -tcd TCLINK_DELAY, --tclink_delay TCLINK_DELAY
                        Delay of the TCLink (ms)
  -tcbw TCLINK_BW, --tclink_bw TCLINK_BW
                        Bandwidth of the TCLink
  -tcj TCLINK_JITTER, --tclink_jitter TCLINK_JITTER
                        Jitter of the TCLink
  -tcl TCLINK_LOSS, --tclink_loss TCLINK_LOSS
                        Loss of the TCLink
```

priv-accept arguments can be edited in main.py