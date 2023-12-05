from loguru import logger
import configparser


config = configparser.ConfigParser()
config.read('bot.conf')
logger.add(config['LOG']['LOG_PATH'])
