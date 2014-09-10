from FollowerFetcher import FollowerFetcher
from ShadowLogger import ShadowLogger

class ShadowUser:
	token, twitch_username, summoner_id, newfollow_callback = "", "", "", ""

	def __init__(self, newfollow_callback, twitch_username, summoner_id, token):
		self.token = token
		self.twitch_username = twitch_username
		self.summoner_id = summoner_id
		self.newfollow_callback = newfollow_callback
		self.followFetcher = FollowerFetcher(self.SendMessage, twitch_username, token)

	def Start(self):
		#Create a connection to the base
		self.followFetcher.Start()

	def Stop(self):
		self.followFetcher.alive = False

	def SendMessage(self, newfollow_username):
		ShadowLogger.Info('Sending %s to %s' % (newfollow_username, self.twitch_username))
		self.newfollow_callback(self.summoner_id, newfollow_username)