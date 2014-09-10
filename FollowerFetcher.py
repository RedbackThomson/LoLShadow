import urllib2
import json
import time
import threading
import math
from ShadowLogger import ShadowLogger
from Constants import Constants

class FollowerFetcher:
	def __init__(self, newfollow_callback, twitch_username, token):
		self.token = token
		self.twitch_username = twitch_username
		self.newfollow_callback = newfollow_callback
	
	def Start(self):
		self.alive = True
		self.run_thread = threading.Thread(target = self._run, args=())
		self.run_thread.start()

	def _run(self):
		errorTime = 0
		self.followed = []
		while(self.alive):
			time.sleep(5)
			current_subs = self._getLatestFollower()
			
			if(current_subs is None):
				errorTime += 1
				time.sleep(60.011*(1-5.159*math.exp(-1.9284*errorTime)))
				continue	
			
			for current_sub in current_subs:
				errorTime = 0
				current_id = current_sub['user']['_id']
				if(not self.followed):
					self.followed.append(current_id)
				else:
					if(current_id not in self.followed):
						self.followed.append(current_id)
						self.newfollow_callback(current_sub['user']['display_name'])

	def _getLatestFollower(self):
		url = Constants.FOLLOWER_URI.format(self.twitch_username, 1)
		try:
			response = urllib2.urlopen(url)
			return self._parseLatestFollower(response.read())
		except Exception as e:
			ShadowLogger.Debug("(%s): %s" % (self.twitch_username, ("Error getting follower: %s" % (e))))
			return None

	def _parseLatestFollower(self, jsonData):
		follows = json.loads(jsonData)
		return follows['follows']

	def _throwError(self, message):
		ShadowLogger.Error(message)	