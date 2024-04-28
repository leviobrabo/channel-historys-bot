from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_uk_db


def send_historical_events_CHANNEL_UK_image(CHANNEL_UK):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://uk.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
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
        caption = f'<b>🖼 | Ілюстрована історія </b>\n\nУ <b>{day} {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>\n\n<blockquote>💬 Ви знали? Підписуйтеся на @istoriya_uks.</blockquote>'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL_UK, photo_url, caption=caption, **options)
        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL_UK}.'
        )
    except Exception as e:
        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_CHANNEL_UK_imgs():
    try:
        send_historical_events_CHANNEL_UK_image(CHANNEL_UK)
        logger.success(f'Mensagem enviada o canal {CHANNEL_UK}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho imgs:', str(e))


def get_month_name(month):
    month_names = [
        'Січень',
        'Лютий',
        'Березень',
        'Квітень',
        'Травень',
        'Червень',
        'Липень',
        'Серпень',
        'Вересень',
        'Жовтень',
        'Листопад',
        'Грудень',
    ]
    return month_names[month]


def get_deaths_of_the_day(CHANNEL_UK):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        response = requests.get(
            f'https://uk.wikipedia.org/api/rest_v1/feed/onthisday/deaths/{month}/{day}',
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

                    death_message = f'<i>{index}.</i> <b>Ім\'я:</b> {name}\n<b>Інформація:</b> {info}\n<b>Дата смерті:</b> {date}'
                    death_messages.append(death_message)

                message = f'<b>⚰️ | Смерті у цей день: {day} {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(death_messages)
                message += '\n\n<blockquote>💬 Ви знали? Підписуйтеся на @istoriya_uks.</blockquote>'

                bot.send_message(CHANNEL_UK, message)
            else:

                logger.info(
                    'Não há informações sobre mortos para o dia atual.'
                )

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao enviar mortos para os canal:', str(e))


def hist_CHANNEL_UK_death():
    try:
        get_deaths_of_the_day(CHANNEL_UK)
        logger.success(f'Mortos enviada o canal {CHANNEL_UK}')
    except Exception as e:
        logger.info('Erro ao enviar o trabalho mortes:', str(e))


def get_births_of_the_day(CHANNEL_UK):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://uk.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
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

                    birth_message = f'<i>{index}.</i> <b>Ім\'я:</b> {name}\n<b>Інформація:</b> {info}\n<b>Дата народження:</b> {date}'
                    birth_messages.append(birth_message)

                message = f'<b>🎂 | Народилися у цей день: {day} {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n<blockquote>💬 Ви знали? Підписуйтеся на @istoriya_uks.</blockquote>'

                bot.send_message(CHANNEL_UK, message)
            else:

                logger.info('Não há informações sobre nascidos hoje.')

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao obter informações:', str(e))


def hist_CHANNEL_UK_birth():
    try:
        get_births_of_the_day(CHANNEL_UK)
        logger.success(f'Nascidos enviada o canal {CHANNEL_UK}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho nascido:', str(e))


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-uk.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_UK):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>СЬОГОДНІ В ІСТОРІЇ</b>\n\n📅 | Подія в <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 Ви знали? Підписуйтеся на @istoriya_uks.</blockquote>'
            bot.send_message(CHANNEL_UK, message)
        else:
            bot.send_message(
                CHANNEL_UK,
                '<b>На сьогодні нічого не знайдено</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_UK}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_UK_events():
    try:
        send_historical_events_channel(CHANNEL_UK)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_UK}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_UK_alert():

    try:
        повідомлення = "🌟 📺 <b>Приєднуйтесь до нашого неймовірного каналу історії!</b> 📺 🌟\n\n"\
            "Друзі, відкрийте для себе чарівність історії через наші захоплюючі та захопливі канали! "\
            "Приєднуйтесь зараз, щоб насолодитися широким спектром програм та документальних фільмів, "\
            "що введуть вас у захоплюючу подорож у глибини історії.\n\n"\
            "Відчуйте давні пригоди, захоплюючі факти та ключові події, які сформували наш світ. "\
            "Приєднуйтесь до нас сьогодні для приємного та просвітницького освітнього досвіду!\n\n"\
            "🌍 Натисніть посилання, щоб приєднатися до списку історичних каналів: [@history_channels]"\

        bot.send_message(
            CHANNEL_UK,
            повідомлення,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Помилка під час надсилання історичних фактів до каналу:', str(e))

def get_curiosity_UK(CHANNEL_UK):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-uk.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")
                message = f'<b>Історична цікавинка 📜</b>\n\n{info}\n\n<blockquote>💬 Чи знали ви? Слідкуйте за @hoy_en_la_historia.</blockquote>'
                bot.send_message(CHANNEL_UK, message)
            else:

                logger.info('Немає інформації на сьогодні.')

    except Exception as e:

        logger.error('Помилка отримання інформації:', str(e))


def hist_channel_curiosity_UK():
    try:
        get_curiosity_UK(CHANNEL_UK)

        logger.success(f'Цікавинка надіслана до каналу {CHANNEL_UK}')

    except Exception as e:

        logger.error('Помилка відправлення цікавинки до каналу:', str(e))

with open(
    './data/presidents/presidents-uk.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_UK():
    try:
        if db.presidents_uk.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_uk_db(new_id, new_date)
            send_info_through_channel_UK(president)
        else:
            last_president = (
                db.presidents_uk.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Updating information of the last president to the current date.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_uk.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_UK(next_president)
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


def send_info_through_channel_UK(president_info):
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
            f'<b>Ім’я:</b> {name}\n'
            f'<b>Інформація:</b> {position}° {title}\n'
            f'<b>Партія:</b> {party}\n'
            f'<b>Рік у владі:</b> {term_year}\n'
            f'<b>Віце-президент:</b> {vice_president}\n'
            f'<b>Місцезнаходження:</b> {where}\n\n'
            f'<blockquote>💬 Знаєте?</blockquote>'
        )

        logger.success('Фотографію президента відправлено успішно!')

        bot.send_photo(
            CHANNEL_UK, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Помилка під час відправлення фотографії президента: {str(e)}')
