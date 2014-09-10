class SummonerModel:
	def __init__(self, dbRow):
		self.ID = dbRow["ID"]
		self.User = dbRow["User"]
		self.SummonerName = dbRow["SummonerName"]
		self.SummonerID = dbRow["SummonerID"]
		self.Shadow = dbRow["Shadow"]
		self.Region = dbRow["Region"]
		self.Timestamp = dbRow["Timestamp"]