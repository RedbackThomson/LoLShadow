import redis

class LoLRedis:
	def Connect(self):
		self.r = redis.StrictRedis(host=self.host, password=self.password,
			port=self.port, db=self.db)

	def NewFollow(self, user, follower):
		self.r.lpush('follows:'+user.APIKey, follower)