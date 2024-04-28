from logger import *
import random
from datetime import datetime
from bot import *
import pytz
import requests
from telebot import types
import json
from db import db, add_presidents_ar_db


def send_historical_events_CHANNEL_AR_image(CHANNEL_AR):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://ar.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
        )
        events = response.json().get('events', [])
        events_with_photo = [
            event
            for event in events
            if event.get('pages') and event['pages'][0].get('thumbnail')
        ]

        random_event = random.choice(events_with_photo)
        event_text = random_event.get('text', '')
        event_year = random_event.get('year', '')

        if not events_with_photo:
            logger.info('Não há eventos com fotos para enviar hoje.')
            return

        random_event = random.choice(events_with_photo)
        caption = f'<b>🖼 | تاريخ مصور </b>\n\nفي <b>{day} {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>\n\n<blockquote>💬 هل تعلم؟ تابع @tarikh_yawm.</blockquote>'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL_AR, photo_url, caption=caption, **options)
        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL_AR}.'
        )
    except Exception as e:
        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_CHANNEL_AR_imgs():
    try:
        send_historical_events_CHANNEL_AR_image(CHANNEL_AR)
        logger.success(f'Mensagem enviada o canal {CHANNEL_AR}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho imgs:', str(e))


def get_month_name(month):
    month_names = [
        'يناير',
        'فبراير',
        'مارس',
        'أبريل',
        'مايو',
        'يونيو',
        'يوليو',
        'أغسطس',
        'سبتمبر',
        'أكتوبر',
        'نوفمبر',
        'ديسمبر',
    ]
    return month_names[month]


def get_deaths_of_the_day(CHANNEL_AR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        response = requests.get(
            f'https://ar.wikipedia.org/api/rest_v1/feed/onthisday/deaths/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            deaths = data.get('deaths', [])

            if len(deaths) > 0:
                death_messages = []

                for index, death in enumerate(deaths[:5], start=1):
                    name = f"<b>{death.get('text', '')}</b>"
                    info = death.get('pages', [{}])[0].get(
                        'extract', 'Informações não disponíveis.'
                    )
                    date = death.get('year', 'Data desconhecida.')

                    death_message = f'<i>{index}.</i> <b>الاسم:</b> {name}\n<b>المعلومات:</b> {info}\n<b>تاريخ الوفاة:</b> {date}'
                    death_messages.append(death_message)

                message = f'<b>⚰️ |  الوفيات في هذا اليوم: {day} من {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(death_messages)
                message += '\n\n<blockquote>💬 هل كنت تعلم؟ تابع @tarikh_yawm.</blockquote>'

                bot.send_message(CHANNEL_AR, message)
            else:

                logger.info(
                    'Não há informações sobre mortos para o dia atual.'
                )

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao enviar mortos para os canal:', str(e))


def hist_CHANNEL_AR_death():
    try:
        get_deaths_of_the_day(CHANNEL_AR)
        logger.success(f'Mortos enviada o canal {CHANNEL_AR}')
    except Exception as e:
        logger.info('Erro ao enviar o trabalho mortes:', str(e))


def get_births_of_the_day(CHANNEL_AR):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://ar.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            births = data.get('births', [])

            if len(births) > 0:
                birth_messages = []

                for index, birth in enumerate(births[:5], start=1):
                    name = f"<b>{birth.get('text', '')}</b>"
                    info = birth.get('pages', [{}])[0].get(
                        'extract', 'Informações não disponíveis.'
                    )
                    date = birth.get('year', 'Data desconhecida.')

                    birth_message = f'<i>{index}.</i> <b>الاسم:</b> {name}\n<b>المعلومات:</b> {info}\n<b>تاريخ الميلاد:</b> {date}'
                    birth_messages.append(birth_message)

                message = f'<b>🎂 | الأعياد في هذا اليوم: {day} من {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n<blockquote>💬 هل كنت تعلم؟ تابع @tarikh_yawm.</blockquote>'

                bot.send_message(CHANNEL_AR, message)
            else:

                logger.info('Não há informações sobre nascidos hoje.')

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:
        logger.error('Erro ao obter informações:', str(e))


def hist_CHANNEL_AR_birth():
    try:
        get_births_of_the_day(CHANNEL_AR)
        logger.success(f'Nascidos enviada o canal {CHANNEL_AR}')
    except Exception as e:
        logger.error('Erro ao enviar o trabalho nascido:', str(e))


def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    try:
        with open(
            'data/events_ar.json', 'r', encoding='utf-8'
        ) as file:

            json_events = json.load(file)
            events = json_events[f'{month}-{day}']
            if events:
                return '\n\n'.join(events)
            else:
                return None
    except Exception as e:
        logger.error('Error reading events from JSON:', repr(e))
        return None


def send_historical_events_channel(CHANNEL_AR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>اليوم في التاريخ</b>\n\n📅 | حدث في <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 هل كنت تعلم؟ تابع @tarikh_yawm.</blockquote>'
            bot.send_message(CHANNEL_AR, message)
        else:
            bot.send_message(
                CHANNEL_AR,
                '<b>ولا توجد معلومات عن الوفيات لليوم الحالي..</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL_AR}'
            )

    except Exception as e:
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))


def hist_CHANNEL_AR_events():
    try:
        send_historical_events_channel(CHANNEL_AR)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL_AR}')
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))


