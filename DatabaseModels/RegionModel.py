class RegionModel:
	def __init__(self, dbRow):
		self.ID = dbRow["ID"]
		self.RegionName = dbRow["RegionName"]
		self.RegionCode = dbRow["RegionCode"]
		self.RegionChat = dbRow["RegionChat"]