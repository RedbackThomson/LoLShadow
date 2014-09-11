import urllib2
import json
import time
import threading
import math
from ShadowLogger import ShadowLogger
from Constants import Constants

class FollowerFetcher:
	def __init__(self, newfollow_callback, user, lolredis):
		self.user = user
		self.lolredis = lolredis
		self.newfollow_callback = newfollow_callback
	
	def Start(self):
		self.alive = True
		self.first = True #First follower on startup
		self.run_thread = threading.Thread(target = self._run, args=())
		self.run_thread.start()

	def _run(self):
		errorTime = 0
		while(self.alive):
			current_subs = self._getLatestFollower()
			
			if(current_subs is None):
				errorTime += 1
				time.sleep(60.011*(1-5.159*math.exp(-1.9284*errorTime)))
				continue	
			
			for current_sub in current_subs:
				errorTime = 0
				if(self.first):
					self.lolredis.DumpFollow(self.user, current_sub['user']['name'])
					self.first = False
				else:
					if(not self.lolredis.HasFollower(self.user, current_sub['user']['name'])):
						self.lolredis.NewFollow(self.user, current_sub['user']['name'])
						self.newfollow_callback(current_sub['user']['display_name'])

			time.sleep(5)

	def _getLatestFollower(self):
		url = Constants.FOLLOWER_URI.format(self.user.TwitchUsername, 1)
		try:
			response = urllib2.urlopen(url)
			return self._parseLatestFollower(response.read())
		except Exception as e:
			ShadowLogger.Debug("(%s): %s" % (self.user.TwitchUsername, ("Error getting follower: %s" % (e))))
			return None

	def _parseLatestFollower(self, jsonData):
		follows = json.loads(jsonData)
		return follows['follows']

	def _throwError(self, message):
		ShadowLogger.Error(message)	