from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_vi_db


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
        tin_nhan = "🌟 📺 <b>Tham gia kênh Lịch sử tuyệt vời của chúng tôi!</b> 📺 🌟\n\n"\
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


def get_curiosity_VI(CHANNEL_VI):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-vi.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")
                message = f'<b>Những điều tò mò về lịch sử 📜 📜</b>\n\n{info}\n\n<blockquote>💬 Bạn có biết không? Theo @hist_vi.</blockquote>'
                bot.send_message(CHANNEL_VI, message)
            else:

                logger.info('No hay información para el día de hoy.')

    except Exception as e:

        logger.error('Error al obtener información:', str(e))


def hist_channel_curiosity_VI():
    try:
        get_curiosity_VI(CHANNEL_VI)

        logger.success(f'Curiosidad enviada al canal {CHANNEL_VI}')

    except Exception as e:

        logger.error('Error al enviar la curiosidad al canal:', str(e))

with open(
    './data/presidents/presidents-vi.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_VI():
    try:
        if db.presidents_vi.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_vi_db(new_id, new_date)
            send_info_through_CHANNEL_VI(president)
        else:
            last_president = (
                db.presidents_vi.find().sort([('_id', -1)]).limit(1)[0]
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
                    db.presidents_vi.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_CHANNEL_VI(next_president)
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


def send_info_through_CHANNEL_VI(president_info):
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
            f'<b>Tên:</b> {name}\n'
            f'<b>Thông tin:</b> {position}° {title}\n'
            f'<b>Đảng:</b> {party}\n'
            f'<b>Năm nhiệm kỳ:</b> {term_year}\n'
            f'<b>Phó Tổng thống:</b> {vice_president}\n'
            f'<b>Địa điểm:</b> {where}\n\n'
            f'<blockquote>💬 Bạn có biết không? Theo dõi @hist_vi.</blockquote>'
        )

        logger.success('¡Envío del presidente completado con éxito!')

        bot.send_photo(
            CHANNEL_VI, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Error al enviar la foto del presidente: {str(e)}')