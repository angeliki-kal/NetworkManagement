# !/usr/bin/python

"""
Task 1: Implementation of the experiment described in the paper with title: 
"From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks"
http://ieeexplore.ieee.org/document/7859348/ 
"""

import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI
import sys
gnet=None

#.data files
phase1_c0_out = 'phase1_c0_output.data'
phase1_client_out = 'phase1_client_output.data'
phase1_ping = 'phase1_ping.data'
phase2_c0_out = 'phase2_c0_output.data'
phase2_client_out = 'phase2_client_output.data'
phase2_ping = 'phase2_ping.data'
phase3_c0_out = 'phase3_c0_output.data'
phase3_client_out= 'phase3_client_output.data'
phase3_ping = 'phase3_ping.data'


# Implement the graphic function in order to demonstrate the network measurements
# Hint: You can save the measurement in an output file and then import it here
def graphic():
    
    if not os.path.exists('output2'):
        os.makedirs('output2')
    print"Phase 1:"
    tjp = pd.read_csv('c0-client.p1', delim_whitespace=True, header=None)
    tjp2 = pd.read_csv('c0-client.p2', delim_whitespace=True, header=None)
#latency
    l = pd.read_csv('c0-client-ping.p1', delim_whitespace=True, header=None)
    l2 = pd.read_csv('c0-client-ping.p1', delim_whitespace=True, header=None)
    latency_p1 = [x + y for x, y in zip(l[0].tolist(), l2[0].tolist())]
    latency_fig = plt.figure()
    latency_fig.suptitle('[Phase 1] Latency', fontsize=20)
    plt.ylabel('latency (ms)')
    plt.xlabel('time (sec)')
    plt.plot(latency_p1)
    latency_fig.savefig('output2/latency_phase1.png')
 #packet loss
    packet_loss_p1 = []
    for packets, packets2 in zip(tjp[2].tolist(), tjp2[2].tolist()):
     packet_loss_p1.append(int(packets.rpartition('/')[0]) + int(packets2.rpartition('/')[0]))
    packet_loss_fig = plt.figure()
    packet_loss_fig.suptitle('[Phase 1] Packet Loss ', fontsize=20)
    plt.ylabel('packets')
    plt.xlabel('time (sec)')
    plt.plot(packet_loss_p1)
    packet_loss_fig.savefig('output2/packet_loss_phase1.png')
 #throughput
    throughput_p1 = [(x+y)/2 for x, y in zip(tjp[0].tolist(), tjp2[0].tolist())]
    throughput_fig = plt.figure()
    throughput_fig.suptitle('[Phase 1] Throughput ', fontsize=20)
    plt.ylabel('kbps')
    plt.xlabel('time (sec)')
    plt.plot(throughput_p1)
    throughput_fig.savefig('output2/throughput_phase1.png')
 #jitter     
    jitter_p1 = [x + y for x, y in zip(tjp[1].tolist(), tjp2[1].tolist())]
    jitter_fig = plt.figure()
    jitter_fig.suptitle('Jitter Phase 1', fontsize=18)
    plt.ylabel('ms')
    plt.xlabel('Seconds')
    plt.plot(jitter_p1)
    jitter_fig.savefig('output2/jitter_phase1.png')

    print "Phase 2:"
    #latency
    l = pd.read_csv('c0-client-ping.p3', delim_whitespace=True, header=None)
    latency_p2 = l[0].tolist()
    latency_fig = plt.figure()
    latency_fig.suptitle('[Phase 2]: Latency', fontsize=20)
    plt.ylabel('latency (ms)')
    plt.xlabel('time (sec)')
    plt.plot(latency_p2)
    latency_fig.savefig('output2/latency_phase2.png')
 #Throughput   
    tjp = pd.read_csv('c0-client.p3', delim_whitespace=True, header=None)
    throughput_p2 = tjp[0].tolist()
    throughput_fig = plt.figure()
    throughput_fig.suptitle('[Phase 2] Throughput', fontsize=20)
    plt.ylabel('kbps')
    plt.xlabel('time (sec)')
    plt.plot(throughput_p2)
    throughput_fig.savefig('output2/throughput_phase2.png')
