import logging
import logging.config

class ShadowLogger:
	@staticmethod
	def InitLogger():
		logging.config.fileConfig('conf/logConfig.conf')
		ShadowLogger.logger = logging.getLogger()

	@staticmethod
	def Info(message):
		ShadowLogger.logger.info(message)

	@staticmethod
	def Debug(message):
		ShadowLogger.logger.debug(message)

	@staticmethod
	def Error(message):
		ShadowLogger.logger.error(message)

	@staticmethod
	def ShadowInfo(message, shadowName):
		ShadowLogger.logger.info(shadowName + ' - ' + message)

	@staticmethod
	def ShadowDebug(message, shadowName):
		ShadowLogger.logger.debug(shadowName + ' - ' + message)

	@staticmethod
	def ShadowError(message, shadowName):
		ShadowLogger.logger.error(shadowName + ' - ' + message)