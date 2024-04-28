from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_de_db


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
        nachricht = "🌟 📺 <b>Treten Sie unserem erstaunlichen Geschichtskanal bei!</b> 📺 🌟\n\n"\
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


def get_curiosity_DE(CHANNEL_DE):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-de.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>Historische Kuriositäten 📜</b>\n\n{info}\n\n<blockquote>💬 Wussten Sie? Folgen @die_huetie_geschichte.</blockquote>'
                bot.send_message(CHANNEL_DE, message)
            else:

                logger.info('Es gibt keine Informationen für heute.')

    except Exception as e:

        logger.error('Fehler beim Abrufen von Informationen:', str(e))


def hist_channel_curiosity_DE():
    try:
        get_curiosity_DE(CHANNEL_DE)

        logger.success(f'Neugierde an den Kanal {CHANNEL_DE} gesendet')

    except Exception as e:

        logger.error('Fehler beim Senden der Neugier an den Kanal:', str(e))

with open(
    './data/presidents/presidents-de.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_DE():
    try:
        if db.presidents_de.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_de_db(new_id, new_date)
            send_info_through_CHANNEL_DE(president)
        else:
            last_president = (
                db.presidents_de.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Aktualisieren der Informationen zum letzten Präsidenten auf das aktuelle Datum.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_de.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_CHANNEL_DE(next_president)
                else:

                    logger.error('Keine weiteren Präsidenten zum Senden.')

            else:

                logger.info(
                    "Es ist noch nicht an der Zeit, Informationen über den nächsten Präsidenten zu senden."
                )

    except Exception as e:

        logger.error(
            f'Ein Fehler ist aufgetreten beim Senden von Präsidenteninformationen: {str(e)}'
        )


def send_info_through_CHANNEL_DE(president_info):
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
            f'<b>Name:</b> {name}\n'
            f'<b>Information:</b> {position}° {title}\n'
            f'<b>Partei:</b> {party}\n'
            f'<b>Amtszeit:</b> {term_year}\n'
            f'<b>Vizepräsident:</b> {vice_president}\n'
            f'<b>Ort:</b> {where}\n\n'
            f'<blockquote>💬 Wussten Sie schon? Folgen Sie @die_huetie_geschichte..</blockquote>'
        )

        logger.success('Präsidentenfoto erfolgreich gesendet!')

        bot.send_photo(
            CHANNEL_DE, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Fehler beim Senden des Präsidentenfotos: {str(e)}')
