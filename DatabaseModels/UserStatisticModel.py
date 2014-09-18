class UserStatistic:
	def __init__(self, dbRow):
		self.User = dbRow["User"]
		self.TotalSubscribed = dbRow["TotalSubscribed"]