from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json


def send_historical_events_CHANNEL_DE_image(CHANNEL_DE):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://de.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
        )
        events = response.json().get('events', [])
        events_with_photo = [
            event
            for event in events
            if event.get('pages') and event['pages'][0].get('thumbnail')
        ]

        if not events_with_photo:
            logger.info('Não há eventos com fotos para enviar hoje.')
            return

        random_event = random.choice(events_with_photo)
        event_text = random_event.get('text', '')
        event_year = random_event.get('year', '')

        caption = f'<b>🖼 | Illustrierte Geschichte </b>\n\nAm <b>{day}. {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>\n\n<blockquote>💬 Wussten Sie schon? Folgen Sie @die_huetie_geschichte.</blockquote>'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL_DE, photo_url, caption=caption, **options)
        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL_DE}.'
        )
    except Exception as e:
        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_CHANNEL_DE_imgs():
    try:
        send_historical_events_CHANNEL_DE_image(CHANNEL_DE)
        logger.success(f'Mensagem enviada o canal {CHANNEL_DE}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho imgs:', str(e))


def get_month_name(month):
    month_names = [
        'Januar',
        'Februar',
        'März',
        'April',
        'Mai',
        'Juni',
        'Juli',
        'August',
        'September',
        'Oktober',
        'November',
        'Dezember',
    ]
    return month_names[month]


def get_deaths_of_the_day(CHANNEL_DE):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        response = requests.get(
            f'https://de.wikipedia.org/api/rest_v1/feed/onthisday/deaths/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            deaths = data.get('deaths', [])

            if len(deaths) > 0:
                death_messages = []

                for index, death in enumerate(deaths[:5], start=1):
                    name = f"<b>{death.get('text', '')}</b>"
                    info = death.get('pages', [{}])[0].get(
                        'extract', 'Informações não disponíveis.'
                    )
                    date = death.get('year', 'Data desconhecida.')

                    death_message = f'<i>{index}.</i> <b>Name:</b> {name}\n<b>Informationen:</b> {info}\n<b>Sterbedatum:</b> {date}'

                    death_messages.append(death_message)

                message = f'<b>⚰️ | Todesfälle an diesem Tag: {day} von {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(death_messages)
                message += '\n\n💬 Wussten Sie? Folgen Sie @die_huetie_geschichte.'

                bot.send_message(CHANNEL_DE, message)
            else:

                logger.info(
                    'Não há informações sobre mortos para o dia atual.'
                )

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao enviar mortos para os canal:', str(e))


def hist_CHANNEL_DE_death():
    try:
        get_deaths_of_the_day(CHANNEL_DE)
        logger.success(f'Mortos enviada o canal {CHANNEL_DE}')
    except Exception as e:
        logger.info('Erro ao enviar o trabalho mortes:', str(e))


def get_births_of_the_day(CHANNEL_DE):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://de.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            births = data.get('births', [])

            if len(births) > 0:
                birth_messages = []

                for index, birth in enumerate(births[:5], start=1):
                    name = f"<b>{birth.get('text', '')}</b>"
                    info = birth.get('pages', [{}])[0].get(
                        'extract', 'Informações não disponíveis.'
                    )
                    date = birth.get('year', 'Data desconhecida.')

                    birth_message = f'<i>{index}.</i> <b>Name:</b> {name}\n<b>Informationen:</b> {info}\n<b>Geburtsdatum:</b> {date}'

                    birth_messages.append(birth_message)

                message = f'<b>🎂 | Geburtstage an diesem Tag: {day} von {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n💬 Wussten Sie? Folgen Sie @die_huetie_geschichte.'
                bot.send_message(CHANNEL_DE, message)
            else:

                logger.info('Não há informações sobre nascidos hoje.')

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao obter informações:', str(e))


def hist_CHANNEL_DE_birth():
    try:
        get_births_of_the_day(CHANNEL_DE)
        logger.success(f'Nascidos enviada o canal {CHANNEL_DE}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho nascido:', str(e))


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-de.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_DE):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>HEUTE IN DER GESCHICHTE</b>\n\n📅 | Ereignis am <b>{day}/{month}</b>\n\n{events}\n\n💬 Wussten Sie? Folgen Sie @die_huetie_geschichte.'
            bot.send_message(CHANNEL_DE, message)
        else:
            bot.send_message(
                CHANNEL_DE,
                '<b>Não há eventos históricos para hoje.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_DE}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_DE_events():
    try:
        send_historical_events_channel(CHANNEL_DE)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_DE}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_DE_alert():
    try:
        nachricht = "🌟 📺 **Treten Sie unserem erstaunlichen Geschichtskanal bei!** 📺 🌟\n\n"\
            "Freunde, entdecken Sie den Zauber der Geschichte durch unsere unterhaltsamen und aufregenden Kanäle! "\
            "Treten Sie jetzt bei und genießen Sie eine breite Palette von Programmen und Dokumentationen, die Sie auf "\
            "eine spannende Reise in die Tiefen der Geschichte mitnehmen.\n\n"\
            "Erleben Sie alte Abenteuer, faszinierende Fakten und entscheidende Ereignisse, die unsere Welt geprägt haben. "\
            "Treten Sie noch heute für ein unterhaltsames und aufschlussreiches Lernerlebnis bei!\n\n"\
            "🌍 Klicken Sie auf den Link, um der Liste der Geschichtskanäle beizutreten: [@history_channels]"\

        bot.send_message(
            CHANNEL_DE,
            nachricht,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Fehler beim Senden von historischen Fakten in den Kanal:', str(e))
