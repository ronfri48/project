#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info
import subprocess

def myNetwork():
	info( '*** Adding controller\n' )
    	controller_instance = RemoteController("faucet", '127.0.0.1', 6653)
	controller_instance.checkListening()
    
	net = Mininet( topo=None,controller=None)
    	info( '*** Add switches\n')
    	s1 = net.addSwitch('s1')
    	Intf( 'enp0s3', node=s1,port=3 )

    	info( '*** Add hosts\n')
    	h1 = net.addHost('h1', ip='0.0.0.0')
    	h2 = net.addHost('h2', ip='0.0.0.0')
    
    	info( '*** Add links\n')
    	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addNAT().configDefault()
	info( '*** Starting network\n')
	
	net.start()
	bashScriptTemplate = "sudo ifconfig "
	#subprocess.Popen(bashScriptTemplate.split())
	#bashScriptTemplate = "sudo tshark -i s1-eth4 -a duration:60 -w host1.pcap  "
	#subprocess.Popen(bashScriptTemplate.split(), stdout=subprocess.PIPE)
	#bashScriptTemplate = "sudo tshark -i s1-eth5 -a duration:60 -w host2.pcap  "
	#subprocess.Popen(bashScriptTemplate.split(), stdout=subprocess.PIPE)
	#bashCapture = "sudo tshark -i enp0s3  -a duration:60 -w enp0s8.pcap "
	#h1.cmdPrint('dhclient '+h1.defaultIntf().name)
  	CLI(net)
  	net.stop()

if __name__ == '__main__':
  	  setLogLevel( 'info' )
  	  myNetwork()
