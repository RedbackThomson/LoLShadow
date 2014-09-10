class SettingModel:
	def __init__(self, dbRow):
		self.Key = dbRow["Key"]
		self.Value = dbRow["Value"]