class ShadowFriendModel:
	def __init__(self, dbRow):
		self.ID = dbRow["ID"]
		self.Shadow = dbRow["Shadow"]
		self.SummonerID = dbRow["SummonerID"]