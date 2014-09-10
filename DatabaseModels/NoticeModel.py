class NoticeModel:
	def __init__(self, dbRow):
		self.ID = dbRow["ID"]
		self.Message = dbRow["Message"]
		self.Timestamp = dbRow["Timestamp"]