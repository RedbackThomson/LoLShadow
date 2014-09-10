import MySQLdb
import MySQLdb.cursors
from DatabaseModels.ShadowModel import ShadowModel
from DatabaseModels.NoticeModel import NoticeModel
from DatabaseModels.UserModel import UserModel

class LoLDB:
	def Connect(self):
		self.conn = MySQLdb.connect(host=self.login_host,user=self.login_user,passwd=self.login_pass,db=self.login_db)
		self.conn.autocommit(True)

	def Close(self):
		self.conn.close()

	def getCursor(self):
		return self.conn.cursor(MySQLdb.cursors.DictCursor)

	def GetAllShadows(self):
		cursor = self.getCursor()
		cursor.execute("SELECT * FROM `shadows`;")
		return cursor.fetchall()

	def GetShadowEnabled(self, shadow):
		cursor = self.getCursor()
		cursor.execute("SELECT `Enabled` FROM `shadows` WHERE `ID`=%s;", (shadow))
		results = cursor.fetchone()
		if results == None: return False
		return (results['Enabled'] == 1)

	def GetShadowByID(self, shadow):
		cursor = self.getCursor()
		cursor.execute("SELECT * FROM `shadows` WHERE `ID`=%s;", (shadow))
		return ShadowModel(cursor.fetchone())

	def CheckUserReserved(self, summoner, shadow):
		cursor = self.getCursor()
		cursor.execute("SELECT COUNT(`ID`) FROM `summoners` WHERE `SummonerID`=%s AND `Shadow`=%s", (summoner, shadow))
		result = cursor.fetchone()
		return (result['COUNT(`ID`)'] == 1)

	def GetSetting(self, key):
		cursor = self.getCursor()
		cursor.execute("SELECT * FROM `settings` WHERE `Key`=%s;", (key))
		return (cursor.fetchone())['Value']

	def GetUserBySummonerId(self, summoner_id, shadow):
		cursor = self.getCursor()
		cursor.execute("SELECT * FROM `users` WHERE `ID`= (SELECT `User` FROM `summoners` WHERE `SummonerID`=%s AND `Shadow`=%s);", (str(summoner_id), shadow))
		result = cursor.fetchone()
		if result == None: return None
		return UserModel(result)

	def AddShadowFriend(self, summoner_id, shadow):
		cursor = self.getCursor()
		cursor.execute("INSERT INTO `shadow_friends`(`Shadow`,`SummonerID`) VALUES(%s,%s);" % (shadow,summoner_id))

	def RemoveShadowFriend(self, summoner_id, shadow):
		cursor = self.getCursor()
		cursor.execute("DELETE FROM `shadow_friends` WHERE `Shadow`=%s AND `SummonerID`=%s;" % (shadow,summoner_id))

	def SetOnlineUsers(self, onlineUsers, shadow):
		cursor = self.getCursor()
		cursor.execute("INSERT INTO `statistics`(`OnlineUsers`,`Shadow`) VALUES(%s,%s) ON DUPLICATE KEY UPDATE;" % (str(onlineUsers), shadow))

	def IncrementTotalFollowed(self, shadow):
		cursor = self.getCursor()
		cursor.execute("INSERT IGNORE INTO `statistics`(`Shadow`,`OnlineUsers`, `TotalFollowed`) VALUES(%s,%s,%s);" % (shadow,0,0))
		cursor.execute("UPDATE `statistics` SET `TotalFollowed` = `TotalFollowed` + 1 WHERE `Shadow`=%s;", (shadow))

	def UpdateNotice(self, user_id, notice):
		cursor = self.getCursor()
		cursor.execute("UPDATE `users` SET `LastNotice`=%s WHERE `ID`=%s;", (notice, user_id))

	def ResetOnlineUsers(self, shadow):
		cursor = self.conn.cursor()
		cursor.execute("UPDATE `statistics` SET `OnlineUsers` = 0 WHERE `Shadow`=%s;", (shadow))

	def GetLatestNotice(self):
		cursor = self.getCursor()
		cursor.execute("SELECT * FROM `notices` ORDER BY `Timestamp` DESC LIMIT 1;")
		return NoticeModel(cursor.fetchone())