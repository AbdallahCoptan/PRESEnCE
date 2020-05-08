#######################################################################################################################
# Author: Abdallah Ibrahim
# Mail: abdallah.ibrahim@uni.lu
# Overview: checking on Presence servers and tools.
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

@click.command(short_help="Prints Presence's check servers and tools information.")
#tests
@click.option('--ycsb', flag_value=True, help='YCSB Tool.')
@click.option('--iperf', flag_value=True, help='Iperf Tool.')
@click.option('--rpcperf', flag_value=True, help='Twitter RPCperf Tool.')
@click.option('--ab', flag_value=True, help='Apache AB Tool.')
@click.option('--httpload', flag_value=True, help='HTTP Load Tool.')
@click.option('--pg', flag_value=True, help='PGbench PostegreSQL Tool.')
@click.option('--rbench', flag_value=True, help='Redis-Benchmarking Tool.')
@click.option('--memt', flag_value=True, help='Memtier-Benchmarking Tool.')
#servers
@click.option('-R','--redis', flag_value=True, help='Redis Server.')
@click.option('-Mem','--memcached', flag_value=True, help='Memcached Server.')
@click.option('-Mdb','--mongodb', flag_value=True, help='Mongodb Server.')
@click.option('-A','--apache', flag_value=True, help='Apache Server.')
@click.option('-PSQL','--postegresql', flag_value=True, help='PostegreSQL Server.')
@click.option('-IpS','--iperfserver', flag_value=True, help='Iperf Server.')



def check(ycsb,iperf,rpcperf,ab,httpload,pg,rbench,memt,redis,memcached,mongodb,apache,postegresql,iperfserver):
	"""
    PRESENCE check commandline interface.

    Select the [test tool | Targeted server] to check the existance and install if not exist \n

		+----------------------+---------+---------------------------+
		|       Test Tool      | Version |      Targeted Servers     |
		+----------------------+---------+---------------------------+
		| YCSB                 | 0.12.0  | Redis, Mongodb, Memcached |
		+----------------------+---------+---------------------------+
		| Memtier-Benchmarking | 1.2.8   | Redis, Memcached          |
		+----------------------+---------+---------------------------+
		| Redis-Benchmarking   | 2.4.2   | Redis                     |
		+----------------------+---------+---------------------------+
		| Twitter RPCperf      | 2.0.3   | Redis, Memcached, Apache  |
		+----------------------+---------+---------------------------+
		| PGbench              | 9.4.12  | PostegreSQL               |
		+----------------------+---------+---------------------------+
		| Apache-AB            | 2.3     | Apache                    |
		+----------------------+---------+---------------------------+
		| HTTP-Load            | 1       | Apache                    |
		+----------------------+---------+---------------------------+
		| Iperf                | v1, v3  | iperfserver               |
		+----------------------+---------+---------------------------+
    """
 	if ycsb:
 		name = 'YCSB'
 		if is_exist(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif httpload:
 		name = 'http_load'
 		if is_exist(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif memt:
 		name = 'memtier_benchmark'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif rbench:
 		name = 'redis-benchmark'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif ab:
 		name = 'ab'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
	elif rpcperf:
		name = 'rpc-perf'
 		if is_exist(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
	elif pg:
		name = 'pgbench'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif iperf:
 		name = 'iperf'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif redis:
 		name = 'redis-server'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 			ch = click.prompt("\nWould you like to check the [server | tool] status (e.g. running or sleeping) [y/n]", type=str, default='n', show_default=False)
 			if ch == 'y' or ch == 'Y':
 				check_server(name)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif memcached:
 		name = 'memcached'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 			ch = click.prompt("\nWould you like to check the [server | tool] status (e.g. running or sleeping) [y/n]", type=str, default='n', show_default=False)
 			if ch == 'y' or ch == 'Y':
 				check_server(name)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif mongodb:
 		name = 'mongod'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 			ch = click.prompt("\nWould you like to check the [server | tool] status (e.g. running or sleeping) [y/n]", type=str, default='n', show_default=False)
 			if ch == 'y' or ch == 'Y':
 				check_server(name)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif postegresql:
 		name = 'psql'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 			ch = click.prompt("\nWould you like to check the [server | tool] status (e.g. running or sleeping) [y/n]", type=str, default='n', show_default=False)
 			if ch == 'y' or ch == 'Y':
 				name = 'postgresql'
 				check_server(name)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif apache:
 		name = 'apache2'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 			ch = click.prompt("\nWould you like to check the [server | tool] status (e.g. running or sleeping) [y/n]", type=str, default='n', show_default=False)
 			if ch == 'y' or ch == 'Y':
 				check_server(name)
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	elif iperfserver:
 		name = 'iperf'
 		if where_is(name):
 			click.echo('You can use the presence run [testing_tool][server] command to start testing')
 			t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 			t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 			t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 			t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 			t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 			t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 			t.add_row(['Apache-AB', '2.3', 'Apache'])
 			t.add_row(['HTTP-Load', '1', 'Apache'])
 			t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 			click.echo('check the following table for the tests combinations:\n\n %s' % t)
 			ch = click.prompt("\nWould you like to check the [server | tool] status (e.g. running or sleeping) [y/n]", type=str, default='n', show_default=False)
 			if ch == 'y' or ch == 'Y':
 				i = subprocess.call(['iperf', '-s'], stderr=subprocess.STDOUT, stdout = True)
 				if i == 0:
 					click.echo("\n Iperf server is running")
 		else:
 			click.echo('Would you like to install it [y/n]?')
 	else:
 		click.echo('Attention...\n')
 		click.echo('You need to chose a [testing tool | server] to check if it is existing or not ...\n')
 		click.echo('Usage: presence check [testing_tool | server] \n')
 		t = Table(titles=['Test Tool', 'Version', 'Targeted Servers'])
 		t.add_row(['YCSB', '0.12.0', 'Redis, Mongodb, Memcached'])
 		t.add_row(['Memtier-Benchmarking', '1.2.8', 'Redis, Memcached'])
 		t.add_row(['Redis-Benchmarking', '2.4.2', 'Redis'])
 		t.add_row(['Twitter RPCperf', '2.0.3', 'Redis, Memcached, Apache'])
 		t.add_row(['PGbench', '9.4.12', 'PostegreSQL'])
 		t.add_row(['Apache-AB', '2.3', 'Apache'])
 		t.add_row(['HTTP-Load', '1', 'Apache'])
 		t.add_row(['Iperf', 'v1, v3', 'iperfserver'])
 		click.echo('check the following table which summerize testing tools and servers:\n\n %s' % t)
 		click.echo('\n try the --help command:  presence check --help   \n')
 	return