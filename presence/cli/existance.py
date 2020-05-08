from subprocess import call, STDOUT
import os
import subprocess
from distutils.spawn import find_executable


def is_git_directory(path = '.'):
    return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0


def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def where_is(name):
    if find_executable(name):
        path = find_executable(name)
        print(name + ' server/testing tool is installed in the following path: '+ "'"+path+"'")
        return True
    else:
        print('%s server/testing tool is not installed in your system' % name)
        return False
		 
def is_exist(name):
    os.chdir(os.getenv('HOME'))
    if os.path.isdir(name):
        os.chdir(name)
        path = os.getcwd()
        print(name + ' respository/directory  is existing in the following path: '+ "'"+path+"'")
        return True
    else:
        print('%s respository/directory  doesn not exist in your /HOME/..' % name)
        return False

def check_server(name):
    print("\n")
    subprocess.call(['sudo', 'service', name, 'status'], stderr=subprocess.STDOUT, stdout = True)
    print("\n\n The server connection: \n")
    subprocess.call(['sudo', 'netstat', '-naptu',' | ','grep', name], stderr=subprocess.STDOUT, stdout = True)



