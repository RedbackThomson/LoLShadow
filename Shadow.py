from LoLChat import LoLChat
from ShadowUser import ShadowUser
from ShadowLogger import ShadowLogger

class Shadow:
	def __init__(self):
		self.current_alerts = {}
		self.alive = False

	def Start(self):
		self.lolchat = LoLChat(self, self.loldb, self.model.Username, self.model.Password)
		#Connect to the XMPP
		self.lolchat.Start()
		ShadowLogger.ShadowInfo("Started", self.model.SummonerName)
		self.alive = True

		#Reset Counters
		self.loldb.ResetOnlineUsers(self.model.ID)

	def Stop(self):
		for username, alert in self.current_alerts.iteritems():
			alert.Stop()
		self.current_alerts = {}
		ShadowLogger.ShadowInfo("Stopped", self.model.SummonerName)
		self.alive = False

	def UserOn(self, summoner_id):
		#try:
		if(summoner_id == str(self.model.SummonerID)): return
		user = self.loldb.GetUserBySummonerId(summoner_id, self.model.ID)
		if(user == None): 
			#Freeloader
			self.SendMessage(summoner_id, "This summoner has not been configured.")
			self.lolchat.UnFriend(summoner_id)
			return
		if(user.Active == 0):
			return

		username = user.TwitchUsername
		self.CheckUserNotices(user, summoner_id)

		ShadowLogger.ShadowInfo('User Online: %s @ %s' % (str(username),str(summoner_id)), self.model.SummonerName)
		if(username in self.current_alerts): 
			#Chat might have reset - no need to restart the whole thread service
			self.current_alerts[username].Stop()
			del self.current_alerts[username]

		self.current_alerts[username] = ShadowUser(self.SendNewFollow, username, summoner_id, user.TwitchToken)
		self.current_alerts[username].Start()
		self.loldb.SetOnlineUsers(len(self.current_alerts), self.model.ID)
		#except Exception, e:
			#ShadowLogger.ShadowError(str(e), self.model.SummonerName)

	def UserOff(self, summoner_id):
		if(summoner_id == self.model.SummonerID): return
		user = self.loldb.GetUserBySummonerId(summoner_id)
		if(user == None): return
		username = user.TwitchUsername

		ShadowLogger.ShadowInfo('User Offline: ' + str(username) + '@' + str(summoner_id), self.model.SummonerName)
		if(username in self.current_alerts): 
			self.current_alerts[username].Stop()
			del self.current_alerts[username]

		self.loldb.SetOnlineUsers(len(self.current_alerts), self.model.ID)

	def SendMessage(self, target, message):
		self.lolchat.SendMessage(target, message)

	def SendNewFollow(self, target, new_follow):
		#Send new follow message
		self.loldb.IncrementTotalFollowed(self.model.ID)
		message = '{} has just followed!'.format(new_follow)
		self.SendMessage(target, message)

	def CheckUserNotices(self, user, summoner_id):
		lastNotice = user.LastNotice
		latestNotice = self.loldb.GetLatestNotice()
		#Hasn't received the latest message
		if (latestNotice.ID > lastNotice):
			self.lolchat.SendMessage(summoner_id, '[Notice] %s' % latestNotice.Message)
			self.loldb.UpdateNotice(user.ID, latestNotice.ID)

	def Broadcast(self, message):
		for username, alert in self.current_alerts.iteritems():
			ShadowLogger.ShadowInfo('Sending broadcast to %s' % (username), self.model.SummonerName)
			self.SendMessage(alert.summoner_id, message)

	def GetOnline(self):
		return self.current_alerts.keys()

	def Restart(self):
		for username, alert in self.current_alerts.iteritems():
			alert.Stop()
		self.current_alerts = {}