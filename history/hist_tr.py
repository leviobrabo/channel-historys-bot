from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_tr_db


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-tr.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_TR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>TARİHTE BUGÜN</b>\n\n📅 | {day}/{month} tarihindeki olaylar\n\n{events}\n\n<blockquote>💬 Biliyor muydunuz? @bugun_in_history adresinden takip edebilirsiniz.</blockquote>'
            bot.send_message(CHANNEL_TR, message)
        else:
            bot.send_message(
                CHANNEL_TR,
                '<b>Bugün için hiçbir şey bulunamadı</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_TR}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_TR_events():
    try:
        send_historical_events_channel(CHANNEL_TR)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_TR}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_TR_alert():
    try:
        mesaj = "🌟 📺 <b>Harika Tarih Kanalımıza Katılın!</b> 📺 🌟\n\n"\
            "Arkadaşlar, tarihin büyüsünü eğlenceli ve heyecan verici kanallarımız aracılığıyla keşfedin! "\
            "Şimdi katılın ve sizi tarihin derinliklerine götürecek geniş program ve belgesel yelpazemizin tadını çıkarın.\n\n"\
            "Antik maceraları, ilgi çekici gerçekleri ve dünyamızı şekillendiren önemli olayları yaşayın. "\
            "Keyifli ve aydınlatıcı bir eğitim deneyimi için bugün bize katılın!\n\n"\
            "🌍 Tarih Kanalları listesine katılmak için bağlantıya tıklayın: [@history_channels]"\

        bot.send_message(
            CHANNEL_TR,
            mesaj,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('Kanalda tarihi gerçekleri gönderme hatası:', str(e))

def get_curiosity_TR(CHANNEL_TR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-tr.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")
                message = f'<b>Tarihî Meraklar 📜</b>\n\n{info}\n\n<blockquote>💬 Biliyor muydunuz? @bugun_in_history\'yı takip edin.</blockquote>'
                bot.send_message(CHANNEL_TR, message)
            else:

                logger.info('Bugün için bilgi yok.')

    except Exception as e:

        logger.error('Bilgi alınırken hata oluştu:', str(e))


def hist_channel_curiosity_TR():
    try:
        get_curiosity_TR(CHANNEL_TR)

        logger.success(f'Merak bilgisi {CHANNEL_TR} kanalına gönderildi')

    except Exception as e:

        logger.error('Merak bilgisini kanala gönderirken hata:', str(e))

with open(
    './data/presidents/presidents-tr.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_TR():
    try:
        if db.presidents_tr.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_tr_db(new_id, new_date)
            send_info_through_channel_TR(president)
        else:
            last_president = (
                db.presidents_tr.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Son başkanın bilgileri güncelleniyor.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_tr.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_TR(next_president)
                else:

                    logger.error('Gönderilecek başka başkan kalmadı.')

            else:

                logger.info(
                    "Henüz gelecek başkan hakkında bilgi gönderme zamanı değil."
                )

    except Exception as e:

        logger.error(
            f'Başkan bilgisi gönderirken hata oluştu: {str(e)}'
        )


def send_info_through_channel_TR(president_info):
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
            f'<b>İsim:</b> {name}\n'
            f'<b>Bilgi:</b> {position}° {title}\n'
            f'<b>Parti:</b> {party}\n'
            f'<b>Görev Yılı:</b> {term_year}\n'
            f'<b>Yardımcı Başkan:</b> {vice_president}\n'
            f'<b>Yer:</b> {where}\n\n'
            f'<blockquote>💬 Biliyor muydunuz? @bugun_in_history\'yı takip edin.</blockquote>'
        )

        logger.success('Başkan fotoğrafı gönderimi başarılı!')

        bot.send_photo(
            CHANNEL_TR, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Başkan fotoğrafı gönderirken hata: {str(e)}')

