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
        'Gennaio',
        'Febbraio',
        'Marzo',
        'Aprile',
        'Maggio',
        'Giugno',
        'Luglio',
        'Agosto',
        'Settembre',
        'Ottobre',
        'Novembre',
        'Dicembre',
    ]
    return month_names[month]


def send_historical_events_CHANNEL_IT_image(CHANNEL_IT):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://it.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
        )
        events = response.json().get('events', [])
        events_with_photo = [
            event
            for event in events
            if event.get('pages') and event['pages'][0].get('thumbnail')
        ]

        if events:
            random_event = random.choice(events)
            event_text = random_event.get('text', '')
            event_year = random_event.get('year', '')

        if not events_with_photo:
            logger.info('Não há eventos com fotos para enviar hoje.')
            return

        random_event = random.choice(events_with_photo)
        caption = f'<b>🖼 | Storia illustrata </b>\n\nIl <b>{day} di {get_month_name(month)} di {event_year}</b>\n\n<code>{event_text}</code>\n\n💬 Lo sapevi? Segui @storia_oggi'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL_IT, photo_url, caption=caption, **options)
        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL_IT}.'
        )
    except Exception as e:
        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_CHANNEL_IT_imgs():
    try:
        send_historical_events_CHANNEL_IT_image(CHANNEL_IT)
        logger.success(f'Mensagem enviada o canal {CHANNEL_IT}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho imgs:', str(e))


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            '../data/events-it.json', 'r', encoding='utf-8'
        ) as file:

            json_events = json.load(file)
            events = json_events[f'{month}-{day}']
            if events:
                return '\n\n'.join(events)
            else:
                return None
    except Exception as e:
        logger.error('Error reading events from JSON:', str(e))
        return None


def send_historical_events_channel(CHANNEL_IT):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>OGGI NELLA STORIA</b>\n\n📅 | Evento in data <b>{day}/{month}</b>\n\n{events}\n\n💬 Lo sapevi? Segui @storia_oggi.'

            bot.send_message(CHANNEL_IT, message)
        else:
            bot.send_message(
                CHANNEL_IT,
                '<b>Niente trovato per oggi</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_IT}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_IT_events():
    try:
        send_historical_events_channel(CHANNEL_IT)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_IT}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_IT_alert():
    try:
        messaggio = "🌟 📺 **Unisciti al nostro incredibile canale di Storia!** 📺 🌟\n\n"\
            "Amici, scopri la magia della storia attraverso i nostri canali coinvolgenti ed emozionanti! "\
            "Unisciti a noi ora per goderti una vasta gamma di programmi e documentari che ti porteranno in un "\
            "emozionante viaggio nelle profondità della storia.\n\n"\
            "Vivi antiche avventure, fatti intriganti ed eventi cruciali che hanno plasmato il nostro mondo. "\
            "Unisciti a noi oggi per un'esperienza educativa divertente e illuminante!\n\n"\
            "🌍 Clicca sul link per accedere alla lista dei canali di Storia: [@history_channels]"\

        bot.send_message(
            CHANNEL_IT,
            messaggio,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Errore nell\'invio dei fatti storici nel canale:', str(e))
