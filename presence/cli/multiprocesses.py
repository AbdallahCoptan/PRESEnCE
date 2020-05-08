from multiprocessing import Process
from multiprocessing import Pool
from subprocess import check_output
from itertools import product
from functools import partial
import os
import time

def info(title):
    #print title
    #print 'module name:', __name__
    #if hasattr(os, 'getppid'):  # only available on Unix
        #print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def f(stre,args):
    info('function f')
    #test = check_output(["ab","-n",'20',"-c",'5','http://127.0.0.1:80/'])
    time.sleep(args[1])
    print "sleep for ", args[1]
    start = time.time()
    for x in range(args[2]):
        if time.time() - start < args[3] :
            print stre, "-----------running num", args[0]
            test = check_output(["ab","-n",'20',"-c",'5','http://127.0.0.1:80/'])
            print test
    	else:
    		print "*********process terminated", args[0]
    		break

if __name__ == '__main__':
    #pname = 'p'+ str(num)
    #info('main line')
    p = Pool(5)
    list1 = [1,2,3,6,7]
    list2 = [3,3,3,3,3]
    list3 = [5,5,5,5,5]
    list4 = [1,1,1,1,1]
    process = "process"
    f2 = partial(f,process)
    p.map(f2, zip(list1, list2,list3,list4))
    #pname = Process(target=f, args=(num,))
    #pname.start()
    #time.sleep(5)
    #pname.join()