#Packet Loss
    packet_loss_p2 = []
    for packets in tjp[2].tolist():
        packet_loss_p2.append(int(packets.rpartition('/')[0]))
    packet_loss_fig = plt.figure()
    packet_loss_fig.suptitle('[Phase 2] packet loss', fontsize=20)
    plt.ylabel('packets')
    plt.xlabel('time (sec)')
    plt.plot(packet_loss_p2)
    packet_loss_fig.savefig('output2/packet_loss_phase2.png')
 #Jitter
    jitter_p2 = tjp[1].tolist()
    jitter_fig = plt.figure()
    jitter_fig.suptitle('[Phase 2]: Jitter', fontsize=20)
    plt.ylabel('jitter (ms)')
    plt.xlabel('time (sec)')
    plt.plot(jitter_p2)
    jitter_fig.savefig('output2/jitter_phase2.png')

    print"Overall Results"
    #Overall lLatency
    latency = latency_p1
    latency.extend(latency_p2)
    latency_fig = plt.figure()
    latency_fig.suptitle('[Overall] Latency', fontsize=20)
    plt.ylabel('latency (ms)')
    plt.xlabel('time (sec)')
    plt.plot(latency)
    latency_fig.savefig('output2/latency.png')
    #Overall throughput
    throughput = throughput_p1
    throughput.extend(throughput_p2)
    throughput_fig = plt.figure()
    throughput_fig.suptitle('[Overall] throughput ', fontsize=20)
    plt.ylabel('kbps')
    plt.xlabel('time (sec)')
    plt.plot(throughput)
    throughput_fig.savefig('output2/throughput.png')
      #Overall Packet Loss
    packet_loss = packet_loss_p1
    packet_loss.extend(packet_loss_p2)
    packet_loss_fig = plt.figure()
    packet_loss_fig.suptitle('[Overall] packet loss', fontsize=20)
    plt.ylabel('packets')
    plt.xlabel('time (sec)')
    plt.plot(packet_loss)
    packet_loss_fig.savefig('output2/packet_loss.png')
    #Overall Jitter
    jitter = jitter_p1
    jitter.extend(jitter_p2)
    jitter_fig = plt.figure()
    jitter_fig.suptitle('[Overall]  jItter', fontsize=20)
    plt.ylabel('jitter (ms)')
    plt.xlabel('time (sec)')
    plt.plot(jitter)
    jitter_fig.savefig('output2/jitter.png')
    
    
def apply_experiment(car,client,switch):
    #Samples
    x=15
    
    #time.sleep(2)
    print "Applying first phase"

    ################################################################################ 
    #   1) Add the flow rules below and the necessary routing commands
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #   Hint 2: For the routing commands check the configuration 
    #           at the beginning of the experiment.
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #               ***************** Insert code below *********************  
    #################################################################################
	
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1,3')
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.100')    
    client.cmd('iperf -s -u -i 1 >> %s &' % phase1_client_out)
    time.sleep(1)
    car[0].cmd('ping 200.0.10.2 -c %d >> %s &' % (x,phase1_ping))
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t %d >> %s' % (x,phase1_c0_out))
    time.sleep(1)
    car[0].cmd('grep -v "datagrams received out-of-order" phase1_client_output.data | head -16 | tail -9 | tr -s " " | cut -d " " -f6,10,12-13 > c0-client.p1 ')
    car[0].cmd('grep -v "datagrams received out-of-order" phase1_client_output.data | head -17 | tail -1 | tr -s " " | cut -d " " -f5,9,11-12 >> c0-client.p1 ')
    car[0].cmd('grep -v "(DUP\!)" phase1_ping.data | tail -14 | head -10 | cut -d "=" -f4 > c0-client-ping.p1')
    
    print "Moving node"
    car[0].moveNodeTo('150,100,0')
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2,3')
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')
    client.cmd('iperf -s -u -i 1 >> %s &' % phase2_client_out)
    time.sleep(1)
    car[0].cmd('ping 200.0.10.2 -c %d >> %s &' % (x,phase2_ping))
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t %d >> %s' % (x,phase2_c0_out))
    time.sleep(1)
    car[0].cmd('grep -v "datagrams received out-of-order" phase2_client_output.data | head -16 | tail -9 | tr -s " " | cut -d " " -f6,10,12-13 > c0-client.p2 ')
    car[0].cmd('grep -v "datagrams received out-of-order" phase2_client_output.data | head -17 | tail -1 | tr -s " " | cut -d " " -f5,9,11-12 >> c0-client.p2 ')
    car[0].cmd('grep -v "(DUP\!)" phase2_ping.data | tail -14 | head -10 | cut -d "=" -f4 > c0-client-ping.p2')
    
    print "Moving node"
    car[0].moveNodeTo('190,100,0')
    
    
    time.sleep(2)
    print "Applying second phase"
    
    ################################################################################ 
    #   1) Add the flow rules below and routing commands if needed
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #           ***************** Insert code below ********************* 
    #################################################################################
    
    
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')
    client.cmd('iperf -s -u -i 1 >> %s &' % phase3_client_out)
    time.sleep(1)
    car[0].cmd('ping 200.0.10.2 -c %d >> %s &' % (x,phase3_ping))
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t %d >> %s' % (x,phase3_c0_out))
    time.sleep(1)
    car[0].cmd('grep -v "datagrams received out-of-order" phase3_client_output.data | head -16 | tail -9 | tr -s " " | cut -d " " -f6,10,12-13 > c0-client.p3')
    car[0].cmd('grep -v "datagrams received out-of-order" phase3_client_output.data | head -17 | tail -1 | tr -s " " | cut -d " " -f5,9,11-12 >> c0-client.p3')
    car[0].cmd('tail -14 phase3_ping.data | head -10 | cut -d "=" -f4 > c0-client-ping.p3')
	
