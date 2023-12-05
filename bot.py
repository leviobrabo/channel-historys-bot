import configparser

import telebot

config = configparser.ConfigParser()
config.read('bot.conf')


config = configparser.ConfigParser()
config.read('bot.conf')

TOKEN = config['HISTORY']['TOKEN']
CHANNEL_AR = int(config['HISTORY']['channel_arabic'])
CHANNEL_RU = int(config['HISTORY']['channel_russian'])
CHANNEL_FR = int(config['HISTORY']['channel_french'])
CHANNEL_DE = int(config['HISTORY']['channel_german'])
CHANNEL_ES = int(config['HISTORY']['channel_spanish'])
CHANNEL_IT = int(config['HISTORY']['channel_italian'])
CHANNEL_JA = int(config['HISTORY']['channel_japanese'])
CHANNEL_KO = int(config['HISTORY']['channel_korean'])
CHANNEL_HI = int(config['HISTORY']['channel_hindi'])
CHANNEL_TR = int(config['HISTORY']['channel_turkish'])
CHANNEL_PL = int(config['HISTORY']['channel_polish'])
CHANNEL_CS = int(config['HISTORY']['channel_czech'])
CHANNEL_UK = int(config['HISTORY']['channel_ukrainian'])
CHANNEL_ID = int(config['HISTORY']['channel_indonesian'])
CHANNEL_VI = int(config['HISTORY']['channel_vietnamese'])
CHANNEL_ZH = int(config['HISTORY']['channel_chinese'])

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
