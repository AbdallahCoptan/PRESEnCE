import csv
import time 
from datetime import datetime
import time 
import os



def create_output_file(directory, test, tool, fieldnames= None):
	filename = directory + test + '_' + tool +'_%s.csv'% datetime.now()
	csvfile = open(filename, 'w')
	if fieldnames == None:
		if test == 'ycsb': 
			fieldnames = ['count','Date','ExpName', 'WorkLoad','No Operations','No Records','No_Threads','Runtime(ms)','Thr(ops/sec)',
			'cleanup_lat(us)','readFail_lat(us)','Read_ReturnOk','Read_ReturnErr','read_lat(us)','update_lat(us)']
		if test == 'httpload':
			fieldnames = ['count','Date','ExpName', 'No Fetches','Parallel_con','total_kbytes','total_time/sec','avg_kB/conn','fetches/sec',
			'Kbytes/sec','avg_msec/connection','avg_msec/first_response']
		if test == 'memtier':
			fieldnames = ['count','Date','ExpName', 'No Requests','Parallel_con','WorkLoad_size','No_Threads','ops/sec','hits/sec','miss/sec','latency','TR: kb/sec']
		if test == 'pgbench':
			fieldnames = ['count','Date','ExpName', 'DB Size','Parallel Clients','Num_Threads','Num_Transactions/client','#TransActuallyProcessed',
			'TPS/incConn','TPS/excConn','Avg Latency/AllStatments(ms)']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	return writer, csvfile


def write_ycsb_results(writer, csvfile, test_out, vlist):
	if test_out == '':
		return 0
	a = test_out.split('\n')
	list = []
	listb = []
	for g in range (0, len(a)):
		e = a[g].split(', ')
		if ((e[0] == '[OVERALL]' and e[1] == 'RunTime(ms)') 
		or (e[0] == '[OVERALL]' and e[1] == 'Throughput(ops/sec)') 
		or (e[0] == '[CLEANUP]' and e[1] == 'AverageLatency(us)') 
		or (e[0] == '[READ]' and e[1] == 'AverageLatency(us)') 
		or (e[0] == '[UPDATE]' and e[1] == 'AverageLatency(us)') 
		or (e[0] == '[READ-FAILED]' and e[1] =='AverageLatency(us)') 
		or (e[0] =='[READ]' and e[1] == 'Return=OK') 
		or (e[0] =='[READ]' and e[1] == 'Return=ERROR')):
			list.append(g)
			listb.append(float(e[2]))
	if len(listb) == 6:
		writer.writerow({'count':vlist[0],'Date':time.strftime("%d/%m/%Y"),
			'ExpName':vlist[1],'WorkLoad':vlist[2],'No Operations':vlist[3],'No Records':vlist[4],'No_Threads':vlist[5],
			'Runtime(ms)':listb[0],'Thr(ops/sec)':listb[1],'cleanup_lat(us)':listb[2],'readFail_lat(us)':'NULL','Read_ReturnOk':listb[4],
			'Read_ReturnErr':'NULL','read_lat(us)':listb[3],'update_lat(us)':listb[5]})
	elif len(listb) < 6 and vlist[2] == "workloads/workloadc":
		writer.writerow({'count':vlist[0],'Date':time.strftime("%d/%m/%Y"),
			'ExpName':vlist[1],'WorkLoad':vlist[2],'No Operations':vlist[3],'No Records':vlist[4],'No_Threads':vlist[5],
			'Runtime(ms)':listb[0],'Thr(ops/sec)':listb[1],'cleanup_lat(us)':listb[2],'readFail_lat(us)':'NULL','Read_ReturnOk':listb[4],
			'Read_ReturnErr':'NULL','read_lat(us)':listb[3],'update_lat(us)':'NULL'})
	elif len(listb) < 8 and vlist[2] == "workloads/workloadc":
		writer.writerow({'count':vlist[0],'Date':time.strftime("%d/%m/%Y"),
			'ExpName':vlist[1],'WorkLoad':vlist[2],'No Operations':vlist[3],'No Records':vlist[4],'No_Threads':vlist[5],
			'Runtime(ms)':listb[0],'Thr(ops/sec)':listb[1],'cleanup_lat(us)':listb[3],'readFail_lat(us)':listb[2],'Read_ReturnOk':listb[5],
			'Read_ReturnErr':listb[6],'read_lat(us)':listb[4],'update_lat(us)':'NULL'})
	else:
		writer.writerow({'count':vlist[0],'Date':time.strftime("%d/%m/%Y"),
			'ExpName':vlist[1],'WorkLoad':vlist[2],'No Operations':vlist[3],'No Records':vlist[4],'No_Threads':vlist[5],
			'Runtime(ms)':listb[0],'Thr(ops/sec)':listb[1],'cleanup_lat(us)':listb[3],'readFail_lat(us)':listb[2],'Read_ReturnOk':listb[5],
			'Read_ReturnErr':listb[6],'read_lat(us)':listb[4],'update_lat(us)':listb[7]})


