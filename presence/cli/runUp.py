#######################################################################################################################
# Author: Abdallah Ibrahim
# Mail: abdallah.ibrahim@uni.lu
# Overview: running up Presence servers.
#######################################################################################################################

import click
import os

import subprocess
from subprocess import check_output
from subprocess import call
import csv
import time 
from datetime import datetime
import os
from Table import Table
from existance import *


def status(server):
	click.echo('----------------------------------------------------------------------------------------------------------')
	if where_is(server):
		if server == 'psql':
			server = 'postgresql'
		click.echo('%s status:                                             ' % server)
		subprocess.call(['sudo', 'service', server, 'status'], stderr=subprocess.STDOUT, stdout = True)
		click.echo('Usage: [start | stop | restart] for starting, stoping or restarting %s' % server)
	click.echo('----------------------------------------------------------------------------------------------------------\n')
	#raw_input()


def rstart(server):
	click.echo('----------------------------------------------------------------------------------------------------------')
	if where_is(server):
		if server == 'psql':
			server = 'postgresql'
		click.echo('%s restarts running:                                             ' % server)
		subprocess.call(['sudo', 'service', server, 'restart'], stderr=subprocess.STDOUT, stdout = True)
	click.echo('----------------------------------------------------------------------------------------------------------\n')
	raw_input()

def strt(server):
	click.echo('----------------------------------------------------------------------------------------------------------')
	if where_is(server):
		if server == 'psql':
			server = 'postgresql'
		click.echo('%s starts running:                                             ' % server)
		subprocess.call(['sudo', 'service', server, 'start'], stderr=subprocess.STDOUT, stdout = True)
	click.echo('----------------------------------------------------------------------------------------------------------\n')
	raw_input()

def stp(server):
	click.echo('----------------------------------------------------------------------------------------------------------')
	if where_is(server):
		if server == 'psql':
			server = 'postgresql'
		click.echo('%s stops running:                                             ' % server)
		subprocess.call(['sudo', 'service', server, 'stop'], stderr=subprocess.STDOUT, stdout = True)
	click.echo('----------------------------------------------------------------------------------------------------------\n')


@click.command(short_help="Prints Presence's runUp servers information.")
#servers
@click.option('-R','--redis', flag_value=True, help='Redis Server.\n default = Redis status')
@click.option('-Mem','--memcached', flag_value=True, help='Memcached Server.\n default = Memcached status')
@click.option('-Mdb','--mongodb', flag_value=True, help='Mongodb Server.\n default = Mongodb status')
@click.option('-A','--apache', flag_value=True, help='Apache Server.\n default = Apache status')
@click.option('-PSQL','--postegresql', flag_value=True, help='PostegreSQL Server.\n default = PostegreSQL status')
@click.option('-IpS','--iperfserver', flag_value=True, help='Iperf Server.\n default = Iperf server status')

@click.option('-s','--start', flag_value=True, help='starting a specific server')
@click.option('-r','--restart', flag_value=True, help='restarting a specific server')
@click.option('-c','--stop', flag_value=True, help='stoping a specific server')


def runUp(redis,memcached,mongodb,apache,postegresql,iperfserver, start, stop,restart):
	"""
    PRESENCE runUp commandline interface.

    Select the [Targeted server] [options: start | stop | restart] to run up  \n


				+------------------+
				| Targeted Servers |
				+------------------+
				|       Redis      |
				+------------------+
				|     Memcached    |
				+------------------+
				|      MongoDB     |
				+------------------+
				|      Apache      |
				+------------------+
				|    PostegreSQL   |
				+------------------+
				|    iperfserver   |
				+------------------+

    """
 	
 	if redis:
 		server = 'redis-server'
 		if start:
 			strt(server)
 		elif stop:
 			stp(server)
 		elif restart:
 			rstrt(server)
 		else:
 			status(server)

 	elif memcached:
 		server = 'memcached'
 		if start:
 			strt(server)
 		elif stop:
 			stp(server)
 		elif restart:
 			rstrt(server)
 		else:
 			status(server)
 	elif mongodb:
 		server = 'mongod'
 		if start:
 			strt(server)
 		elif stop:
 			stp(server)
 		elif restart:
 			rstrt(server)
 		else:
 			status(server)
 	elif postegresql:
 		server = 'psql'
 		if start:
 			strt(server)
 		elif stop:
 			stp(server)
 		elif restart:
 			rstrt(server)
 		else:
 			status(server)
 	elif apache:
 		server = 'apache2'
 		if start:
 			strt(server)
 		elif stop:
 			stp(server)
 		elif restart:
 			rstrt(server)
 		else:
 			status(server)
 	elif iperfserver:
 		server = 'iperf'
 		if start:
 			click.echo('----------------------------------------------------------------------------------------------------------')
 			if where_is(server):
 				click.echo('%s starts running:                                             ' % server)
 				subprocess.call(['iperf', '-s'], stderr=subprocess.STDOUT, stdout = True)
 			click.echo('----------------------------------------------------------------------------------------------------------\n')
 		elif stop:
 			click.echo('----------------------------------------------------------------------------------------------------------')
 			if where_is(server):
 				click.echo('%s stops running:                                             ' % server)
 				subprocess.call(['iperf', '-s'], stderr=subprocess.STDOUT, stdout = True)
 			click.echo('----------------------------------------------------------------------------------------------------------\n')
 		elif restart:
 			click.echo('----------------------------------------------------------------------------------------------------------')
			if where_is(server):
				click.echo('%s restarts running:                                             ' % server)
				subprocess.call(['iperf', '-s'], stderr=subprocess.STDOUT, stdout = True)
			click.echo('----------------------------------------------------------------------------------------------------------\n')
 		else:
 			click.echo('----------------------------------------------------------------------------------------------------------')
 			if where_is(server):
 				click.echo('%s status:                                             ' % server)
 				i = subprocess.call(['iperf', '-s'], stderr=subprocess.STDOUT, stdout = True)
 				if i == 0:
 					click.echo("Iperf server is running")
 				click.echo('Usage: [start | stop | restart] for starting, stoping or restarting %s' % server)
 			click.echo('----------------------------------------------------------------------------------------------------------\n')
 	else:
 		click.echo('Attention...\n')
 		click.echo('You need to chose a [server] to runup, restart, stop or start  ...\n')
 		click.echo('Usage: presence runup [server] \n')
 		t = Table(titles=['Targeted Servers','Link'])
 		t.add_row(['Redis','https://redis.io/'])
 		t.add_row(['Memcached','https://memcached.org/'])
 		t.add_row(['MongoDB','https://www.mongodb.com/'])
 		t.add_row(['Apache','https://httpd.apache.org/'])
 		t.add_row(['PostegreSQL','https://www.postgresql.org/'])
 		t.add_row(['iperfserver','https://iperf.fr/'])
 		click.echo('check the following table which summerize PRESENCE\'s servers:\n\n %s' % t)
 		click.echo('\n try the --help command:  presence runup --help   \n')
 	return