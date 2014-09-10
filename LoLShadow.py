#!/usr/bin/python

import os
import inspect
import json
import time

from ShadowLogger import ShadowLogger
from LoLDB import LoLDB
from Shadow import Shadow
from DatabaseModels.ShadowModel import ShadowModel

class LoLShadow:
	def __init__(self):
		ShadowLogger.InitLogger()
		self.loldb = LoLDB()
		self.LoadDatabaseSettings()
		self.loldb.Connect()
		ShadowLogger.Info('Connected to DB')

	def LoadDatabaseSettings(self):
		settingsFile = open('conf/settings.json', 'r')
		settings = json.loads(settingsFile.read())
		dbSettings = settings['database']

		self.loldb.login_host = dbSettings['host']
		self.loldb.login_user = dbSettings['user']
		self.loldb.login_pass = dbSettings['pass']
		self.loldb.login_db = dbSettings['db']

	def Start(self):
		#Get all shadows
		shadows = self.loldb.GetAllShadows()

		self.shadows = []
		#Popping in a test shadow
		for shadow in shadows:
			newShadow = Shadow()
			newShadow.loldb = self.loldb
			newShadow.model = ShadowModel(shadow)
			self.shadows.append(newShadow)

		#Shadow enabled polling
		self.enabledThread = True
		self.EnabledPoll()

	def Stop(self):
		self.enabledThread = False
		for shadow in self.shadows:
			shadow.Stop()
		self.loldb.Close()

	def EnabledPoll(self):
		while self.enabledThread:
			for shadow in self.shadows:
				enabled = self.loldb.GetShadowEnabled(shadow.model.ID)
				if enabled and not shadow.alive:
					shadow.Start()
				elif not enabled and shadow.alive:
					shadow.Stop()
			time.sleep(5)

def checkPidRunning(pid):        
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def writePID():
	pid = str(os.getpid())
	pidpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	pidfile = os.path.join(pidpath, 'tmp_shadow.pid')

	if os.path.isfile(pidfile) and checkPidRunning(int(file(pidfile,'r').readlines()[0])):
		print "%s already exists, exiting" % pidfile
		sys.exit()
	else:
		file(pidfile, 'w').write(pid)

#Entry Point
if __name__ == '__main__':
	writePID()

	lolShadow = LoLShadow()
	lolShadow.Start()