#######################################################################################################################
# Author: Abdallah Ibrahim
# Mail: abdallah.ibrahim@uni.lu
# Overview: Campaign test Presence.
#######################################################################################################################

import click
import os

import subprocess
from multiprocessing import Process
from multiprocessing import Pool
from itertools import product
from functools import partial
from subprocess import check_output
from subprocess import Popen
from subprocess import call
import subprocess
import csv
import ast
import time
import random
from datetime import datetime
import os
import signal
from Table import Table
from output import *
from generatecamp import *
from dstat import *


#global variables
redisServer = "redis"
redisHost = "127.0.0.1"
redisPort = "6379"
memcachedServer = "memcached"
memcachedHost = "127.0.0.1"
memcachedPort = "11211"
mongoServer = "mongodb"
mongoHost = "127.0.0.1"
mongoPort = "27017"
#variables for ycsb
workload = "workloads/workloada"
mongoURL = "mongodb.url=mongodb://localhost:27017/ycsb?w=0"

def info(title):
    #print title
    #print 'module name:', __name__
    #if hasattr(os, 'getppid'):  # only available on Unix
        #print 'parent process:', os.getppid()
    print 'process id:', os.getpid()
    pid = os.getpid()
    return pid

def complete_campaign(outputdir,args):
	if args[0] == 'ycsb':
		pid = info('function complete_campaign')
		testname = args[0]+'-' + args[1]  #bench-server
		writer, csv = create_output_file(outputdir,args[0],args[1])
		print "sleep for...", args[2]
		time.sleep(args[2])
		print "Already !! sleept for...", args[2]
		start = time.time()
		l = []
		l.append(args[3])
		l.append(args[0])
		l.append(args[1])
		l.append(str(datetime.now()))
		num = 0
		while True:
			if time.time() - start < args[7] :
				print "---------------------- process num", args[3],"----------------------------"
				vlist = [num, testname, workload, args[4], args[5] , args[6]]
				if args[1] == 'redis':
					host = 'redis.host=' + redisHost
					port = 'redis.port='+ redisPort
					test_out = check_output(["./bin/ycsb", "run", args[1],"-s", "-P", workload,"-p",host,"-p",port,"-threads",str(args[6]),"-p","recordcount="+str(args[5]),"-p","operationcount="+str(args[4])])
				if args[1] == 'mongodb':
					host = 'mongodb.host=' + mongoHost
					port = 'mongodb.port='+ mongoPort
					test_out = check_output(["./bin/ycsb", "run", args[1],"-s", "-P", workload,"-p",mongoURL,"-threads",str(args[6]),"-p","recordcount="+str(args[5]),"-p","operationcount="+str(args[4])])
				if args[1] == 'memcached':
					host = 'memcached.host=' + memcachedHost
					port = 'memcached.port='+ memcachedPort
					test_out = check_output(["./bin/ycsb", "run", args[1],"-s", "-P", workload,"-p",host,"-p",port,"-threads",str(args[6]),"-p","recordcount="+str(args[5]),"-p","operationcount="+str(args[4])])
				click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
				write_ycsb_results(writer, csv, test_out, vlist)
				num = num + 1
			else:
				print "********************** process terminated", args[3],"****************************"
				l.append(str(datetime.now()))
				break
		file = open('/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/workers.txt', "a")
		workerstatus = str(l) + '\n'
		file.write(workerstatus)
		file.close()
		close_csv(csv)
	elif args[0] == 'memtier' and args[1] == 'redis':
		print "no yet"
	elif args[0] == 'memtier' and args[1] == 'memcached':
		print "no yet"
	elif args[0] == 'httpload' and args[1] == 'apache':
		print "no yet"
	elif args[0] == 'PGbench' and args[1] == 'postegresql':
		print "no yet"
	else:
		print "no matches"


