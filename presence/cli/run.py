#######################################################################################################################
# Author: Abdallah Ibrahim
# Mail: abdallah.ibrahim@uni.lu
# Overview: run test Presence.
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
from output import *

@click.command(short_help="Prints Presence's run test information.")
#tests
@click.option('--ycsb', flag_value=True, help='YCSB Test.')
@click.option('--iperf', flag_value=True, help='Iperf Test.')
@click.option('--rpcperf', flag_value=True, help='Twitter RPCperf Test.')
@click.option('--ab', flag_value=True, help='Apache AB Test.')
@click.option('--httpload', flag_value=True, help='HTTP Load Test.')
@click.option('--pg', flag_value=True, help='PGbench PostegreSQL Test.')
@click.option('--rbench', flag_value=True, help='Redis-Benchmarking Test.')
@click.option('--memt', flag_value=True, help='Memtier-Benchmarking Test.')
#servers
@click.option('-R','--redis', flag_value=True, help='Testing Redis Server.')
@click.option('-Mem','--memcached', flag_value=True, help='Testing Memcached Server.')
@click.option('-Mdb','--mongodb', flag_value=True, help='Testing Mongodb Server.')
@click.option('-A','--apache', flag_value=True, help='Testing Apache Server.')
@click.option('-PSQL','--postegresql', flag_value=True, help='Testing PostegreSQL Server.')
@click.option('-IpS','--iperfserver', flag_value=True, help='Testing Iperf Server.')
#Input parameters
@click.option('-o','--oper', default=1000,help='The number of operations per second.')
@click.option('-r','--rec', default=1000,help='The number of records per second.')
@click.option('-rq','--req', default=1000,help='The number of requests per second.')
@click.option('-td','--thrd', default=1,help='The number of threads.')
@click.option('-pp','--pips', default=1,help='The number of pipes.')
@click.option('-tr','--trans', default=1000,help='The number of transactions.')
@click.option('-ft','--fetches', default=1000,help='The number of fetches for the http-load test.')
@click.option('-pc','--pclts', default=5,help='The number of parallel clients.')
@click.option('-s','--size', default=40,help='The unite of size such as size of data for Memtier-Benchmarking.')
@click.option('-p','--protocol', default='memcache_text',help='Protocol to use (default: memcache_text). Supported protocols are redis, memcache_text, memcache_binary.')
#@click.option('-wl','--workload', default=1,help='The size of workload.')
#others
@click.option('-n','--nrepeat', default= 1 ,help='Number of iterations to repeate a test (default: 1).')
@click.option('-incby','--increaseby', default= 0 ,help='Number to increase the value of operations or records during a test (default: 0).')
@click.option('--every', default= 1 ,help='The modulo number to repeate during a test (default: 1).')
@click.option('-tdh','--thrdhop', default=1,help='The number of threads hop count(default: 1).')
@click.option('-pch','--pcltshop', default=1,help='The number of parallel clients hop count(default: 1).')
@click.option('-sF','--sfactor',   default=50,help='The scaling factor for the postegresql database to setup a db for benechmarking (default: 50).')
@click.option('-fF','--ffactor',   default=100,help='The filling factor for the postegresql database to fill-in a db for benechmarking (default: 100).')

#@click.option('--fullRun', flag_value=True, help='A flag to indicate the full runneing script')

@click.option('--outputdir', default='/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Output/',help='The directory for the output files (default:/home/git/../../presence/presence/cli/Output/).')
#

