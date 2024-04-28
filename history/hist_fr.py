from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_fr_db


def send_historical_events_CHANNEL_FR_image(CHANNEL_FR):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://fr.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
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
        caption = f'<b>🖼 | Histoire illustrée </b>\n\nLe <b>{day} {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>\n\n<blockquote>💬 Saviez-vous? Suivez @histoire_france.</blockquote>'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL_FR, photo_url, caption=caption, **options)
        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL_FR}.'
        )
    except Exception as e:
        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_CHANNEL_FR_imgs():
    try:
        send_historical_events_CHANNEL_FR_image(CHANNEL_FR)
        logger.success(f'Mensagem enviada o canal {CHANNEL_FR}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho imgs:', str(e))


def get_month_name(month):
    month_names = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro',
    ]
    return month_names[month]


def get_deaths_of_the_day(CHANNEL_FR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        response = requests.get(
            f'https://fr.wikipedia.org/api/rest_v1/feed/onthisday/deaths/{month}/{day}',
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

                    death_message = f'<i>{index}.</i> <b>Nome:</b> {name}\n<b>Informações:</b> {info}\n<b>Data da morte:</b> {date}'
                    death_messages.append(death_message)

                message = f'<b>⚰️ | Décès ce jour-là : {day} de {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(death_messages)
                message += '\n\n💬 Le saviez-vous ? Suivez @histoire_france.'

                bot.send_message(CHANNEL_FR, message)
            else:

                logger.info(
                    'Não há informações sobre mortos para o dia atual.'
                )

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao enviar mortos para os canal:', str(e))


def hist_CHANNEL_FR_death():
    try:
        get_deaths_of_the_day(CHANNEL_FR)
        logger.success(f'Mortos enviada o canal {CHANNEL_FR}')
    except Exception as e:
        logger.info('Erro ao enviar o trabalho mortes:', str(e))


def get_births_of_the_day(CHANNEL_FR):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://fr.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
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

                    birth_message = f'<i>{index}.</i> <b>Nome:</b> {name}\n<b>Informações:</b> {info}\n<b>Data de nascimento:</b> {date}'
                    birth_messages.append(birth_message)

                message = f'<b>🎂 | Naissances ce jour-là : {day} de {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n💬 Le saviez-vous ? Suivez @histoire_france.'

                bot.send_message(CHANNEL_FR, message)
            else:

                logger.info('Não há informações sobre nascidos hoje.')

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao obter informações:', str(e))


def hist_CHANNEL_FR_birth():
    try:
        get_births_of_the_day(CHANNEL_FR)
        logger.success(f'Nascidos enviada o canal {CHANNEL_FR}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho nascido:', str(e))


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-fr.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_FR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>AUJOURD\'HUI DANS L\'HISTOIRE</b>\n\n📅 | Événement le <b>{day}/{month}</b>\n\n{events}\n\n💬 Le saviez-vous ? Suivez @histoire_france.'

            bot.send_message(CHANNEL_FR, message)
        else:
            bot.send_message(
                CHANNEL_FR,
                '<b>Il n’y a aucune information sur les décès pour la journée en cours.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_FR}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_FR_events():
    try:
        send_historical_events_channel(CHANNEL_FR)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_FR}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_FR_alert():
    try:
        message = "🌟 📺 <b>Rejoignez notre incroyable chaîne d'Histoire !</b> 📺 🌟\n\n"\
            "Amis, découvrez la magie de l'histoire à travers nos chaînes divertissantes et passionnantes ! "\
            "Rejoignez-nous dès maintenant pour profiter d'une large gamme de programmes et de documentaires "\
            "qui vous emmèneront dans un voyage passionnant dans les profondeurs de l'histoire.\n\n"\
            "Vivez des aventures anciennes, des faits intrigants et des événements décisifs qui ont façonné notre monde. "\
            "Rejoignez-nous dès aujourd'hui pour une expérience éducative agréable et enrichissante !\n\n"\
            "🌍 Cliquez sur le lien pour rejoindre la liste des chaînes d'histoire : [@history_channels]"\

        bot.send_message(
            CHANNEL_FR,
            message,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Erreur lors de l\'envoi de faits historiques dans le canal :', str(e))


def get_curiosity_FR(CHANNEL_FR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-fr.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("text1", "")
                message = f'<b>Curiosités historiques 📜</b>\n\n{info}\n\n<blockquote>💬 Saviez-vous? Suivre @histoire_france.</blockquote>'
                bot.send_message(CHANNEL_FR, message)
            else:

                logger.info("Pas d'informations pour aujourd'hui.")

    except Exception as e:

        logger.error('Erreur lors de la récupération des informations:', str(e))


def hist_channel_curiosity_FR():
    try:
        get_curiosity_FR(CHANNEL_FR)

        logger.success(f'Curiosité envoyée à la chaîne {CHANNEL_FR}')

    except Exception as e:

        logger.error("Erreur lors de l'envoi de la curiosité à la chaîne:", str(e))

with open(
    './data/presidents/presidents-fr.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_FR():
    try:
        if db.presidents_fr.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_fr_db(new_id, new_date)
            send_info_through_CHANNEL_FR(president)
        else:
            last_president = (
                db.presidents_fr.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Mise à jour des informations du dernier président pour la date actuelle.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_fr.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_CHANNEL_FR(next_president)
                else:

                    logger.error('Plus de présidents à envoyer.')

            else:

                logger.info(
                    "Il n'est pas encore temps d'envoyer des informations sur le prochain président."
                )

    except Exception as e:

        logger.error(
            f'Une erreur s\'est produite lors de l\'envoi des informations sur le président: {str(e)}'
        )


def send_info_through_CHANNEL_FR(president_info):
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
            f'<b>Nom :</b> {name}\n'
            f'<b>Information :</b> {position}° {title}\n'
            f'<b>Parti :</b> {party}\n'
            f'<b>Année de mandat :</b> {term_year}\n'
            f'<b>Vice-président :</b> {vice_president}\n'
            f'<b>Emplacement :</b> {where}\n\n'
            f'<blockquote>💬 Saviez-vous ? Suivez @hoy_en_la_historia.</blockquote>'
        )

        logger.success('Envoi de la photo du président réussi!')

        bot.send_photo(
            CHANNEL_FR, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Erreur lors de l\'envoi de la photo du président: {str(e)}')
