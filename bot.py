import configparser

import telebot

config = configparser.ConfigParser()
config.read('bot.conf')
TOKEN = config['HIST']['TOKEN']

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

config = configparser.ConfigParser()
config.read('bot.conf')

CHANNEL_AR = int(config['HIST']['channel_arabic'])
CHANNEL_RU = int(config['HIST']['channel_russian'])
CHANNEL_FR = int(config['HIST']['channel_french'])
CHANNEL_DE = int(config['HIST']['channel_german'])
CHANNEL_ES = int(config['HIST']['channel_spanish'])
CHANNEL_IT = int(config['HIST']['channel_italian'])
CHANNEL_JA = int(config['HIST']['channel_japanese'])
CHANNEL_KO = int(config['HIST']['channel_korean'])
CHANNEL_HI = int(config['HIST']['channel_hindi'])
CHANNEL_TR = int(config['HIST']['channel_turkish'])
CHANNEL_PL = int(config['HIST']['channel_polish'])
CHANNEL_CS = int(config['HIST']['channel_czech'])
CHANNEL_UK = int(config['HIST']['channel_ukrainian'])
CHANNEL_ID = int(config['HIST']['channel_indonesian'])
CHANNEL_VI = int(config['HIST']['channel_vietnamese'])
CHANNEL_ZH = int(config['HIST']['channel_chinese'])
