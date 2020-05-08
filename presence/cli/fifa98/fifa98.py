import random
import csv
import time 
from datetime import datetime,timedelta
#import datetime
#from datetime import datetime
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
datelist2 = []
httpcodelist = []
sizelist = []   #-1193330
for num in range(len(list)):
	tem = list[num].split(' ')
	userslist.append(int(tem[0]))
	tem1 = tem[3].split('[')
	datelist.append(tem1[1])
	datelist2.append(tem1[1])
	if tem[8] == '-':
		httpcodelist.append(200)
	else:
		httpcodelist.append(int(tem[8]))
	tem2 = tem[9].split('\n')
	#print tem2
	if tem2[0] == '-':
		sizelist.append(0)
		#print 'worked'
	else:
		sizelist.append(int(tem2[0]))

#writing fifa analysis
csvfile = open("/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/fifa98/FIFA98Anlaysis%s.csv"% datetime.now(), 'w')

fieldnames = ['time','user','requestsize', 'httpcode']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
for num in range(len(list)):  #-1193330
	writer.writerow({'time':datelist[num],'user':userslist[num],'requestsize':sizelist[num],'httpcode':httpcodelist[num]})

#calculate the throughput
count = 0
cumsize = 0
uniqdatelist = []
hitslist = []
cumsizelist = []
datelist2.append('the lastlast one') 
print len(datelist), len(datelist2)
#print datelist, datelist2
for x in range(len(datelist)):
	if datelist[x] == datelist2[x+1]:
		count = count + 1
		cumsize =  cumsize + sizelist[x]
	else:
		count = count + 1
		cumsize =  cumsize + sizelist[x]
		uniqdatelist.append(datelist[x])
		hitslist.append(count)
		cumsizelist.append(cumsize)
		count = 0
		cumsize = 0

#calculate the throuhput
realtimelist = []
realtimelist2 = []
for enum in range(len(uniqdatelist)):
	datetime_object = datetime.strptime(uniqdatelist[enum], '%d/%b/%Y:%H:%M:%S')
	realtimelist.append(datetime_object)
	realtimelist2.append(datetime_object)
	
tmpvalue = len(realtimelist) -1
onesec = timedelta(0,1)
lasttime = realtimelist2[tmpvalue] + onesec
realtimelist2.append(lasttime)

print len(realtimelist), len(realtimelist2)
throughput = 0
throughputlist = []
epochtimelist = []
for t in range(len(realtimelist)):
	differnce = realtimelist2[t+1] - realtimelist[t]
	epch = realtimelist[t].strftime('%s')
	epochtimelist.append(epch)
	throughput = cumsizelist[t] / differnce.total_seconds()
	#print throughput, throughput/1000
	throughputlist.append(throughput)   

throughputlist[:] = [itr / 1000 for itr in throughputlist]

###dettermining the peakes
peakslist = [None] * len(throughputlist)
peakslist2 = []
epochlist = []
normaltimelist = []
requestslist = []
for pek in range(len(throughputlist)):
	if throughputlist[pek] > 2300:
		peakslist[pek] = throughputlist[pek]
		peakslist2.append(throughputlist[pek])
		epochlist.append(epochtimelist[pek])
		normaltimelist.append(realtimelist[pek])
		requestslist.append(hitslist[pek])




#writing fifa throughput
#csvfile = open("/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/fifa98/FIFA98Throughput%s.csv"% datetime.now(), 'w')

#fieldnames = ['time','epochTime','throughput(kbyts/sec)', 'numofrequests(hits/sec)', 'peaks']
#writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#writer.writeheader()
#for num in range(len(uniqdatelist)):
	#writer.writerow({'time':uniqdatelist[num],'epochTime':epochtimelist[num],'throughput(kbyts/sec)':throughputlist[num],'numofrequests(hits/sec)':hitslist[num], 'peaks':peakslist[num]})

#writing fifa throughput peaks
#csvfile = open("/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/fifa98/FIFA98Peaks.csv", 'w')

#fieldnames = ['time','epochTime','requests','peaks']
#writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#writer.writeheader()
#for num in range(len(normaltimelist)):
	#writer.writerow({'time':normaltimelist[num],'epochTime':epochlist[num],'requests':requestslist[num],'peaks':peakslist2[num]})


peakslist = [None] * len(throughputlist)
peakslist2 = []
epochlist = []
normaltimelist = []
requestslist = []
for pek in range(len(throughputlist)):
	if throughputlist[pek] < 2000 and throughputlist[pek] > 1000:
		peakslist[pek] = throughputlist[pek]
		peakslist2.append(throughputlist[pek])
		epochlist.append(epochtimelist[pek])
		normaltimelist.append(realtimelist[pek])
		requestslist.append(hitslist[pek])


#writing fifa throughput other peaks
#csvfile = open("/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/fifa98/FIFA98Peaksss.csv", 'w')

#fieldnames = ['time','epochTime','requests','peaks']
#writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#writer.writeheader()
#for num in range(len(normaltimelist)):
	#writer.writerow({'time':normaltimelist[num],'epochTime':epochlist[num],'requests':requestslist[num],'peaks':peakslist2[num]})

peakslist = [None] * len(throughputlist)
peakslist2 = []
epochlist = []
normaltimelist = []
requestslist = []
for pek in range(len(throughputlist)):
	if throughputlist[pek] < 3600 and throughputlist[pek] > 2300:
		peakslist[pek] = throughputlist[pek]
		peakslist2.append(throughputlist[pek])
		epochlist.append(epochtimelist[pek])
		normaltimelist.append(realtimelist[pek])
		requestslist.append(hitslist[pek])


#writing fifa throughput other peaks
csvfile = open("/home/abdallah/git/gitlab.uni.lu/aibrahim/presence/presence/cli/fifa98/FIFA98Peaks_object.csv", 'w')

fieldnames = ['time','epochTime','requests','peaks']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
for num in range(len(normaltimelist)):
	writer.writerow({'time':normaltimelist[num],'epochTime':epochlist[num],'requests':requestslist[num],'peaks':peakslist2[num]})