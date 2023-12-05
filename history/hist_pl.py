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
            'data/events-pl.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_PL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>DZIŚ W HISTORII</b>\n\n📅 | Wydarzenia w dniu <b>{day}/{month}</b>\n\n{events}\n\n💬 Czy wiedziałeś? Śledź @dzisiaj_w_historii.'

            bot.send_message(CHANNEL_PL, message)
        else:
            bot.send_message(
                CHANNEL_PL,
                '<b>Nic nie znaleziono na dzisiaj</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_PL}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_PL_events():
    try:
        send_historical_events_channel(CHANNEL_PL)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_PL}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_PL_alert():
    try:
        wiadomosc = "🌟 📺 **Dołącz do naszego niesamowitego kanału historycznego!** 📺 🌟\n\n"\
            "Znajomi, odkryj magię historii poprzez nasze angażujące i ekscytujące kanały! "\
            "Dołącz już teraz, aby cieszyć się szeroką gamą programów i dokumentów, które zabiorą cię w "\
            "pasjonującą podróż w głąb historii.\n\n"\
            "Doświadcz starożytnych przygód, fascynujących faktów i kluczowych wydarzeń, które kształtowały nasz świat. "\
            "Dołącz do nas już dziś, by mieć przyjemne i pouczające doświadczenie edukacyjne!\n\n"\
            "🌍 Kliknij link, aby dołączyć do listy kanałów historycznych: [@history_channels]"\

        bot.send_message(
            CHANNEL_PL,
            wiadomosc,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Błąd podczas wysyłania faktów historycznych do kanału:', str(e))
