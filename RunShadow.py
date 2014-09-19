from datetime import datetime
import re
import subprocess
import os, inspect
import time

pidpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
pidfile = os.path.join(pidpath, 'tmp_shadow.pid')

def isRunning(process):
	s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
	for x in s.stdout:
		if re.search(process, x):
			return True

	return False

def startProcess():
	print str(datetime.now()) + ' Starting a new instance...'
	os.system('python LoLShadow.py &')

if __name__ == '__main__':
	while (True):
		try:
			with open(pidfile, 'r') as f:
				pid = f.read()

			if(not isRunning(pid)):
				startProcess()
		except Exception, e:
			print e
		time.sleep(5)