#######################################################################################################################
# Author: Abdallah Ibrahim
# Mail: abdallah.ibrahim@uni.lu
# Overview: Create command Presence.
#######################################################################################################################

import click
import os
import subprocess
from subprocess import check_output
from subprocess import call
import dpkt



@click.command(short_help="Prints Presence's create command.")
@click.option('-tcp','--tcpdump', flag_value=True, help='create a tcpdupm.')
#@click.option('-tf','--tcpfile', default='capture-%H:%M:%S.txt',help='the txt file to write the tcpdump.')
@click.option('-pf','--pcapfile', default='capture-%H:%M:%S.pcap',help='the pcap file to write the tcpdump.')

def create(tcpdump,pcapfile):
 	if tcpdump:
		click.echo("This the tcpdump .... ")
		#subprocess.call(["tcpdump"],stdout=subprocess.PIPE)
		command = 'tcpdump -G 3600 -w'+pcapfile
		os.popen("sudo -S %s"%(command), 'w').write('rrss2015')
	else:
		click.echo("Hint: enter -tcp to create a new tcpdump file ... ")
		counter=0
		ipcounter=0
		tcpcounter=0
		udpcounter=0
		filename= pcapfile
		for ts, pkt in dpkt.pcap.Reader(open(filename,'r')):
			counter+=1
			eth=dpkt.ethernet.Ethernet(pkt) 
			if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
				continue
			ip=eth.data
			ipcounter+=1
			if ip.p==dpkt.ip.IP_PROTO_TCP: 
				tcpcounter+=1
			if ip.p==dpkt.ip.IP_PROTO_UDP:
				udpcounter+=1
		click.echo('Total number of packets in the pcap file: %s ' % counter)
		click.echo('Total number of ip packets:  %s ' % ipcounter)
		click.echo('Total number of tcp packets: %s ' % tcpcounter)
		click.echo('Total number of udp packets:  %s ' %  udpcounter)
	return