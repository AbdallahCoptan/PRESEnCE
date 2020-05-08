import random
import csv
import time 
from datetime import datetime
import time 
import os
import subprocess
from subprocess import call
from subprocess import check_output
from subprocess import Popen

def all_dstat(completetime, frequenttime, outputfiledirectory):
	Popproc = subprocess.Popen(["dstat", "-t","-cdmnl", "--output", outputfiledirectory,str(frequenttime),str(completetime)],stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	#if you want to see the output
	#L = ["dstat", "-t","-cdmnl", "--output", outputfiledirectory ,str(frequenttime),str(completetime)]
	#os.spawnvpe(os.P_NOWAIT, 'dstat',L,  os.environ)
	#print "it works"
	#print "sleep for half time"
	#time.sleep(completetime/2)
	#print "already sleept for half time"
	#print "sleep again"
	#time.sleep((completetime/2) + 2)
	#print "now should be finished and output is: \n"
	#print Popproc.communicate()[0]
	return Popproc

def print_dstat(Popproc):
	print Popproc.communicate()[0]




