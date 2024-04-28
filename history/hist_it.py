from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_it_db


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

        random_event = random.choice(events_with_photo)
        event_text = random_event.get('text', '')
        event_year = random_event.get('year', '')

        if not events_with_photo:
            logger.info('Não há eventos com fotos para enviar hoje.')
            return

        random_event = random.choice(events_with_photo)
        caption = f'<b>🖼 | Storia illustrata </b>\n\nIl <b>{day} di {get_month_name(month)} di {event_year}</b>\n\n<code>{event_text}</code>\n\n<blockquote>💬 Lo sapevi? Segui @storia_oggi</blockquote>'

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
            'data/events-it.json', 'r', encoding='utf-8'
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
            message = f'<b>OGGI NELLA STORIA</b>\n\n📅 | Evento in data <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 Lo sapevi? Segui @storia_oggi</blockquote>.'

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
        messaggio = "🌟 📺 <b>Unisciti al nostro incredibile canale di Storia!</b> 📺 🌟\n\n"\
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


def get_curiosity_IT(CHANNEL_IT):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-it.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")
                message = f'<b>Curiosità storiche 📜</b>\n\n{info}\n\n<blockquote>💬 Lo sapevate? Seguire @storia_oggi.</blockquote>'
                bot.send_message(CHANNEL_IT, message)
            else:

                logger.info('Non ci sono informazioni per oggi.')

    except Exception as e:

        logger.error('Errore nel recupero delle informazioni:', str(e))


def hist_channel_curiosity_IT():
    try:
        get_curiosity_IT(CHANNEL_IT)

        logger.success(f'Curiosità inviata al canale {CHANNEL_IT}')

    except Exception as e:

        logger.error('Errore nell\'invio della curiosità al canale:', str(e))

with open(
    './data/presidents/presidents-it.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_IT():
    try:
        if db.presidents_it.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_it_db(new_id, new_date)
            send_info_through_channel_IT(president)
        else:
            last_president = (
                db.presidents_it.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Aggiornamento delle informazioni dell\'ultimo presidente alla data attuale.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_it.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_IT(next_president)
                else:

                    logger.error('Non ci sono più presidenti da inviare.')

            else:

                logger.info(
                    "Non è ancora il momento di inviare informazioni sul prossimo presidente."
                )

    except Exception as e:

        logger.error(
            f'Errore durante l\'invio delle informazioni sul presidente: {str(e)}'
        )


def send_info_through_channel_IT(president_info):
    try:
        title = president_info.get('title', '')
        name = president_info.get('name', '')
        position = president_info.get('position', '')
        party = president_info.get('broken', '')
        term_year = president_info.get('year_of_office', '')
        vice_president = president_info.get('vice_president', '')
        photo = president_info.get('photo', '')
        where = president_info.get('local', '')

        caption = (
            f'<b>{title}</b>\n\n'
            f'<b>Nome:</b> {name}\n'
            f'<b>Informazioni:</b> {position}° {title}\n'
            f'<b>Partito:</b> {party}\n'
            f'<b>Anno di Mandato:</b> {term_year}\n'
            f'<b>Vicepresidente:</b> {vice_president}\n'
            f'<b>Luogo:</b> {where}\n\n'
            f'<blockquote>💬 Lo sapevi? Segui @storia_oggi.</blockquote>'
        )

        logger.success('Invio del presidente completato con successo!')

        bot.send_photo(
            CHANNEL_IT, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Errore nell\'invio della foto del presidente: {str(e)}')