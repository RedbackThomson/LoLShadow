from FollowerFetcher import FollowerFetcher
from ShadowLogger import ShadowLogger

class ShadowUser:
	def __init__(self, newfollow_callback, user, summoner_id, redis):
		self.user = user
		self.summoner_id = summoner_id
		self.newfollow_callback = newfollow_callback
		self.followFetcher = FollowerFetcher(self.SendMessage, user, redis)

	def Start(self):
		#Create a connection to the base
		self.followFetcher.Start()

	def Stop(self):
		self.followFetcher.alive = False

	def SendMessage(self, newfollow_username):
		self.newfollow_callback(self.user, self.summoner_id, newfollow_username)