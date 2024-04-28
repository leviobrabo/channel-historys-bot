from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_cs_db


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-cs.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_CS):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>DNEŠNÍ UDÁLOSTI V HISTORII</b>\n\n📅 | Událost dne <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 Věděli jste? Sledujte @dnes_v_historii</blockquote>'
            bot.send_message(CHANNEL_CS, message)
        else:
            bot.send_message(
                CHANNEL_CS,
                '<b>Pro aktuální den nejsou žádné informace o úmrtích.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_CS}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_CS_events():
    try:
        send_historical_events_channel(CHANNEL_CS)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_CS}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_CS_alert():
    try:
        zprava = "🌟 📺 <b>Připojte se k našemu úžasnému kanálu historie!</b> 📺 🌟\n\n"\
            "Přátelé, objevte kouzlo historie prostřednictvím našich zábavných a vzrušujících kanálů! "\
            "Přidejte se k nám nyní a užijte si širokou škálu programů a dokumentů, které vás zavedou na "\
            "vzrušující cestu do hlubin historie.\n\n"\
            "Zažijte starověké dobrodružství, zajímavé fakty a klíčové události, které formovaly náš svět. "\
            "Přidejte se k nám dnes pro příjemný a osvěžující vzdělávací zážitek!\n\n"\
            "🌍 Klepněte na odkaz pro připojení k seznamu historických kanálů: [@history_channels]"\

        bot.send_message(
            CHANNEL_CS,
            zprava,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Chyba při odesílání historických faktů do kanálu:', str(e))


def get_curiosity_CS(CHANNEL_CS):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-cs.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>Historické kuriozity 📜</b>\n\n{info}\n\n<blockquote>💬 Věděl jsi? Následovat @dnes_v_historii.</blockquote>'
                bot.send_message(CHANNEL_CS, message)
            else:

                logger.info('Pro dnešní den nejsou k dispozici žádné informace.')

    except Exception as e:

        logger.error('Chyba při získávání informací:', str(e))


def hist_channel_curiosity_CS():
    try:
        get_curiosity_CS(CHANNEL_CS)

        logger.success(f'Zvědavost odeslána do kanálu {CHANNEL_CS}')

    except Exception as e:

        logger.error('Chyba při odesílání zvědavosti do kanálu:', str(e))

with open(
    './data/presidents/presidents-cs.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_CS():
    try:
        if db.presidents_cs.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_cs_db(new_id, new_date)
            send_info_through_CHANNEL_CS(president)
        else:
            last_president = (
                db.presidents_cs.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Aktualizace informací o posledním prezidentovi na aktuální datum.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_cs.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_CHANNEL_CS(next_president)
                else:

                    logger.error('Nejsou žádní další prezidenti k odeslání.')

            else:

                logger.info(
                    "Ještě nenastal čas poslat informace o dalším prezidentovi."
                )

    except Exception as e:

        logger.error(
            f'Při odesílání informací o prezidentovi došlo k chybě: {str(e)}'
        )


def send_info_through_CHANNEL_CS(president_info):
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
            f'<b>Jméno:</b> {name}\n'
            f'<b>Informace:</b> {position}° {title}\n'
            f'<b>Strana:</b> {party}\n'
            f'<b>Rok v úřadu:</b> {term_year}\n'
            f'<b>Místopředseda:</b> {vice_president}\n'
            f'<b>Umístění:</b> {where}\n\n'
            f'<blockquote>💬 Věděli jste? Sledujte @dnes_v_historii.</blockquote>'
        )

        logger.success('Odeslání fotky prezidenta bylo úspěšné!')

        bot.send_photo(
            CHANNEL_CS, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Chyba při odesílání fotky prezidenta: {str(e)}')

