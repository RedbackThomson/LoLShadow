class ShadowStatisticModel:
	def __init__(self, dbRow):
		self.Shadow = dbRow["Shadow"]
		self.OnlineUsers = dbRow["OnlineUsers"]
		self.TotalFollowed = dbRow["TotalFollowed"]
		self.Timestamp = dbRow["Timestamp"]