def write_httpload_results(writer, test_out, vlist):
	a = test_out.split('\n')
	l0 = a[0].split(' ')
	l1 = a[1].split(' ')
	l2 = a[2].split(' ')
	l3 = a[3].split(' ')
	l4 = a[4].split(' ')
	l5 = a[5].split(' ')
	total_kbytes = float(l0[5]) / 1024
	total_time_sec = float(l0[8])
	avg_kB_conn = float(l1[0]) / 1024
	fetches_sec = float(l2[0])
	Kbytes_sec = float(l2[2]) / 1024
	avg_msec_connection = float(l3[1])
	avg_msec_first_response = float(l4[1])
	writer.writerow({'count':vlist[0],'Date':time.strftime("%d/%m/%Y"),
		'ExpName':vlist[1],'No Fetches':vlist[2], 'Parallel_con': vlist[3],'total_kbytes':total_kbytes,'total_time/sec':total_time_sec,
		'avg_kB/conn':avg_kB_conn,'fetches/sec':fetches_sec,'Kbytes/sec':Kbytes_sec,'avg_msec/connection':avg_msec_connection,
		'avg_msec/first_response':avg_msec_first_response})



def write_memtier_results(writer, test_out, vlist):
	a = test_out.split('---\nTotals')
	b = a[1].split(' ')
	list = []
	for k in range (0, len(b)):
		if b[k] != '':
			f = float(b[k])
			list.append(f)
	writer.writerow({'count':vlist[0],'Date':time.strftime("%d/%m/%Y"),
		'ExpName':vlist[1],'No Requests':vlist[2], 'Parallel_con': vlist[3],'WorkLoad_size':vlist[4] ,'No_Threads': vlist[5] ,
		'ops/sec':list[0] ,'hits/sec': list[1],'miss/sec':list[2],'latency':list[3],'TR: kb/sec':list[4]})


def get_factors(x):
	""" This function takes a number and returns its factors"""
	listf = []
	#print("The factors of",x,"are:")
	for i in range(1, x + 1):
		if x % i == 0:
			#print(i)
			listf.append(i)
	return listf


def write_pgbench_results(writer, test_out, vlist):
	a = test_out.split('\n')
	for s in range(0, len(a)):
		if a[s] == 'statement latencies in milliseconds:':
			x = s + 1
	list = []
	for d in range(x, len(a)-1):
		list.append(a[d])
	listl = []
	lat = 0
	for g in range(0, len(list)):
		c = list[g].split("\t")
		listl.append(float(c[1]))
		lat = lat + listl[g]
	f = a[6].split(" ")
	f = f[len(f)-1]
	u = ""
	y = ""
	for h in range(0,len(f)):
		if f[h] != '/' and h < len(f)/2 :
			u = str(u) + f[h]
		if f[h] != '/' and h > len(f)/2 :
			y = str(y) + f[h]
	m1 = a[7].split(" ")
	m2 = a[8].split(" ")
	m1 = float(m1[2]) # TPS including connections establishing
	m2 = float(m2[2]) # TPS excluding connections establishing
	writer.writerow({'count':vlist[0],'Date':time.strftime("%d/%m/%Y"),'ExpName':vlist[1],
		'DB Size':vlist[2],'Parallel Clients': vlist[3] ,'Num_Threads':vlist[4],'Num_Transactions/client':vlist[5],
		'#TransActuallyProcessed':float(u),'TPS/incConn':m1,'TPS/excConn':m2,'Avg Latency/AllStatments(ms)':float(lat)})

def close_csv(csvfile):
	csvfile.close()