from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_id_db


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
            message = f'<b>HARI INI DALAM SEJARAH</b>\n\n📅 | Peristiwa pada <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 Tahukah Anda? Ikuti @sejararah_in.</blockquote>'
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
        pesan = "🌟 📺 <b>Bergabunglah dengan Saluran Sejarah kami yang menakjubkan!</b> 📺 🌟\n\n"\
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


def get_curiosity_ID(CHANNEL_ID):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-id.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>Keingintahuan Sejarah 📜</b>\n\n{info}\n\n<blockquote>💬 Tahukah kamu? Mengikuti @sejararah_in.</blockquote>'
                bot.send_message(CHANNEL_ID, message)
            else:

                logger.info('Tidak ada informasi untuk hari ini.')

    except Exception as e:

        logger.error('Gagal mendapatkan informasi:', str(e))


def hist_channel_curiosity_ID():
    try:
        get_curiosity_ID(CHANNEL_ID)

        logger.success(f'Keraguan dikirim ke saluran {CHANNEL_ID}')

    except Exception as e:

        logger.error('Gagal mengirimkan rasa ingin tahu ke saluran:', str(e))

with open(
    './data/presidents/presidents-id.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_ID():
    try:
        if db.presidents_id.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_id_db(new_id, new_date)
            send_info_through_channel_ID(president)
        else:
            last_president = (
                db.presidents_id.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Memperbarui informasi presiden terakhir untuk tanggal saat ini.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_id.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_ID(next_president)
                else:

                    logger.error('Tidak ada presiden lagi untuk dikirim.')

            else:

                logger.info(
                    "Belum saatnya untuk mengirim informasi tentang presiden berikutnya."
                )

    except Exception as e:

        logger.error(
            f'Terjadi kesalahan saat mengirim informasi presiden: {str(e)}'
        )


def send_info_through_channel_ID(president_info):
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
            f'<b>Nama:</b> {name}\n'
            f'<b>Informasi:</b> {position}° {title}\n'
            f'<b>Partai:</b> {party}\n'
            f'<b>Tahun Masa Jabatan:</b> {term_year}\n'
            f'<b>Wakil Presiden:</b> {vice_president}\n'
            f'<b>Lokasi:</b> {where}\n\n'
            f'<blockquote>💬 Tahukah Anda? Ikuti @sejararah_in.</blockquote>'
        )

        logger.success('Pengiriman presiden berhasil!')

        bot.send_photo(
            CHANNEL_ID, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Gagal mengirimkan foto presiden: {str(e)}')