def ycsb_campaign(host, port, server, workload,outputdir,args):
	""" definition """
	pid = info('function ycsb_campaign')
	testname = 'ycsb-' + server
	os.chdir(os.getenv('HOME'))
 	os.chdir("YCSB")
	writer, csv = create_output_file(outputdir,'ycsb',server)
	print "sleep for...", args[0]
	time.sleep(args[0])
	print "Already !! sleept for...", args[0]
	start = time.time()
	timeout = args[5] + start
	l = []
	l.append(args[1])
	l.append(str(datetime.now()))
	num = 0
	while True:
		print "************** Campaign",time.time(),"*********************"
		timetocheck = time.time() - start
		if timetocheck < args[5] :
			print "---------------------- process num", args[1],"----------------------------"
			vlist = [num, testname, workload, args[2], args[3] , args[4]]
			if server == 'mongodb':
				mongodb_url= "mongodb.url=mongodb://localhost:27017/ycsb?w=0"
				test_out = check_output(["./bin/ycsb", "run", server,"-s", "-P", workload,"-p",mongodb_url,"-threads",str(args[4]),"-p","recordcount="+str(args[3]),"-p","operationcount="+str(args[2])])
				print "###################",time.time()-timeout,"###################"
				if time.time() >= timeout:
					print "********************** process killed", args[1],"****************************"
					#Popproc.kill()
					l.append(str(datetime.now()))
					l.append('killed')
					break
			else:
				#test_out = check_output(["timeout",str(timeout),"./bin/ycsb", "run", server,"-s", "-P", workload,"-p",host,"-p",port,"-threads",str(args[4]),"-p","recordcount="+str(args[3]),"-p","operationcount="+str(args[2])])
				Popproc = subprocess.Popen(["./bin/ycsb", "run", server,"-s", "-P", workload,"-p",host,"-p",port,"-threads",str(args[4]),"-p","recordcount="+str(args[3]),"-p","operationcount="+str(args[2])],stderr=subprocess.PIPE, stdout=subprocess.PIPE)
				print "###################",time.time()-timeout,"###################"
				if time.time() >= timeout:
					print "********************** process killed", args[1],"****************************"
					Popproc.kill()
					l.append(str(datetime.now()))
					l.append('killed')
					break
				test_out = Popproc.communicate()[0]
 			click.echo(' \n The final results for iteration # {} are ...\n{}'.format(num+1 ,test_out))
 			write_ycsb_results(writer, csv, test_out, vlist)
 			num = num + 1
		else:
			print "********************** process terminated", args[1],"****************************"
			l.append(str(datetime.now()))
			l.append('terminated')
			break
	file = open('/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/workers.txt', "a")
	workerstatus = str(l) + '\n'
	file.write(workerstatus)
	file.close()
	close_csv(csv)


@click.command(short_help="Prints Presence's campaign test information.")
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
@click.option('-o','--oper', default='[500,700,900,1000,1500]',help='The number of operations per second.')
@click.option('-r','--rec', default='[200,300,400,600]',help='The number of records per second.')
@click.option('-td','--thrd', default='[1]',help='The number of threads.')
@click.option('-stime','--starttime', default= 0,help='The start time of the compaign, which is usually now.')
@click.option('-etime','--endtime', default= 100,help='The end time of the compaign.')

@click.option('--compcamp', flag_value=True, help='compelet Campaign Test.')
@click.option('--outputdir', default='/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Output/Campaign/',help='The directory for the output files (default:/home/git/../../presence/presence/cli/Output/Campaign).')
@click.option('--tempdir', default='/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/campaign',help='The directory for the saving files (default:/home/git/../../presence/presence/cli/Tmp/campaign).')


