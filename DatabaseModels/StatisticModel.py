class StatisticModel:
	def __init__(self, dbRow):
		self.Key = dbRow["Key"]
		self.Value = dbRow["Value"]
		self.Timestamp = dbRow["Timestamp"]