from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json


def get_month_name(month):
    month_names = [
        'जनवरी',
        'फ़रवरी',
        'मार्च',
        'अप्रैल',
        'मई',
        'जून',
        'जुलाई',
        'अगस्त',
        'सितंबर',
        'अक्टूबर',
        'नवंबर',
        'दिसंबर',
    ]
    return month_names[month]


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            '../data/events-hi.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_HI):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>आज इतिहास में</b>\n\n📅 | <b>{day}/{month}</b> को घटना\n\n{events}\n\n💬 क्या आप जानते हैं? @itihaas_hi को फॉलो करें।'

            bot.send_message(CHANNEL_HI, message)
        else:
            bot.send_message(
                CHANNEL_HI,
                '<b>आज तक मौतों के बारे में कोई जानकारी नहीं है।</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_HI}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_HI_events():
    try:
        send_historical_events_channel(CHANNEL_HI)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_HI}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_HI_alert():
    try:
        message = "🌟 📺 **हमारे शानदार इतिहास चैनल में शामिल हों!** 📺 🌟\n\n"\
            "दोस्तों, हमारे मनोरंजक और रोमांचक चैनलों के माध्यम से इतिहास का जादू खोजें! "\
            "अभी हमारे साथ जुड़ें और एक व्यापक कार्यक्रम और डॉक्यूमेंट्री का आनंद लें जो आपको एक रोमांचक यात्रा पर लेकर जाएगा "\
            "इतिहास के गहराईयों में।\n\n"\
            "प्राचीन साहसिक किस्से, रोचक तथ्य और हमारी दुनिया को आकार देने वाले महत्वपूर्ण घटनाओं का अनुभव करें। "\
            "एक मनोरंजन से भरपूर और ज्ञानवर्धक शैक्षिक अनुभव के लिए आज हमारे साथ जुड़ें!\n\n"\
            "🌍 इतिहास चैनल की सूची में शामिल होने के लिए लिंक पर क्लिक करें: [@history_channels]"\

        bot.send_message(
            CHANNEL_HI,
            message,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('चैनल में ऐतिहासिक तथ्यों को भेजने में त्रुटि:', str(e))
