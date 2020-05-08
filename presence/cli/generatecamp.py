import random
import csv
import time 
from datetime import datetime
import time 
import os

# functions

def comb_ycsb_inputs(operlist, reclist, thrdlist):
	"""function to get the combination of the input's values, 
	help: the number of loops depends on the number of parameters"""
	list = []
	templist = []
	for i in operlist:
		for j in reclist:
			for k in thrdlist:
				templist = [i,j,k]
				list.append(templist)
	return list


def generate_all_possible_campaigns(inputlist, starttime, endtime, bench):
	t0 = []
	if endtime < len(inputlist):
		endtime = len(inputlist)
		print "The time is not enough for generate all the inputs, increase the end time !"
		exit(50)
	t0 = random.sample(range(starttime, endtime), len(inputlist))
	t = random.sample(range(starttime + 10, endtime), len(inputlist))
	list = []
	for x in range(len(inputlist)):
		tmplist = []
		tmplist.append(t0[x])
		tmplist.append(t[x])
		tmplist.append(bench)
		for y in range(len(inputlist[x])):
			tmplist.append(inputlist[x][y])
		list.append(tmplist)
	list.sort()
	return list

def write_campaigns(listofcampaigns, filepath):
	file = open(filepath, "w")
	for x in range(len(listofcampaigns)):
		L = str(listofcampaigns[x]) + '\n'
		file.writelines(L)

def write_campaigns_csv(listofcampaigns, filepath):
	csvfile = open(filepath, 'w')
	fieldnames = ['STime','Disrubtion','Bench','No Operations','No Records','No Threads']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for x in range(len(listofcampaigns)):
		L = listofcampaigns[x]
		writer.writerow({'STime':L[0],'Disrubtion':L[1],
			'Bench':L[2],'No Operations':L[3],'No Records':L[4],'No Threads':L[5]})

def read_campaigns(filepath):
	list = []
	file = open(filepath, "r")
	for x in file:
		tmp = x
		list.append(tmp)
	return list
def read_campaigns_csv(filepath):
	list = []
	with open(filepath, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			tmplist = []
			tmplist.append(int(row['STime']))
			tmplist.append(int(row['Disrubtion']))
			tmplist.append(row['Bench'])
			tmplist.append(int(row['No Operations']))
			tmplist.append(int(row['No Records']))
			tmplist.append(int(row['No Threads']))
			list.append(tmplist)
	return list

def read_colume_csv(filepath, colnam):
	list = []
	with open(filepath, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if colnam == 'Bench':
				list.append(row[colnam])
			else:
				list.append(int(row[colnam]))
	return list

def differnce_list(list):
	difflist = [0]
	for i in range(len(list)-1):
		dif = list[i+1] - list[i]
		difflist.append(dif)
	return difflist

def timetosleep(list):
	if list[0] == 0:
		return list
	else:
		difflist = []
		for i in range(len(list)):
			dif = list[i] - list[0]
			difflist.append(dif)
		return difflist

def makeindex(num):
	return list(range(num))


def mixcamp(args):
	list = []
	for num in range(len(args)):
		list = list + args[num]
	list.sort()
	return list

def splitlistofstring(list, char):
	listl = []
	listr = []
	for i in range(len(list)):
		left, right = list[i].split(char)
		listl.append(left)
		listr.append(right)
	return listl, listr

#___Main____


# l1 = [1,2,3]
# l2 = [4,5,10]
# l3 = [6,7,5]


# test = comb_ycsb_inputs(l1,l2,l3)
# print(test)



# gen = generate_all_possible_campaigns(test, 0, 100,'ycsb')

# for x in range(len(gen)):
# 	print gen[x]
# 	print "\n"

# write_campaigns(gen,'hello.txt')
# write_campaigns_csv(gen,'hello.csv')
# camplist = read_campaigns('hello.txt')
# print camplist[26][1]
# new = read_campaigns_csv('hello.csv')
# stime = read_colume_csv('hello.csv','STime')
# print stime

# difflist = [0]
# for i in range(len(stime)-1):
# 	dif = stime[i+1] - stime[i]
# 	difflist.append(dif)

# print difflist, len(difflist), len(stime)