def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car = []
    stas = []
    for x in range(0, 1):
        car.append(x)
        stas.append(x)
    
            
    car[0] = net.addCar('car%s' % (0), wlans=2, ip='10.0.0.%s/8' % (0 + 1), mac='00:00:00:00:00:0%s' % 0, mode='b')

    
    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000', mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000', mode='ac', channel='6', position='180,75,0', range=70)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000', mode='g', channel='11', position='140,120,0', range=40)
    c1 = net.addController('c1', controller=Controller)
    client = net.addHost ('client')
    switch = net.addSwitch ('switch', dpid='4000000000000000')

    net.plotNode(client, position='125,230,0')
    net.plotNode(switch, position='125,200,0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(eNodeB1, switch)
    net.addLink(eNodeB2, switch)
    net.addLink(rsu1, switch)
    net.addLink(switch, client)

    print "*** Starting network"
    net.build()
    c1.start()
    eNodeB1.start([c1])
    eNodeB2.start([c1])
    rsu1.start([c1])
    switch.start([c1])

    for sw in net.vehicles:
        sw.start([c1])

    i = 1
    j = 2
    for c in car:
        c.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (c, i))
        c.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (c, i))
        c.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

    i = 1
    j = 2
    for v in net.vehiclesSTA:
        v.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (v, j))
        v.cmd('ifconfig %s-mp0 10.0.0.%s/24 up' % (v, i))
        v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for v1 in net.vehiclesSTA:
        i = 1
        j = 1
        for v2 in net.vehiclesSTA:
            if v1 != v2:
                v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    client.cmd('ifconfig client-eth0 200.0.10.2')
    #net.vehiclesSTA[0].cmd('ifconfig car0STA-eth0 200.0.10.50')
    
    car[0].cmd('modprobe bonding mode=3')
    car[0].cmd('ip link add bond0 type bond')
    car[0].cmd('ip link set bond0 address 02:01:02:03:04:08')
    car[0].cmd('ip link set car0-eth0 down')
    car[0].cmd('ip link set car0-eth0 address 00:00:00:00:00:11')
    car[0].cmd('ip link set car0-eth0 master bond0')
    car[0].cmd('ip link set car0-wlan0 down')
    car[0].cmd('ip link set car0-wlan0 address 00:00:00:00:00:15')
    car[0].cmd('ip link set car0-wlan0 master bond0')
    car[0].cmd('ip link set car0-wlan1 down')
    car[0].cmd('ip link set car0-wlan1 address 00:00:00:00:00:13')
    car[0].cmd('ip link set car0-wlan1 master bond0')
    car[0].cmd('ip addr add 200.0.10.100/24 dev bond0')
    car[0].cmd('ip link set bond0 up')


    #client.cmd('ip route add 192.168.1.8 via 200.0.10.150')
    #client.cmd('ip route add 10.0.0.1 via 200.0.10.150')

    #net.vehiclesSTA[3].cmd('ip route add 200.0.10.2 via 192.168.1.7')
    #net.vehiclesSTA[3].cmd('ip route add 200.0.10.100 via 10.0.0.1')
    #net.vehiclesSTA[0].cmd('ip route add 200.0.10.2 via 10.0.0.4')

    #car[0].cmd('ip route add 10.0.0.4 via 200.0.10.50')
    #car[0].cmd('ip route add 192.168.1.7 via 200.0.10.50')
    #car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
    #car[3].cmd('ip route add 200.0.10.100 via 192.168.1.8')
    

    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()

    # Uncomment and modify the two commands below to stream video using VLC 
    car[0].cmdPrint("vlc -vvv bunnyMob.mp4 --sout 'duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
    client.cmdPrint("vlc rtp://200.0.10.2:5004 &")

    car[0].moveNodeTo('110,100,0')
    

    os.system('ovs-ofctl del-flows switch')

    time.sleep(3)

    apply_experiment(car,client,switch)

    # Uncomment the line below to generate the graph that you implemented
    graphic()

    # kills all the xterms that have been opened
    # os.system('pkill xterm')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
        os.system('rm *.data *.phase1 *.phase2 *.phase3 *.p1 *.p2 *.p3')
        print "in try"
    except:
        print "Error handle:"
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        os.system('rm *.data *.phase1 *.phase2 *.phase3 *.p1 *.p2 *.p3 ')
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print "no network created"

