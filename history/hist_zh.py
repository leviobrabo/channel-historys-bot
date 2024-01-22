from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json


def send_historical_events_CHANNEL_AR_image(CHANNEL_ZH):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://zh.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
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
        caption = f'<b>🖼 | 圖片歷史 </b>\n\n在 <b>{day} {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>\n\n<blockquote>💬 你知道嗎？關注 @history_zh.</blockquote>'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL_ZH, photo_url, caption=caption, **options)
        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL_ZH}.'
        )
    except Exception as e:
        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_CHANNEL_ZH_imgs():
    try:
        send_historical_events_CHANNEL_AR_image(CHANNEL_ZH)
        logger.success(f'Mensagem enviada o canal {CHANNEL_ZH}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho imgs:', str(e))


def get_month_name(month):
    month_names = [
        '一月',
        '二月',
        '三月',
        '四月',
        '五月',
        '六月',
        '七月',
        '八月',
        '九月',
        '十月',
        '十一月',
        '十二月',
    ]
    return month_names[month]


def get_deaths_of_the_day(CHANNEL_ZH):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        response = requests.get(
            f'https://zh.wikipedia.org/api/rest_v1/feed/onthisday/deaths/{month}/{day}',
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

                    death_message = f'<i>{index}.</i> <b>姓名：</b> {name}\n<b>信息：</b> {info}\n<b>死亡日期：</b> {date}'

                    death_messages.append(death_message)

                    message = f'<b>⚰️ | 今天的死亡事件: {day}日 {get_month_name(month)}</b>\n\n'
                    message += '\n\n'.join(death_messages)
                    message += '\n\n<blockquote>💬 你知道嗎？關注 @history_zh.</blockquote>'

                bot.send_message(CHANNEL_ZH, message)
            else:

                logger.info(
                    'Não há informações sobre mortos para o dia atual.'
                )

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao enviar mortos para os canal:', str(e))


def hist_CHANNEL_ZH_death():
    try:
        get_deaths_of_the_day(CHANNEL_ZH)
        logger.success(f'Mortos enviada o canal {CHANNEL_ZH}')
    except Exception as e:
        logger.info('Erro ao enviar o trabalho mortes:', str(e))


def get_births_of_the_day(CHANNEL_ZH):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://zh.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
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

                    birth_message = f'<i>{index}.</i> <b>姓名：</b> {name}\n<b>信息：</b> {info}\n<b>出生日期：</b> {date}'

                    birth_messages.append(birth_message)

                message = f'<b>🎂 | 今天出生的人: {day}日 {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n<blockquote>💬 你知道嗎？關注 @history_zh.</blockquote>'

                bot.send_message(CHANNEL_ZH, message)
            else:

                logger.info('Não há informações sobre nascidos hoje.')

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao obter informações:', str(e))


def hist_CHANNEL_ZH_birth():
    try:
        get_births_of_the_day(CHANNEL_ZH)
        logger.success(f'Nascidos enviada o canal {CHANNEL_ZH}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho nascido:', str(e))


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-zh.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_ZH):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>歷史上的今天</b>\n\n📅 | 事件發生在 <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 你知道嗎？關注 @history_zh.</blockquote>'
            bot.send_message(CHANNEL_ZH, message)
        else:
            bot.send_message(
                CHANNEL_ZH,
                '<b>今天沒有找到任何內容</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_ZH}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_ZH_events():
    try:
        send_historical_events_channel(CHANNEL_ZH)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_ZH}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_ZH_alert():
    try:
        消息 = "🌟 📺 **加入我们精彩的历史频道！** 📺 🌟\n\n"\
            "朋友们，通过我们有趣且激动人心的频道，发现历史的魔力！"\
            "立即加入我们，享受各种节目和纪录片，带您踏上一个引人入胜的历史之旅。\n\n"\
            "体验古老的冒险，引人入胜的事实以及塑造我们世界的关键事件。"\
            "今天就加入我们，享受有趣而富有教育意义的体验！\n\n"\
            "🌍 点击链接加入历史频道列表：[@history_channels]"\

        bot.send_message(
            CHANNEL_ZH,
            消息,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('发送历史事件至频道时出错：', str(e))
