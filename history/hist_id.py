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
            'data/events-id.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_ID):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>HARI INI DALAM SEJARAH</b>\n\n📅 | Peristiwa pada <b>{day}/{month}</b>\n\n{events}\n\n💬 Tahukah Anda? Ikuti @sejararah_in.'
            bot.send_message(CHANNEL_ID, message)
        else:
            bot.send_message(
                CHANNEL_ID,
                '<b>Tidak ada informasi mengenai kematian pada hari ini.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_ID}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_ID_events():
    try:
        send_historical_events_channel(CHANNEL_ID)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_ID}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_ID_alert():
    try:
        pesan = "🌟 📺 **Bergabunglah dengan Saluran Sejarah kami yang menakjubkan!** 📺 🌟\n\n"\
            "Teman-teman, temukan keajaiban sejarah melalui saluran-saluran kami yang menarik dan mendebarkan! "\
            "Bergabunglah sekarang untuk menikmati beragam program dan dokumenter yang membawa Anda dalam perjalanan "\
            "seru ke kedalaman sejarah.\n\n"\
            "Alami petualangan zaman kuno, fakta menarik, dan peristiwa penting yang membentuk dunia kita. "\
            "Bergabunglah hari ini untuk pengalaman pendidikan yang menyenangkan dan memberi pengetahuan!\n\n"\
            "🌍 Klik tautan untuk bergabung dalam daftar Saluran Sejarah: [@history_channels]"\

        bot.send_message(
            CHANNEL_ID,
            pesan,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Kesalahan dalam mengirim fakta sejarah ke saluran:', str(e))