def campaign(oper,rec,thrd,starttime,endtime,ycsb,iperf,rpcperf,ab,httpload,pg,rbench,memt,redis,memcached,mongodb,apache,postegresql,iperfserver,compcamp,outputdir,tempdir):
	"""
    PRESENCE campaign commandline interface.

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
 		whenstart = time.time()
 		#prepare for the campaign
 		oper_values_list = eval(oper)
 		rec_values_list = eval(rec)
 		thrd_values_list = eval(thrd)
 		comblist = comb_ycsb_inputs(oper_values_list, rec_values_list, thrd_values_list)
 		camplist = generate_all_possible_campaigns(comblist, starttime, endtime, 'ycsb-redis')
 		Campaign_number = random.randint(1,101)
 		tempdir = tempdir + '#' + str(Campaign_number) +'ycsb-redis_%s.csv'% datetime.now()
 		write_campaigns_csv(camplist,tempdir)
 		stime = read_colume_csv(tempdir,'STime')
 		no_of_processes = len(stime)
 		listofprocesses = makeindex(no_of_processes)
 		#time_to_sleep = timetosleep(stime)
 		time_to_sleep = stime
 		dstatTime = 0
 		for t in range(len(stime)):
 			dstatTime = dstatTime + stime[t]
 		click.echo('dstat time = %s' % dstatTime)   
 		operations = read_colume_csv(tempdir,'No Operations')
 		records = read_colume_csv(tempdir,'No Records')
 		threads = read_colume_csv(tempdir,'No Threads')
 		stoptime = read_colume_csv(tempdir,'Disrubtion')
 		#Pre processing before ycsb
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
 			subprocess.call(["./bin/ycsb", "load", server,"-s", "-P", workLoad,"-p",host,"-p",port,"-threads",str(thrd_values_list[0]),"-p","recordcount="+str(rec_values_list[0]),"-p","operationcount="+str(oper_values_list[0])],stdout=subprocess.PIPE)
 			click.echo('\n----YCSB Redis Test is loaded----\n')
 		click.echo('\n----Run the YCSB Redis Test----\n')
 		# some manegment 
 		file = open('/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/workers.txt', "a")
 		newcampign = "***new campaign started***   " + str(datetime.now()) + '\n'
 		file.write(newcampign)
 		file.close()
 		#dstat start
 		campaigndstat = all_dstat(dstatTime + 20, 1, '/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/campaigndstat.csv')
 		#multi processing campagn
 		processespool = Pool(3) #no_of_processes 3
 		new_ycsb_campaign = partial(ycsb_campaign,host, port, server, workLoad,outputdir)
 		#click.echo(zip(time_to_sleep, listofprocesses, operations, records, threads, stoptime))
 		processespool.map(new_ycsb_campaign, zip(time_to_sleep, listofprocesses, operations, records, threads, stoptime))
 		processespool.terminate()
 		#done with parallelization
 		whenfinished = time.time()
 		#dstat finish
 		print_dstat(campaigndstat)
 		alltime = whenfinished - whenstart
 		click.echo('\n ----------- the whole Campaign time = %s ----------\n' % alltime)
 	elif ycsb and memcached:
 		whenstart = time.time()
 		#prepare for the campaign
 		oper_values_list = eval(oper)
 		rec_values_list = eval(rec)
 		thrd_values_list = eval(thrd)
 		comblist = comb_ycsb_inputs(oper_values_list, rec_values_list, thrd_values_list)
 		camplist = generate_all_possible_campaigns(comblist, starttime, endtime, 'ycsb-memcached')
 		Campaign_number = random.randint(1,101)
 		tempdir = tempdir + '#' + str(Campaign_number) +'ycsb-memcached_%s.csv'% datetime.now()
 		write_campaigns_csv(camplist,tempdir)
 		stime = read_colume_csv(tempdir,'STime')
 		no_of_processes = len(stime)
 		listofprocesses = makeindex(no_of_processes)
 		time_to_sleep = timetosleep(stime)
 		operations = read_colume_csv(tempdir,'No Operations')
 		records = read_colume_csv(tempdir,'No Records')
 		threads = read_colume_csv(tempdir,'No Threads')
 		stoptime = read_colume_csv(tempdir,'Disrubtion')
 		#Pre processing before ycsb
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
 			subprocess.call(["./bin/ycsb", "load", server,"-s", "-P", workLoad,"-p",host,"-p",port,"-threads",str(thrd_values_list[0]),"-p","recordcount="+str(rec_values_list[0]),"-p","operationcount="+str(oper_values_list[0])],stdout=subprocess.PIPE)
 			click.echo('\n----YCSB Memcached Test is loaded----\n')
 		click.echo('\n----Run the YCSB Memcached Test----\n')
 		# some manegment 
 		file = open('/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/workers.txt', "a")
 		newcampign = "***new campaign started***   " + str(datetime.now()) + '\n'
 		file.write(newcampign)
 		file.close()
 		#multi processing campagn
 		processespool = Pool(1)
 		new_ycsb_campaign = partial(ycsb_campaign,host, port, server, workLoad,outputdir)
 		#click.echo(zip(time_to_sleep, listofprocesses, operations, records, threads, stoptime))
 		processespool.map(new_ycsb_campaign, zip(time_to_sleep, listofprocesses, operations, records, threads, stoptime))
 		processespool.terminate()
 		#done with parallelization
 		whenfinished = time.time()
 		alltime = whenfinished - whenstart
 		click.echo('\n ----------- the whole Campaign time = %s ----------\n' % alltime)
 	elif ycsb and mongodb:
 		whenstart = time.time()
 		#prepare for the campaign
 		oper_values_list = eval(oper)
 		rec_values_list = eval(rec)
 		thrd_values_list = eval(thrd)
 		comblist = comb_ycsb_inputs(oper_values_list, rec_values_list, thrd_values_list)
 		camplist = generate_all_possible_campaigns(comblist, starttime, endtime, 'ycsb-mongodb')
 		Campaign_number = random.randint(1,101)
 		tempdir = tempdir + '#' + str(Campaign_number) +'ycsb-mongodb_%s.csv'% datetime.now()
 		write_campaigns_csv(camplist,tempdir)
 		stime = read_colume_csv(tempdir,'STime')
 		no_of_processes = len(stime)
 		listofprocesses = makeindex(no_of_processes)
 		#time_to_sleep = timetosleep(stime)
 		time_to_sleep = stime
 		operations = read_colume_csv(tempdir,'No Operations')
 		records = read_colume_csv(tempdir,'No Records')
 		threads = read_colume_csv(tempdir,'No Threads')
 		stoptime = read_colume_csv(tempdir,'Disrubtion')
 		#Pre processing before ycsb
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
 			subprocess.call(["./bin/ycsb", "load", server,"-s", "-P", workLoad,"-p",mongodb_url,"-threads",str(thrd_values_list[0]),"-p","recordcount="+str(rec_values_list[0]),"-p","operationcount="+str(oper_values_list[0])],stdout=subprocess.PIPE)
 			click.echo('\n----YCSB Mongodb Test is loaded----\n')
 		click.echo('\n----Run the YCSB Mongodb Test----\n')
 		# some manegment 
 		file = open('/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/workers.txt', "a")
 		newcampign = "***new campaign started***   " + str(datetime.now()) + '\n'
 		file.write(newcampign)
 		file.close()
 		#multi processing campagn
 		processespool = Pool(no_of_processes)
 		new_ycsb_campaign = partial(ycsb_campaign,host, port, server, workLoad,outputdir)
 		processespool.map(new_ycsb_campaign, zip(time_to_sleep, listofprocesses, operations, records, threads, stoptime))
 		processespool.terminate()
 		#done with parallelization
 		whenfinished = time.time()
 		alltime = whenfinished - whenstart
 		click.echo('\n ----------- the whole Campaign time = %s ----------\n' % alltime)
 	elif compcamp:
 		oper_values_list = eval(oper)
 		rec_values_list = eval(rec)
 		thrd_values_list = eval(thrd)
 		comblist = comb_ycsb_inputs(oper_values_list, rec_values_list, thrd_values_list)
 		camp1 = generate_all_possible_campaigns(comblist, starttime, endtime, 'ycsb-redis')
 		camp2 = generate_all_possible_campaigns(comblist, starttime + 10 , endtime, 'ycsb-memcached')
 		camp3 = generate_all_possible_campaigns(comblist, starttime + 20, endtime, 'ycsb-mongodb')
 		compeletcamplist = mixcamp([camp1,camp2,camp3])
 		click.echo(compeletcamplist)
 		Campaign_number = random.randint(1,101)
 		tempdir = tempdir + '#' + str(Campaign_number) +'completeCamp_%s.csv'% datetime.now()
 		write_campaigns_csv(compeletcamplist,tempdir)
 		stime = read_colume_csv(tempdir,'STime')
 		no_of_processes = len(stime)
 		listofprocesses = makeindex(no_of_processes)
 		time_to_sleep = timetosleep(stime)
 		operations = read_colume_csv(tempdir,'No Operations')
 		records = read_colume_csv(tempdir,'No Records')
 		threads = read_colume_csv(tempdir,'No Threads')
 		stoptime = read_colume_csv(tempdir,'Disrubtion')
 		bench_server = read_colume_csv(tempdir,'Bench')
 		benchlist, serverlist = splitlistofstring(bench_server, '-')
 		os.chdir(os.getenv('HOME'))
 		os.chdir("YCSB")
 		click.echo('Directory changed to ./YCSB/')
 		char = click.prompt('Did you run maven and load the YCSB test before [Y/n]?', type=str, default = 'y')
 		if char == 'n':
 			draft = call(["mvn", "-pl", "com.yahoo.ycsb:redis-binding", "-am", "clean","package"])
 			click.echo('\n ----Done with Maven----\n ')
 			click.echo('\n----Load the YCSB Redis Test----\n')
 			subprocess.call(["./bin/ycsb", "load", server,"-s", "-P", workLoad,"-p",host,"-p",port,"-threads",str(thrd_values_list[0]),"-p","recordcount="+str(rec_values_list[0]),"-p","operationcount="+str(oper_values_list[0])],stdout=subprocess.PIPE)
 			click.echo('\n----YCSB Redis Test is loaded----\n')
 		click.echo('\n----Run the YCSB Redis Test----\n')
 		# some manegment 
 		file = open('/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/Tmp/workers.txt', "a")
 		newcampign = "***new campaign started***   " + str(datetime.now()) + '\n'
 		file.write(newcampign)
 		file.close()
 		#multi processing campagn
 		#multi processing campagn
 		processespool = Pool(2)
 		new_complete_campaign = partial(complete_campaign,outputdir)
 		click.echo(zip(benchlist, serverlist, time_to_sleep, listofprocesses, operations, records, threads, stoptime))
 		processespool.map(new_complete_campaign, zip(benchlist, serverlist, time_to_sleep, listofprocesses, operations, records, threads, stoptime))
 		processespool.terminate()

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
 		click.echo('Usage: presence campaign [testing_tool][server] [options]\n')
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
 		click.echo('\n check the --help command:  presence campaign --help   \n')
 		#click.echo('All Presence default Values:')
 		#click.echo('operations %s !' % oper)
 		#click.echo('records %s !' % rec)
 		#click.echo('threads %s !' % thrd)
 	return