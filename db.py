from pymongo import ASCENDING, MongoClient
import configparser
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
bot_conf_path = os.path.join(script_directory, '..', 'bot.conf')

config = configparser.ConfigParser()
config.read(bot_conf_path)
from logger import logger

MONGO_CON = config['DB']['MONGO_CON']

try:

    logger.info('ℹ️ INITIATING CONNECTION WITH MONGODB')

    client = MongoClient(MONGO_CON)
    db = client.historicalevents
    logger.success('✅ Connection to MongoDB established successfully!')

except Exception as e:
    logger.error(f'❗️ Error connecting to MongoDB: {e}')

def add_presidents_ar_db(id, date):
    return db.presidents_ar.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_cs_db(id, date):
    return db.presidents_cs.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_de_db(id, date):
    return db.presidents_de.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_es_db(id, date):
    return db.presidents_es.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_fr_db(id, date):
    return db.presidents_fr.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_hi_db(id, date):
    return db.presidents_hi.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_id_db(id, date):
    return db.presidents_id.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_it_db(id, date):
    return db.presidents_it.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_ja_db(id, date):
    return db.presidents_ja.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_ko_db(id, date):
    return db.presidents_ko.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_pl_db(id, date):
    return db.presidents_pl.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_ru_db(id, date):
    return db.presidents_ru.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_tr_db(id, date):
    return db.presidents_tr.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_uk_db(id, date):
    return db.presidents_uk.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_vi_db(id, date):
    return db.presidents_vi.insert_one(
        {
            'id': id,
            'date': date,
        }
    )

def add_presidents_zh_db(id, date):
    return db.presidents_zh.insert_one(
        {
            'id': id,
            'date': date,
        }
    )


def search_id_presidente(id):
    return db.presidentes.find_one({'id': id})


def search_date_presidente(date):
    return db.presidentes.find_onde({'date': date})