def message_CHANNEL_AR_alert():
    try:
        message = "🌟 📺 <b>انضم إلى قناتنا المذهلة للتاريخ</b> 📺 🌟\n\n"\
            "الأصدقاء، اكتشفوا سحر التاريخ من خلال قنواتنا الممتعة والمثيرة! "\
            "انضموا إلينا الآن للاستمتاع بمجموعة واسعة من البرامج والوثائقيات "\
            "التي تأخذكم في رحلة مثيرة إلى عمق التاريخ.\n\n"\
            "استمتعوا بالمغامرات القديمة والحقائق المثيرة والأحداث الهامة "\
            "التي شكلت عالمنا. انضموا إلينا اليوم للاستمتاع بتجربة تعليمية ممتعة ومفيدة!\n\n"\
            "🌍 انقر على الرابط للانضمام إلى قائمة قنوات التاريخ: [@history_channels]"\


        bot.send_message(
            CHANNEL_AR,
            message,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))

def get_curiosity_AR(CHANNEL_AR):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './channel-historys/data/curiosity/curiosity-ar.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>الفضول التاريخي 📜</b>\n\n{info}\n\n<blockquote>💬 هل كنت تعلم؟ يتبع @tarikh_yawm.</blockquote>'
                bot.send_message(CHANNEL_AR, message)
            else:

                logger.info('لا توجد معلومات لهذا اليوم.')

    except Exception as e:

        logger.error('خطأ في الحصول على المعلومات:', str(e))


def hist_channel_curiosity_AR():
    try:
        get_curiosity_AR(CHANNEL_AR)

        logger.success(f'تم إرسال الفضول إلى القناة {CHANNEL_AR}')

    except Exception as e:

        logger.error('خطأ في إرسال الفضول إلى القناة:', str(e))

with open(
    './data/presidents/presidents-ar.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo_AR():
    try:
        if db.presidents_ar.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_ar_db(new_id, new_date)
            send_info_through_channel_AR(president)
        else:
            last_president = (
                db.presidents_ar.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            today_str = today.strftime('%Y-%m-%d')

            if last_president['date'] != today_str:

                logger.info(
                    'تحديث معلومات الرئيس الأخير إلى التاريخ الحالي.'
                )

                next_id = last_id + 1
                next_president = presidents.get(str(next_id))
                if next_president:
                    db.presidents_ar.update_one(
                        {'date': last_president['date']},
                        {'$set': {'date': today_str}, '$inc': {'id': 1}},
                    )

                    send_info_through_channel_AR(next_president)
                else:

                    logger.error('لا يوجد المزيد من الرؤساء لإرسالها.')

            else:

                logger.info(
                    "لم يحن الوقت بعد لإرسال معلومات عن الرئيس التالي."
                )

    except Exception as e:

        logger.error(
            f'حدث خطأ أثناء إرسال معلومات الرئيس: {str(e)}'
        )


def send_info_through_channel_AR(president_info):
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
            f'<b>الاسم:</b> {name}\n'
            f'<b>المعلومات:</b> {position}° {title}\n'
            f'<b>الحزب:</b> {party}\n'
            f'<b>سنة الولاية:</b> {term_year}\n'
            f'<b>نائب الرئيس:</b> {vice_president}\n'
            f'<b>الموقع:</b> {where}\n\n'
            f'<blockquote>💬 هل تعلم؟ تابع @tarikh_yawm.</blockquote>'
        )

        logger.success('تم إرسال صورة الرئيس بنجاح!')

        bot.send_photo(
            CHANNEL_AR, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'خطأ في إرسال صورة الرئيس: {str(e)}')
