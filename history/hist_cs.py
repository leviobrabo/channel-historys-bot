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
            'data/events-cs.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_CS):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>DNEŠNÍ UDÁLOSTI V HISTORII</b>\n\n📅 | Událost dne <b>{day}/{month}</b>\n\n{events}\n\n💬 Věděli jste? Sledujte @dnes_v_historii'
            bot.send_message(CHANNEL_CS, message)
        else:
            bot.send_message(
                CHANNEL_CS,
                '<b>Pro aktuální den nejsou žádné informace o úmrtích.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_CS}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_CS_events():
    try:
        send_historical_events_channel(CHANNEL_CS)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_CS}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_CS_alert():
    try:
        zprava = "🌟 📺 **Připojte se k našemu úžasnému kanálu historie!** 📺 🌟\n\n"\
            "Přátelé, objevte kouzlo historie prostřednictvím našich zábavných a vzrušujících kanálů! "\
            "Přidejte se k nám nyní a užijte si širokou škálu programů a dokumentů, které vás zavedou na "\
            "vzrušující cestu do hlubin historie.\n\n"\
            "Zažijte starověké dobrodružství, zajímavé fakty a klíčové události, které formovaly náš svět. "\
            "Přidejte se k nám dnes pro příjemný a osvěžující vzdělávací zážitek!\n\n"\
            "🌍 Klepněte na odkaz pro připojení k seznamu historických kanálů: [@history_channels]"\

        bot.send_message(
            CHANNEL_CS,
            zprava,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Chyba při odesílání historických faktů do kanálu:', str(e))
