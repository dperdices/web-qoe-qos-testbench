#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.nodelib import NAT
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import json
import subprocess
import argparse
import time

setLogLevel('info')
natIP = "10.0.0.2"

parser = argparse.ArgumentParser(description='Runs a test on Containernet')
parser.add_argument('-u','--url', help='URL to be tested', default="https://elpais.es")
parser.add_argument('-o','--output_json', help='Results of the test', default="results.json")
parser.add_argument('-p','--output_pcap', help='Pcap file captured near d2 (NAT)', default="capture.pcap")
parser.add_argument('-t','--timeout', help='Timeout to close priv-accept (seconds)', default=300)
parser.add_argument('-cli','--cli', help='Open CLI after the tests', action='store_true')

parser.add_argument('-tcd','--tclink_delay', help='Delay of the TCLink (ms)', default=None)
parser.add_argument('-tcbw','--tclink_bw', help='Bandwidth of the TCLink', default=None)
parser.add_argument('-tcj','--tclink_jitter', help='Jitter of the TCLink', default=None)
parser.add_argument('-tcl','--tclink_loss', help='Loss of the TCLink', default=None)

args = vars(parser.parse_args())

url = args["url"]
output_json = args["output_json"]
output_pcap = args["output_pcap"]
timeout = args["timeout"]
cli = args["cli"]

delay = args["tclink_delay"]
bw = args["tclink_bw"]
jitter = args["tclink_jitter"]
loss = args["tclink_loss"]

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.1/24', dimage="priv-accept", defaultRoute=f'via {natIP}')
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(s1, s2, cls=TCLink, delay=f'{delay}ms' if delay else None, bw=bw, jitter=jitter, loss=loss)
#d2 = net.addNAT('d2', ip=natIP, connect="s2")
#d2.configDefault()
d2 = net.addHost('d2', cls=NAT, ip='10.0.0.2/24', inNamespace=False)
net.addLink(s2, d2)

info('*** Starting network\n')
net.start()
info('*** Opening capture process\n')
tcpdump = d2.popen(["tcpdump", "-w", output_pcap, "-i", "d2-eth0"])
time.sleep(5)
info('*** Opening priv-accept\n')
cmd = ["/opt/priv-accept/priv-accept.py", 
        "--chrome_driver", "/usr/src/app/node_modules/@sitespeed.io/chromedriver/vendor/chromedriver", 
        "--docker", "--xvfb", "--rum_speed_index"]
cmd += ["--url", url]
with open("priv-accept.log", "w") as log:
    p = d1.popen(cmd,
        stdout=log, stderr=subprocess.STDOUT)
info("*** Waiting for the container\n")
try:
    (stdout, stderr) = p.communicate(timeout=timeout)
    output = d1.cmd(["cat", "output.json"])
    
    with open(output_json, "w") as out:
        out.write(output)
    
    results = json.loads(output)
except:
    pass
tcpdump.terminate()
info("*** Stopping capture\n")
if cli:
    CLI(net)
info('*** Stopping network\n')
net.stop()