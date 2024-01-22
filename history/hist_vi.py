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
            'data/events-vi.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_VI):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>HÔM NAY TRONG LỊCH SỬ</b>\n\n📅 | Sự kiện vào ngày <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 Bạn có biết không? Theo dõi @hist_vi.</blockquote>'

            bot.send_message(CHANNEL_VI, message)
        else:
            bot.send_message(
                CHANNEL_VI,
                '<b>Không tìm thấy gì cho ngày hôm nay</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_VI}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_VI_events():
    try:
        send_historical_events_channel(CHANNEL_VI)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_VI}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_VI_alert():
    try:
        tin_nhan = "🌟 📺 **Tham gia kênh Lịch sử tuyệt vời của chúng tôi!** 📺 🌟\n\n"\
            "Bạn bè, khám phá phép màu của lịch sử qua những kênh thú vị và hấp dẫn của chúng tôi! "\
            "Tham gia ngay để tận hưởng một loạt các chương trình và tài liệu mang bạn vào một chuyến "\
            "phiêu lưu hấp dẫn vào đáy của lịch sử.\n\n"\
            "Trải nghiệm những cuộc phiêu lưu cổ xưa, những sự thật hấp dẫn và những sự kiện quan trọng "\
            "đã định hình thế giới của chúng ta. Tham gia ngay hôm nay để có một trải nghiệm giáo dục thú vị và bổ ích!\n\n"\
            "🌍 Nhấp vào liên kết để tham gia vào danh sách các kênh Lịch sử: [@history_channels]"\

        bot.send_message(
            CHANNEL_VI,
            tin_nhan,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('Lỗi khi gửi các sự kiện lịch sử đến kênh:', str(e))