def run(oper,rec,thrd,req,pclts,fetches,size,protocol,pips,ycsb,iperf,rpcperf,ab,httpload,pg,rbench,memt,redis,memcached,mongodb,apache,postegresql,iperfserver,nrepeat,increaseby,every,thrdhop,outputdir,pcltshop,sfactor,ffactor,trans):
	"""
    PRESENCE Run commandline interface.

    Select the [test tool] [Targeted server] as from the table... \n

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
 	if ycsb and redis:
 		host = "redis.host=127.0.0.1"
		port = "redis.port=6379"
		server = "redis"
		workLoad = "workloads/workloada"
 		os.chdir(os.getenv('HOME'))
 		os.chdir("YCSB")
 		click.echo('Directory changed to ./YCSB/')
 		char = click.prompt('Did you run maven and load the YCSB test before [Y/n]?', type=str, default = 'y')
 		if char == 'n':
 			draft = call(["mvn", "-pl", "com.yahoo.ycsb:redis-binding", "-am", "clean","package"])
 			click.echo('\n ----Done with Maven----\n ')
 			click.echo('\n----Load the YCSB Redis Test----\n')
 			subprocess.call(["./bin/ycsb", "load", server,"-s", "-P", workLoad,"-p",host,"-p",port,"-threads",str(thrd),"-p","recordcount="+str(rec),"-p","operationcount="+str(oper)],stdout=subprocess.PIPE)
 			click.echo('\n----YCSB Redis Test is loaded----\n')
 		click.echo('\n----Run the YCSB Redis Test----\n')
 		writer, csv = create_output_file(outputdir,'ycsb','redis')
 		for num in range (0,nrepeat):
 			if nrepeat >= every and every != 1:
 				if num % every == 0:
 					thrd = thrd + thrdhop
 			if nrepeat < every:
 				click.echo('Error: The moduolo number (--every) to hop during the repeatation is > the number of repeating (-n)')
 				exit(50)
 			oper = oper + increaseby
 			rec = rec + increaseby
 			vlist = [num, 'ycsb-redis', workLoad, oper, rec,  thrd]
 			test_out = check_output(["./bin/ycsb", "run", server,"-s", "-P", workLoad,"-p",host,"-p",port,"-threads",str(thrd),"-p","recordcount="+str(rec),"-p","operationcount="+str(oper)])
 			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
 			write_ycsb_results(writer, csv, test_out, vlist)
 		close_csv(csv)
 	elif ycsb and memcached:
 		host = "memcached.hosts=127.0.0.1"
		port = "memcached.port=11211"
		server = "memcached"
		workLoad = "workloads/workloada"
 		os.chdir(os.getenv('HOME'))
 		os.chdir("YCSB")
 		click.echo('Directory changed to ./YCSB/')
 		char = click.prompt('Did you run maven and load the YCSB test before [Y/n]?', type=str, default = 'y')
 		if char == 'n':
 			draft = call(["mvn", "-pl", "com.yahoo.ycsb:memcached-binding", "-am", "clean","package"])
 			click.echo('\n ----Done with Maven----\n ')
 			click.echo('\n----Load the YCSB Memcached Test----\n')
 			subprocess.call(["./bin/ycsb", "load", server,"-s", "-P", workLoad,"-p",host,"-p",port,"-threads",str(thrd),"-p","recordcount="+str(rec),"-p","operationcount="+str(oper)],stdout=subprocess.PIPE)
 			click.echo('\n----YCSB Memcached Test is loaded----\n')
 		click.echo('\n----Run the YCSB Memcached Test----\n')
 		writer, csv = create_output_file(outputdir,'ycsb','memcached')
 		for num in range (0,nrepeat):
 			if nrepeat >= every and every != 1:
 				if num % every == 0:
 					thrd = thrd + thrdhop
 			if nrepeat < every:
 				click.echo('Error: The moduolo number (--every) to hop during the repeatation is > the number of repeating (-n)')
 				exit(50)
 			oper = oper + increaseby
 			rec = rec + increaseby
 			vlist = [num, 'ycsb-memcached', workLoad, oper, rec,  thrd]
 			test_out = check_output(["./bin/ycsb", "run", server,"-s", "-P", workLoad,"-p",host,"-p",port,"-threads",str(thrd),"-p","recordcount="+str(rec),"-p","operationcount="+str(oper)])
 			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
 			write_ycsb_results(writer, csv, test_out, vlist)
 		close_csv(csv)
 	elif ycsb and mongodb:
 		host = "mongodb.host=127.0.0.1"
		port = "mongodb.port=27017"
		mongodb_url= "mongodb.url=mongodb://localhost:27017/ycsb?w=0"
		server = "mongodb"
		workLoad = "workloads/workloada"
 		os.chdir(os.getenv('HOME'))
 		os.chdir("YCSB")
 		click.echo('Directory changed to ./YCSB/')
 		char = click.prompt('Did you run maven and load the YCSB test before [Y/n]?', type=str, default = 'y')
 		if char == 'n':
 			draft = call(["mvn", "-pl", "com.yahoo.ycsb:mongodb-binding", "-am", "clean","package"])
 			click.echo('\n ----Done with Maven----\n ')
 			click.echo('\n----Load the YCSB Mongodb Test----\n')
 			subprocess.call(["./bin/ycsb", "load", server,"-s", "-P", workLoad,"-p",mongodb_url,"-threads",str(thrd),"-p","recordcount="+str(rec),"-p","operationcount="+str(oper)],stdout=subprocess.PIPE)
 			click.echo('\n----YCSB Mongodb Test is loaded----\n')
 		click.echo('\n----Run the YCSB Mongodb Test----\n')
 		writer, csv = create_output_file(outputdir,'ycsb','mongodb')
 		for num in range (0,nrepeat):
 			if nrepeat >= every and every != 1:
 				if num % every == 0:
 					thrd = thrd + thrdhop
 			if nrepeat < every:
 				click.echo('Error: The moduolo number (--every) to hop during the repeatation is > the number of repeating (-n)')
 				exit(50)
 			oper = oper + increaseby
 			rec = rec + increaseby
 			vlist = [num, 'ycsb-mongodb', workLoad, oper, rec,  thrd]
 			test_out = check_output(["./bin/ycsb", "run", server,"-s", "-P", workLoad,"-p",mongodb_url,"-threads",str(thrd),"-p","recordcount="+str(rec),"-p","operationcount="+str(oper)])
 			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
 			write_ycsb_results(writer, csv, test_out, vlist)
 		close_csv(csv)
 	elif (ycsb and apache) or (ycsb and postegresql) or (ycsb and iperfserver):
 		click.echo('Attention...\n')
 		click.echo('This testing tool is not suitable to test this server ...\n')
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
	elif memt and redis:
		host = "127.0.0.1"
		port = "6379"
		writer, csv = create_output_file(outputdir,'memtier','redis')
		for num in range (0,nrepeat):
			if nrepeat >= every and every != 1:
				if num % every == 0:
					thrd = thrd + thrdhop
					pclts = pclts + pcltshop
			if nrepeat < every:
				click.echo('Error: The moduolo number (--every) to hop during the repeatation is > the number of repeating (-n)')
				exit(50)
			req = req + increaseby
			vlist = [num, 'memtier-redis', req, pclts, size,  thrd]
			test_out = check_output(["memtier_benchmark","-s",host,"-p",port,"-n",str(req),"-c",str(pclts),"-t",str(thrd),"-d", str(size),"--hide-histogram"])
			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
			write_memtier_results(writer, test_out, vlist)
		close_csv(csv)
	elif memt and memcached:
		host = "127.0.0.1"
		port = "11211"
		writer, csv = create_output_file(outputdir,'memtier','memcached')
		for num in range (0,nrepeat):
			if nrepeat >= every and every != 1:
				if num % every == 0:
					thrd = thrd + thrdhop
					pclts = pclts + pcltshop
			if nrepeat < every:
				click.echo('Error: The moduolo number (--every) to hop during the repeatation is > the number of repeating (-n)')
				exit(50)
			req = req + increaseby
			vlist = [num, 'memtier-memcached', req, pclts, size,  thrd]
			test_out = check_output(["memtier_benchmark","-s",host,"-p",port,"-P",protocol,"-n",str(req),"-c",str(pclts),"-t",str(thrd),"-d", str(size),"--hide-histogram"])
			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
			write_memtier_results(writer, test_out, vlist)
		close_csv(csv)
 	elif rbench and redis:
 		host = "127.0.0.1"
		port = "6379"
		test_out = check_output(["redis-benchmark","-n",str(req),"-c",str(pclts),"-h",host,"-p",port,"-t",test,"-d", str(size),"-P",str(pips)])
		click.echo(' \n The final results are...\n %s' % test_out)
 	elif rpcperf and redis:
 		pass
 	elif rpcperf and memcached:
 		pass
 	elif rpcperf and apache:
 		pass
 	elif pg and postegresql:
 		host = "127.0.0.1" #"10.10.1.200" 
 		port = "5432"
 		exName = "pgbench-postgreSQL"
 		dbname = "postgres"  #"ali"
 		DB_size = str(sfactor) +" x 16MB"
 		char = click.prompt('Did you initialize and load the pgbench test before [Y/n]?', type=str, default = 'y')
 		if char == 'n':
 			click.echo('\n----Load and initialize the pgbench Test----\n')
 			subprocess.call(["sudo", "-u", "postgres","pgbench", "-i","-h", host,"-p",port ,dbname,"-s",str(sfactor),"-F",str(ffactor)],stdout=subprocess.PIPE)
 			click.echo('\n ----pgbench test initalized and loaded--------\n ')
 		click.echo('\n----Run the pgbench-postgreSQL Test----\n')
 		writer, csv = create_output_file(outputdir,'pgbench','postegresql')
 		for num in range (0,nrepeat):
 			if nrepeat >= every and every != 1:
 				if num % every == 0:
 					pclts = pclts + pcltshop
 					factors = get_factors(pclts)
 					for indx in range(0,len(factors)):
 						if factors[indx] > thrd:
 							thrd = factors[indx]
 							break
 			if nrepeat < every:
				click.echo('Error: The moduolo number (--every) to hop during the repeatation is > the number of repeating (-n)')
				exit(50)
 			trans = trans + increaseby
 			vlist = [num, 'pgbench-postgreSQL', DB_size, pclts, thrd ,trans]
 			test_out = check_output(["sudo", "-u", "postgres","pgbench","-h", host,"-p",port ,"-c",str(pclts),"-j",str(thrd),"-t",str(trans),"-r",dbname])
 			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
 			write_pgbench_results(writer, test_out, vlist)
 		close_csv(csv)
 	elif ab and apache:
 		Socket = "http://127.0.0.1:80/"
 		test = check_output(["ab","-n",str(req),"-c",str(pclts),Socket])
 		click.echo(' \n The final results are...\n %s' % test)
 	elif httpload and apache:
 		os.chdir(os.getenv('HOME'))
 		os.chdir("http_load")
 		click.echo('Directory changed to ./http_load/')
 		writer, csv = create_output_file(outputdir,'httpload','apache')
 		for num in range (0,nrepeat):
 			if nrepeat >= every and every != 1:
 				if num % every == 0:
 					pclts = pclts + pcltshop
 			if nrepeat < every:
 				click.echo('Error: The moduolo number (--every) to hop during the repeatation is > the number of repeating (-n)')
 				exit(50)
 			fetches = fetches + increaseby
 			vlist = [num, 'httpload-apache',fetches, pclts]
 			test_out = check_output(["./http_load","-parallel",str(pclts),"-fetches",str(fetches),"urls"])
 			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
 			write_httpload_results(writer, test_out, vlist)
 		close_csv(csv)
 	elif iperf and iperfserver:
 		pass
 	else:
 		click.echo('Attention...\n')
 		click.echo('You need to chose a [testing tool] to test a specific  [server] ...\n')
 		click.echo('Usage: presence run [testing_tool][server] [options]\n')
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
 		click.echo('\n check the --help command:  presence run --help   \n')
 		#click.echo('All Presence default Values:')
 		#click.echo('operations %s !' % oper)
 		#click.echo('records %s !' % rec)
 		#click.echo('threads %s !' % thrd)
 	return