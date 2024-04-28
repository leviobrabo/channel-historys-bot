import configparser
import threading
from datetime import datetime, timedelta
from time import sleep
from db import *

import schedule
from telebot import types, util

from bot import bot
from history.hist_ar import *
from history.hist_cs import *
from history.hist_de import *
from history.hist_es import *
from history.hist_fr import *
from history.hist_hi import *
from history.hist_id import *
from history.hist_it import *
from history.hist_ja import *
from history.hist_ko import *
from history.hist_pl import *
from history.hist_ru import *
from history.hist_tr import *
from history.hist_uk import *
from history.hist_vi import *
from history.hist_zh import *
from logger import *

config = configparser.ConfigParser()
config.read('bot.conf')


# arabic
schedule.every().day.at('05:00').do(hist_CHANNEL_AR_events)
schedule.every().day.at('11:00').do(hist_CHANNEL_AR_imgs)
schedule.every().day.at('15:00').do(hist_CHANNEL_AR_death)
schedule.every().day.at('22:00').do(hist_CHANNEL_AR_birth)
schedule.every().friday.at('00:00').do(message_CHANNEL_AR_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_AR)
schedule.every().day.at('19:00').do(send_president_photo_AR)

# czech
schedule.every().day.at('05:00').do(hist_CHANNEL_CS_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_CS_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_CS)
schedule.every().day.at('19:00').do(send_president_photo_CS)

# german
schedule.every().day.at('05:00').do(hist_CHANNEL_DE_events)
schedule.every().day.at('11:00').do(hist_CHANNEL_DE_imgs)
schedule.every().day.at('15:00').do(hist_CHANNEL_DE_death)
schedule.every().day.at('22:00').do(hist_CHANNEL_DE_birth)
schedule.every().friday.at('00:00').do(message_CHANNEL_DE_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_DE)
schedule.every().day.at('19:00').do(send_president_photo_DE)


# spanish
schedule.every().day.at('05:00').do(hist_CHANNEL_ES_events)
schedule.every().day.at('11:00').do(hist_CHANNEL_ES_imgs)
schedule.every().day.at('15:00').do(hist_CHANNEL_ES_death)
schedule.every().day.at('22:00').do(hist_CHANNEL_ES_birth)
schedule.every().friday.at('00:00').do(message_CHANNEL_ES_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_ES)
schedule.every().day.at('19:00').do(send_president_photo_ES)


# french
schedule.every().day.at('05:00').do(hist_CHANNEL_FR_events)
schedule.every().day.at('11:00').do(hist_CHANNEL_FR_imgs)
schedule.every().day.at('15:00').do(hist_CHANNEL_FR_death)
schedule.every().day.at('22:00').do(hist_CHANNEL_FR_birth)
schedule.every().friday.at('00:00').do(message_CHANNEL_FR_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_FR)
schedule.every().day.at('19:00').do(send_president_photo_FR)

# hindi
schedule.every().day.at('05:00').do(hist_CHANNEL_HI_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_HI_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_HI)
schedule.every().day.at('19:00').do(send_president_photo_HI)

# indonesian
schedule.every().day.at('05:00').do(hist_CHANNEL_ID_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_ID_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_ID)
schedule.every().day.at('19:00').do(send_president_photo_ID)

# italian
schedule.every().day.at('05:00').do(hist_CHANNEL_IT_events)
schedule.every().day.at('22:00').do(hist_CHANNEL_IT_imgs)
schedule.every().friday.at('00:00').do(message_CHANNEL_IT_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_IT)
schedule.every().day.at('19:00').do(send_president_photo_IT)

# japanese
schedule.every().day.at('05:00').do(hist_CHANNEL_JA_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_JA_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_JA)
schedule.every().day.at('19:00').do(send_president_photo_JA)

# korean
schedule.every().day.at('05:00').do(hist_CHANNEL_KO_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_KO_alert)

# polish
schedule.every().day.at('05:00').do(hist_CHANNEL_PL_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_PL_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_PL)
schedule.every().day.at('19:00').do(send_president_photo_PL)

# russian
schedule.every().day.at('05:00').do(hist_CHANNEL_RU_events)
schedule.every().day.at('11:00').do(hist_CHANNEL_RU_imgs)
schedule.every().day.at('15:00').do(hist_CHANNEL_RU_death)
schedule.every().day.at('22:00').do(hist_CHANNEL_RU_birth)
schedule.every().friday.at('00:00').do(message_CHANNEL_RU_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_RU)
schedule.every().day.at('19:00').do(send_president_photo_RU)

# turkish
schedule.every().day.at('05:00').do(hist_CHANNEL_TR_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_TR_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_TR)
schedule.every().day.at('19:00').do(send_president_photo_TR)


# ukrainain
schedule.every().day.at('05:00').do(hist_CHANNEL_UK_events)
schedule.every().day.at('11:00').do(hist_CHANNEL_UK_imgs)
schedule.every().day.at('15:00').do(hist_CHANNEL_UK_death)
schedule.every().day.at('22:00').do(hist_CHANNEL_UK_birth)
schedule.every().friday.at('00:00').do(message_CHANNEL_UK_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_UK)
schedule.every().day.at('19:00').do(send_president_photo_UK)

# vietnamese
schedule.every().day.at('05:00').do(hist_CHANNEL_VI_events)
schedule.every().friday.at('00:00').do(message_CHANNEL_VI_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_VI)
schedule.every().day.at('19:00').do(send_president_photo_VI)

# chinese
schedule.every().day.at('05:00').do(hist_CHANNEL_ZH_events)
schedule.every().day.at('11:00').do(hist_CHANNEL_ZH_imgs)
schedule.every().day.at('15:00').do(hist_CHANNEL_ZH_death)
schedule.every().day.at('22:00').do(hist_CHANNEL_ZH_birth)
schedule.every().friday.at('00:00').do(message_CHANNEL_ZH_alert)
schedule.every().day.at('08:00').do(hist_channel_curiosity_ZH)
schedule.every().day.at('19:00').do(send_president_photo_ZH)


def polling_thread():
    logger.success('Start polling...')
    bot.polling(allowed_updates=util.update_types)


def schedule_thread():
    while True:
        schedule.run_pending()
        sleep(1)


polling_thread = threading.Thread(target=polling_thread)
schedule_thread = threading.Thread(target=schedule_thread)

try:
    polling_thread.start()
    schedule_thread.start()
except Exception as e:
    pass
