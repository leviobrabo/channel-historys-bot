from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json


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

        if events:
            random_event = random.choice(events)
            event_text = random_event.get('text', '')
            event_year = random_event.get('year', '')

        if not events_with_photo:
            logger.info('Não há eventos com fotos para enviar hoje.')
            return

        random_event = random.choice(events_with_photo)
        caption = f'<b>🖼 | Histoire illustrée </b>\n\nLe <b>{day} {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>\n\n💬 Saviez-vous? Suivez @histoire_france.'

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
            '../data/events-fr.json', 'r', encoding='utf-8'
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
        message = "🌟 📺 **Rejoignez notre incroyable chaîne d'Histoire !** 📺 🌟\n\n"\
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

