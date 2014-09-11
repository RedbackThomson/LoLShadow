import redis

class LoLRedis:
	def Connect(self):
		self.r = redis.StrictRedis(host=self.host, password=self.password,
			port=self.port, db=self.db)
		self.followerDict = {}

	def DumpFollow(self, user, follower):
		if user.APIKey not in self.followerDict:
			self.followerDict[user.APIKey] = self.r.lrange('follows:'+user.APIKey, 0, -1)
		self.followerDict[user.APIKey].append(follower)

	def NewFollow(self, user, follower):
		self.DumpFollow(user, follower)
		self.r.lpush('follows:'+user.APIKey, follower)

	def HasFollower(self, user, follower):
		if user.APIKey in self.followerDict:
			followers = self.followerDict[user.APIKey]
		else:
			self.followerDict[user.APIKey] = self.r.lrange('follows:'+user.APIKey, 0, -1)
			followers = self.followerDict[user.APIKey]
		return (follower in followers)