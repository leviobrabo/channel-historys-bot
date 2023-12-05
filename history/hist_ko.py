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
            '../data/events-ko.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_KO):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>오늘의 역사</b>\n\n📅 | {day}/{month} 이벤트\n\n{events}\n\n💬 알고 계셨나요? @yeogsa_kr 를 팔로우하세요.'

            bot.send_message(CHANNEL_KO, message)
        else:
            bot.send_message(
                CHANNEL_KO,
                '<b>오늘 검색된 항목이 없습니다.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_KO}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_KO_events():
    try:
        send_historical_events_channel(CHANNEL_KO)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_KO}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_KO_alert():
    try:
        message = "🌟 📺 **우리의 멋진 역사 채널에 참여해보세요!** 📺 🌟\n\n"\
            "친구들, 우리의 매력적이고 스릴 넘치는 채널을 통해 역사의 마법을 발견해보세요! "\
            "지금 참여하여 역사의 심연으로 데려다주는 다양한 프로그램과 다큐멘터리를 즐겨보세요.\n\n"\
            "고대의 모험, 흥미로운 사실, 우리 세계를 형성한 중요한 사건을 경험해보세요. "\
            "즐거운 교육적 경험을 위해 오늘 우리와 함께하세요!\n\n"\
            "🌍 역사 채널 목록에 참여하려면 링크를 클릭하세요: [@history_channels]"\

        bot.send_message(
            CHANNEL_KO,
            message,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('채널로 역사적 사실을 전송하는 중 오류가 발생했습니다:', str(e))
