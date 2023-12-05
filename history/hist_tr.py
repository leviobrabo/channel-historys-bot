from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            '../data/events-tr.json', 'r', encoding='utf-8'
        ) as file:

            json_events = json.load(file)
            events = json_events[f'{month}-{day}']
            if events:
                return '\n\n'.join(events)
            else:
                return None
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error reading events from JSON:', str(e))
        logger.info('-' * 50)
        return None


def send_historical_events_channel(CHANNEL_TR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>TARİHTE BUGÜN</b>\n\n📅 | {day}/{month} tarihindeki olaylar\n\n{events}\n\n💬 Biliyor muydunuz? @bugun_in_history adresinden takip edebilirsiniz.'
            bot.send_message(CHANNEL_TR, message)
        else:
            bot.send_message(
                CHANNEL_TR,
                '<b>Bugün için hiçbir şey bulunamadı</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_TR}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_TR_events():
    try:
        send_historical_events_channel(CHANNEL_TR)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_TR}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_TR_alert():
    try:
        mesaj = "🌟 📺 **Harika Tarih Kanalımıza Katılın!** 📺 🌟\n\n"\
            "Arkadaşlar, tarihin büyüsünü eğlenceli ve heyecan verici kanallarımız aracılığıyla keşfedin! "\
            "Şimdi katılın ve sizi tarihin derinliklerine götürecek geniş program ve belgesel yelpazemizin tadını çıkarın.\n\n"\
            "Antik maceraları, ilgi çekici gerçekleri ve dünyamızı şekillendiren önemli olayları yaşayın. "\
            "Keyifli ve aydınlatıcı bir eğitim deneyimi için bugün bize katılın!\n\n"\
            "🌍 Tarih Kanalları listesine katılmak için bağlantıya tıklayın: [@history_channels]"\

        bot.send_message(
            CHANNEL_TR,
            mesaj,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('Kanalda tarihi gerçekleri gönderme hatası:', str(e))
