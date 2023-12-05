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
            '../data/events-ja.json', 'r', encoding='utf-8'
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
            message = f'<b>歴史上の今日</b>\n\n📅 | {day}/{month}の出来事\n\n{events}\n\n💬 知っていましたか？ @Rekishi_ja をフォローしてください。'

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
        message = "🌟 📺 **当社の素晴らしい歴史チャンネルに参加しましょう！** 📺 🌟\n\n"\
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
