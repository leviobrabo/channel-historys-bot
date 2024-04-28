from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_ko_db


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-ko.json', 'r', encoding='utf-8'
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
            message = f'<b>오늘의 역사</b>\n\n📅 | {day}/{month} 이벤트\n\n{events}\n\n<blockquote>💬 알고 계셨나요? @yeogsa_kr 를 팔로우하세요.</blockquote>'

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
        message = "🌟 📺 <b>우리의 멋진 역사 채널에 참여해보세요!</b> 📺 🌟\n\n"\
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

def get_curiosity_KO(CHANNEL_KO):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-ko.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")
                message = f'<b>역사적 호기심 📜</b>\n\n{info}\n\n<blockquote>💬 알고 계셨나요? 따르다 @yeogsa_kr.</blockquote>'
                bot.send_message(CHANNEL_KO, message)
            else:

                logger.info('오늘은 정보가 없습니다.')

    except Exception as e:

        logger.error('정보를 가져오는 중 오류 발생:', str(e))


def hist_channel_curiosity_KO():
    try:
        get_curiosity_KO(CHANNEL_KO)

        logger.success(f'큐리오시다드 엔비아다 알 카날 {CHANNEL_KO}')

    except Exception as e:

        logger.error('채널에 호기심을 보내는 중에 오류가 발생했습니다.', str(e))

with open(
    './data/presidents/presidents-ko.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_KO():
    try:
        if db.presidents_ko.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_ko_db(new_id, new_date)
            send_info_through_CHANNEL_KO(president)
        else:
            last_president = (
                db.presidents_ko.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    '지난 대통령부터 현재 날짜까지 정보 업데이트.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_ko.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_CHANNEL_KO(next_president)
                else:

                    logger.error('더 이상 보낼 대통령이 없다.')

            else:

                logger.info(
                    "아직은 차기 대통령에 대한 정보를 보낼 때가 아니다.."
                )

    except Exception as e:

        logger.error(
            f'대통령 정보 전송 중 오류가 발생했습니다.: {str(e)}'
        )


def send_info_through_CHANNEL_KO(president_info):
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
            f'<b>이름:</b> {name}\n'
            f'<b>정보:</b> {position}° {title}\n'
            f'<b>정당:</b> {party}\n'
            f'<b>임기 연도:</b> {term_year}\n'
            f'<b>부통령:</b> {vice_president}\n'
            f'<b>장소:</b> {where}\n\n'
            f'<blockquote>💬 알고 계셨나요? @yeogsa_kr를 팔로우하세요.</blockquote>'
        )

        logger.success('대통령 전송 성공!')

        bot.send_photo(
            CHANNEL_KO, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'대통령 사진을 전송하는 중 오류 발생: {str(e)}')
