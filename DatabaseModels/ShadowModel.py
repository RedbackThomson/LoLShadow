class ShadowModel:
	def __init__(self, dbRow):
		self.ID = dbRow["ID"]
		self.Username = dbRow["Username"]
		self.Region = dbRow["Region"]
		self.SummonerID = dbRow["SummonerID"]
		self.SummonerName = dbRow["SummonerName"]
		self.Password = dbRow["Password"]
		self.Email = dbRow["Email"]
		self.Message = dbRow["Message"]
		self.Enabled = dbRow["Enabled"]