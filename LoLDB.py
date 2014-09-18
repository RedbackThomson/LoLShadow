import MySQLdb
import MySQLdb.cursors
from DatabaseModels.ShadowModel import ShadowModel
from DatabaseModels.NoticeModel import NoticeModel
from DatabaseModels.UserModel import UserModel
from DatabaseModels.RegionModel import RegionModel

class LoLDB:
	def Connect(self):
		self.conn = MySQLdb.connect(host=self.login_host,user=self.login_user,passwd=self.login_pass,db=self.login_db)
		self.conn.autocommit(True)

	def Close(self):
		self.conn.close()

	def getCursor(self):
		self.conn.ping(True)
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
		cursor.execute("INSERT INTO `statistics`(`Shadow`,`OnlineUsers`) VALUES(%s,%s) ON DUPLICATE KEY UPDATE `OnlineUsers`=%s;" % (shadow, str(onlineUsers), str(onlineUsers)))

	def IncrementUserFollowed(self, user):
		cursor = self.getCursor()
		cursor.execute("INSERT INTO `user_statistics`(`User`,`TotalSubscribed`) VALUES(%s,1) ON DUPLICATE KEY UPDATE `TotalSubscribed`=`TotalSubscribed` + 1;" % (user))

	def IncrementTotalFollowed(self, shadow):
		cursor = self.getCursor()
		cursor.execute("INSERT INTO `statistics`(`Shadow`,`TotalFollowed`) VALUES(%s,1) ON DUPLICATE KEY UPDATE `TotalFollowed` = `TotalFollowed` + 1", (shadow))

	def UpdateNotice(self, user_id, notice):
		cursor = self.getCursor()
		cursor.execute("UPDATE `users` SET `LastNotice`=%s WHERE `ID`=%s;", (notice, user_id))

	def ResetOnlineUsers(self, shadow):
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO `statistics`(`Shadow`,`OnlineUsers`) VALUES(%s,0) ON DUPLICATE KEY UPDATE `OnlineUsers`=0;" % (shadow))

	def GetLatestNotice(self):
		cursor = self.getCursor()
		cursor.execute("SELECT * FROM `notices` ORDER BY `Timestamp` DESC LIMIT 1;")
		return NoticeModel(cursor.fetchone())

	def GetShadowRegion(self, shadow):
		cursor = self.getCursor()
		cursor.execute("SELECT * FROM `regions` WHERE `ID`=(SELECT `Region` FROM `shadows` WHERE `ID`=%s);", (shadow))
		return RegionModel(cursor.fetchone())