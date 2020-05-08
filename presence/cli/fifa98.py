import random
import csv
import time 
from datetime import datetime
import time 
import csv
import os

#datetime_object = datetime.strptime('30/Apr/1998:22:00:03', '%d/%b/%Y:%H:%M:%S')

filepath = '/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/fifa98/recreat.out'
list = []
file = open(filepath, "r")
for x in file:
	tmp = x
	list.append(tmp)
userslist = []
datelist = []
httpcodelist = []
sizelist = []
for num in range(len(list)- 1193320):
	tem = list[num].split(' ')
	userslist.append(int(tem[0]))
	tem1 = tem[3].split('[')
	datelist.append(tem1[1])
	httpcodelist.append(int(tem[8]))
	tem2 = tem[9].split('\n')
	sizelist.append(int(tem2[0]))


csvfile = open("/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/fifa98/FIFA98Anlaysis%s.csv"% datetime.now(), 'w')

fieldnames = ['time','user','requestsize', 'httpcode']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
for num in range(len(list)- 1193320):
	writer.writerow({'time':datelist[num],'user':userslist[num],'requestsize':sizelist[num],'httpcode':httpcodelist[num]})