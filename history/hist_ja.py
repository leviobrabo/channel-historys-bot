from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_ja_db


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-ja.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_JA):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>歴史上の今日</b>\n\n📅 | {day}/{month}の出来事\n\n{events}\n\n<blockquote>💬 知っていましたか？ @Rekishi_ja をフォローしてください。</blockquote>'

            bot.send_message(CHANNEL_JA, message)
        else:
            bot.send_message(
                CHANNEL_JA,
                '<b>今日は何も見つかりませんでした</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_JA}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_JA_events():
    try:
        send_historical_events_channel(CHANNEL_JA)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_JA}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_JA_alert():
    try:
        message = "🌟 📺 <b>当社の素晴らしい歴史チャンネルに参加しましょう！</b> 📺 🌟\n\n"\
            "皆さん、私たちの魅力的でスリリングなチャンネルを通じて歴史の魔法を発見してください！"\
            "幅広いプログラムやドキュメンタリーをお楽しみいただくために、今すぐご参加ください。これらはあなたを歴史の深みに連れて行きます。\n\n"\
            "古代の冒険、興味深い事実、私たちの世界を形作った重要な出来事を体験してください。"\
            "楽しくて有益な教育的な体験のため、今日私たちに参加してください！\n\n"\
            "🌍 ヒストリーチャンネルのリストに参加するにはリンクをクリックしてください：[@history_channels]"\

        bot.send_message(
            CHANNEL_JA,
            message,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('チャンネルへの歴史的な事実の送信中にエラーが発生しました：', str(e))

def get_curiosity_JA(CHANNEL_JA):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-ja.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')
                
                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")
                message = f'<b>歴史的珍品 📜</b>\n\n{info}\n\n<blockquote>💬 知っていましたか？ フォローする @Rekishi_ja.</blockquote>'
                bot.send_message(CHANNEL, message)
            else:

                logger.info('今日の情報はありません。')

    except Exception as e:

        logger.error('情報の取得中にエラーが発生しました:', str(e))


def hist_channel_curiosity_JA():
    try:
        get_curiosity_JA(CHANNEL_JA)

        logger.success(f'好奇心を{CHANNEL_JA}チャンネルに送信しました')

    except Exception as e:

        logger.error('チャンネルへの好奇心の送信中にエラーが発生しました:', str(e))

with open(
    './data/presidents/presidents-ja.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_JA():
    try:
        if db.presidents_ja.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_ja_db(new_id, new_date)
            send_info_through_channel_JA(president)
        else:
            last_president = (
                db.presidents_ja.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    '最後の大統領の情報を現在の日付に更新します。'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_ja.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_JA(next_president)
                else:

                    logger.error('送信する大統領の情報がもうありません。')

            else:

                logger.info(
                    "次の大統領の情報を送信するのはまだ早いです。"
                )

    except Exception as e:

        logger.error(
            f'大統領情報の送信中にエラーが発生しました: {str(e)}'
        )


def send_info_through_channel_JA(president_info):
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
            f'<b>名前:</b> {name}\n'
            f'<b>情報:</b> {position}° {title}\n'
            f'<b>党:</b> {party}\n'
            f'<b>任期年:</b> {term_year}\n'
            f'<b>副大統領:</b> {vice_president}\n'
            f'<b>場所:</b> {where}\n\n'
            f'<blockquote>💬 知ってましたか？ @Rekishi_ja をフォローしてください。</blockquote>'
        )

        logger.success('大統領の送信が成功しました！')

        bot.send_photo(
            CHANNEL_JA, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'大統領の写真の送信中にエラーが発生しました: {str(e)}')
