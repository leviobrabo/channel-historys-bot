from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_hi_db


def get_month_name(month):
    month_names = [
        'जनवरी',
        'फ़रवरी',
        'मार्च',
        'अप्रैल',
        'मई',
        'जून',
        'जुलाई',
        'अगस्त',
        'सितंबर',
        'अक्टूबर',
        'नवंबर',
        'दिसंबर',
    ]
    return month_names[month]


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-hi.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_HI):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>आज इतिहास में</b>\n\n📅 | <b>{day}/{month}</b> को घटना\n\n{events}\n\n<blockquote>💬 क्या आप जानते हैं? @itihaas_hi को फॉलो करें।</blockquote>'

            bot.send_message(CHANNEL_HI, message)
        else:
            bot.send_message(
                CHANNEL_HI,
                '<b>आज तक मौतों के बारे में कोई जानकारी नहीं है।</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_HI}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_HI_events():
    try:
        send_historical_events_channel(CHANNEL_HI)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_HI}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_HI_alert():
    try:
        message = "🌟 📺 <b>हमारे शानदार इतिहास चैनल में शामिल हों!</b> 📺 🌟\n\n"\
            "दोस्तों, हमारे मनोरंजक और रोमांचक चैनलों के माध्यम से इतिहास का जादू खोजें! "\
            "अभी हमारे साथ जुड़ें और एक व्यापक कार्यक्रम और डॉक्यूमेंट्री का आनंद लें जो आपको एक रोमांचक यात्रा पर लेकर जाएगा "\
            "इतिहास के गहराईयों में।\n\n"\
            "प्राचीन साहसिक किस्से, रोचक तथ्य और हमारी दुनिया को आकार देने वाले महत्वपूर्ण घटनाओं का अनुभव करें। "\
            "एक मनोरंजन से भरपूर और ज्ञानवर्धक शैक्षिक अनुभव के लिए आज हमारे साथ जुड़ें!\n\n"\
            "🌍 इतिहास चैनल की सूची में शामिल होने के लिए लिंक पर क्लिक करें: [@history_channels]"\

        bot.send_message(
            CHANNEL_HI,
            message,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('चैनल में ऐतिहासिक तथ्यों को भेजने में त्रुटि:', str(e))


def get_curiosity_HI(CHANNEL_HI):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-hi.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>ऐतिहासिक जिज्ञासाएँ 📜</b>\n\n{info}\n\n<blockquote>💬 क्या आप जानते हैं? अनुसरण करना @itihaas_hi.</blockquote>'
                bot.send_message(CHANNEL_HI, message)
            else:

                logger.info('आज के लिए कोई जानकारी उपलब्ध नहीं है।')

    except Exception as e:

        logger.error('जानकारी प्राप्त करने में त्रुटि:', str(e))


def hist_channel_curiosity_HI():
    try:
        get_curiosity_HI(CHANNEL_HI)

        logger.success(f'करियोसिटी {CHANNEL_HI} चैनल पर भेजी गई।')

    except Exception as e:

        logger.error('करियोसिटी को चैनल पर भेजने में त्रुटि:', str(e))

with open(
    './data/presidents/presidents-hi.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_HI():
    try:
        if db.presidents_hi.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_hi_db(new_id, new_date)
            send_info_through_channel_HI(president)
        else:
            last_president = (
                db.presidents_hi.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'अंतिम राष्ट्रपति की जानकारी को आज के लिए अपडेट किया जा रहा है।'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_hi.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_HI(next_president)
                else:

                    logger.error('और कोई राष्ट्रपति भेजने के लिए नहीं है।')

            else:

                logger.info(
                    "अगले राष्ट्रपति के बारे में जानकारी भेजने का समय अभी नहीं आया है।"
                )

    except Exception as e:

        logger.error(
            f'राष्ट्रपति जानकारी भेजते समय त्रुटि हुई: {str(e)}'
        )


def send_info_through_channel_HI(president_info):
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
            f'<b>नाम:</b> {name}\n'
            f'<b>जानकारी:</b> {position}° {title}\n'
            f'<b>पार्टी:</b> {party}\n'
            f'<b>कार्यकाल वर्ष:</b> {term_year}\n'
            f'<b>उप-राष्ट्रपति:</b> {vice_president}\n'
            f'<b>स्थान:</b> {where}\n\n'
            f'<blockquote>💬 क्या आप जानतेv हैं? @itihaas_hi को फॉलो करें।</blockquote>'
        )

        logger.success('राष्ट्रपति की तस्वीर भेजना सफल रहा!')

        bot.send_photo(
            CHANNEL_HI, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'राष्ट्रपति की फोटो भेजते समय त्रुटि: {str(e)}')
