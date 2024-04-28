from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_es_db


def send_historical_events_CHANNEL_ES_image(CHANNEL_ES):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
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
        caption = f'<b>🖼 | Historia ilustrada </b>\n\nEl <b>{day} de {get_month_name(month)} de {event_year}</b>\n\n<code>{event_text}</code>\n\n<blockquote>💬 ¿Sabías que? Sigue a @hoy_en_la_historia.</blockquote>'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL_ES, photo_url, caption=caption, **options)
        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL_ES}.'
        )
    except Exception as e:
        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_CHANNEL_ES_imgs():
    try:
        send_historical_events_CHANNEL_ES_image(CHANNEL_ES)
        logger.success(f'Mensagem enviada o canal {CHANNEL_ES}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho imgs:', str(e))


def get_month_name(month):
    month_names = [
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre',
    ]
    return month_names[month]


def get_deaths_of_the_day(CHANNEL_ES):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        response = requests.get(
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/deaths/{month}/{day}',
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

                    death_message = f'<i>{index}.</i> <b>Nombre:</b> {name}\n<b>Información:</b> {info}\n<b>Fecha de fallecimiento:</b> {date}'

                    death_messages.append(death_message)

                message = f'<b>⚰️ |  Fallecimientos en este día: {day} de {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(death_messages)
                message += '\n\n💬 ¿Sabías? Sigue a @hoy_en_la_historia.'

                bot.send_message(CHANNEL_ES, message)
            else:

                logger.info(
                    'Não há informações sobre mortos para o dia atual.'
                )

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao enviar mortos para os canal:', str(e))


def hist_CHANNEL_ES_death():
    try:
        get_deaths_of_the_day(CHANNEL_ES)
        logger.success(f'Mortos enviada o canal {CHANNEL_ES}')
    except Exception as e:
        logger.info('Erro ao enviar o trabalho mortes:', str(e))


def get_births_of_the_day(CHANNEL_ES):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
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

                    birth_message = f'<i>{index}.</i> <b>Nombre:</b> {name}\n<b>Información:</b> {info}\n<b>Fecha de nacimiento:</b> {date}'

                    birth_messages.append(birth_message)

                message = f'<b>🎂 | Nacimientos en este día: {day} de {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n💬 ¿Sabías? Sigue a @hoy_en_la_historia.'

                bot.send_message(CHANNEL_ES, message)
            else:

                logger.info('Não há informações sobre nascidos hoje.')

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao obter informações:', str(e))


def hist_CHANNEL_ES_birth():
    try:
        get_births_of_the_day(CHANNEL_ES)
        logger.success(f'Nascidos enviada o canal {CHANNEL_ES}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho nascido:', str(e))


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-es.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_ES):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>HOY EN LA HISTORIA</b>\n\n📅 | Evento en <b>{day}/{month}</b>\n\n{events}\n\n💬 ¿Sabías? Sigue a @hoy_en_la_historia.'
            bot.send_message(CHANNEL_ES, message)
        else:
            bot.send_message(
                CHANNEL_ES,
                '<b>No hay información sobre muertes para el día actual.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_ES}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_ES_events():
    try:
        send_historical_events_channel(CHANNEL_ES)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_ES}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_ES_alert():
    try:
        mensaje = "🌟 📺 <b>¡Únete a nuestro increíble canal de Historia</b> 📺 🌟\n\n"\
            "Amigos, descubre la magia de la historia a través de nuestros canales entretenidos y emocionantes. "\
            "Únete ahora para disfrutar de una amplia gama de programas y documentales que te llevarán en un emocionante "\
            "viaje a las profundidades de la historia.\n\n"\
            "Experimenta aventuras antiguas, datos intrigantes y eventos cruciales que dieron forma a nuestro mundo. "\
            "¡Únete hoy para tener una experiencia educativa agradable y enriquecedora!\n\n"\
            "🌍 Haz clic en el enlace para unirte a la lista de canales de Historia: [@history_channels]"\

        bot.send_message(
            CHANNEL_ES,
            mensaje,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('Error al enviar hechos históricos al canal:', str(e))

def get_curiosity_ES(CHANNEL_ES):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-es.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>Curiosidades Históricas 📜</b>\n\n{info}\n\n<blockquote>💬 ¿Sabías? Seguir @hoy_en_la_historia.</blockquote>'
                bot.send_message(CHANNEL_ES, message)
            else:

                logger.info('No hay información para el día de hoy.')

    except Exception as e:

        logger.error('Error al obtener información:', str(e))


def hist_channel_curiosity_ES():
    try:
        get_curiosity_ES(CHANNEL_ES)

        logger.success(f'Curiosidad enviada al canal {CHANNEL_ES}')

    except Exception as e:

        logger.error('Error al enviar la curiosidad al canal:', str(e))

with open(
    './data/presidents/presidents-es.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_ES():
    try:
        if db.presidents_es.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_es_db(new_id, new_date)
            send_info_through_channel_ES(president)
        else:
            last_president = (
                db.presidents_es.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Atualizando informações do último presidente para a data atual.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_es.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_ES(next_president)
                else:

                    logger.error('No more presidents to send.')

            else:

                logger.info(
                    "It's not time yet to send information about the next president."
                )

    except Exception as e:

        logger.error(
            f'An error occurred while sending president information: {str(e)}'
        )


def send_info_through_channel_ES(president_info):
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
            f'<b>Nombre:</b> {name}\n'
            f'<b>Información:</b> {position}° {title}\n'
            f'<b>Partido:</b> {party}\n'
            f'<b>Año de Mandato:</b> {term_year}\n'
            f'<b>Vicepresidente:</b> {vice_president}\n'
            f'<b>Ubicación:</b> {where}\n\n'
            f'<blockquote>💬 ¿Sabías? Sigue a @hoy_en_la_historia.</blockquote>'
        )

        logger.success('¡Envío del presidente completado con éxito!')

        bot.send_photo(
            CHANNEL_ES, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Error al enviar la foto del presidente: {str(e)}')
