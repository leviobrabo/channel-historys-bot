from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_pl_db


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events-pl.json', 'r', encoding='utf-8'
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


def send_historical_events_channel(CHANNEL_PL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>DZIŚ W HISTORII</b>\n\n📅 | Wydarzenia w dniu <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 Czy wiedziałeś? Śledź @dzisiaj_w_historii.</blockquote>'

            bot.send_message(CHANNEL_PL, message)
        else:
            bot.send_message(
                CHANNEL_PL,
                '<b>Nic nie znaleziono na dzisiaj</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_PL}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_PL_events():
    try:
        send_historical_events_channel(CHANNEL_PL)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_PL}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_PL_alert():
    try:
        wiadomosc = "🌟 📺 <b>Dołącz do naszego niesamowitego kanału historycznego!</b> 📺 🌟\n\n"\
            "Znajomi, odkryj magię historii poprzez nasze angażujące i ekscytujące kanały! "\
            "Dołącz już teraz, aby cieszyć się szeroką gamą programów i dokumentów, które zabiorą cię w "\
            "pasjonującą podróż w głąb historii.\n\n"\
            "Doświadcz starożytnych przygód, fascynujących faktów i kluczowych wydarzeń, które kształtowały nasz świat. "\
            "Dołącz do nas już dziś, by mieć przyjemne i pouczające doświadczenie edukacyjne!\n\n"\
            "🌍 Kliknij link, aby dołączyć do listy kanałów historycznych: [@history_channels]"\

        bot.send_message(
            CHANNEL_PL,
            wiadomosc,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Błąd podczas wysyłania faktów historycznych do kanału:', str(e))

def get_curiosity_PL(CHANNEL_PL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-pl.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")
                message = f'<b>Ciekawostki Historyczne 📜</b>\n\n{info}\n\n<blockquote>💬 Czy wiesz? Śledź @dzisiaj_w_historii.</blockquote>'
                bot.send_message(CHANNEL_PL, message)
            else:

                logger.info('Brak informacji na dzisiaj.')

    except Exception as e:

        logger.error('Błąd podczas pobierania informacji:', str(e))


def hist_channel_curiosity_PL():
    try:
        get_curiosity_PL(CHANNEL_PL)

        logger.success(f'Ciekawostka wysłana na kanał {CHANNEL_PL}')

    except Exception as e:

        logger.error('Błąd podczas wysyłania ciekawostki na kanał:', str(e))

with open(
    './data/presidents/presidents-pl.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_PL():
    try:
        if db.presidents_pl.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_pl_db(new_id, new_date)
            send_info_through_channel_PL(president)
        else:
            last_president = (
                db.presidents_pl.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'Aktualizacja informacji o ostatnim prezydencie na dzisiejszą datę.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_pl.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_PL(next_president)
                else:

                    logger.error('Brak więcej prezydentów do wysłania.')

            else:

                logger.info(
                    "To jeszcze nie czas na wysłanie informacji o następnym prezydencie."
                )

    except Exception as e:

        logger.error(
            f'Wystąpił błąd podczas wysyłania informacji o prezydencie: {str(e)}'
        )


def send_info_through_channel_PL(president_info):
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
            f'<b>Imię:</b> {name}\n'
            f'<b>Informacja:</b> {position}° {title}\n'
            f'<b>Partia:</b> {party}\n'
            f'<b>Rok Kadencji:</b> {term_year}\n'
            f'<b>Wiceprezydent:</b> {vice_president}\n'
            f'<b>Lokalizacja:</b> {where}\n\n'
            f'<blockquote>💬 Czy wiesz? Śledź @dzisiaj_w_historii.</blockquote>'
        )

        logger.success('Wysłano zdjęcie prezydenta pomyślnie!')

        bot.send_photo(
            CHANNEL_PL, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Błąd podczas wysyłania zdjęcia prezydenta: {str(e)}')


