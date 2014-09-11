class UserModel:
	def __init__(self, dbRow):
		self.ID = dbRow["ID"]
		self.APIKey = dbRow["APIKey"]
		self.TwitchUsername = dbRow["TwitchUsername"]
		self.TwitchDisplay = dbRow["TwitchDisplay"]
		self.TwitchToken = dbRow["TwitchToken"]
		self.RefreshToken = dbRow["RefreshToken"]
		self.Timestamp = dbRow["Timestamp"]
		self.LastNotice = dbRow["LastNotice"]
		self.Active = dbRow["Active"]