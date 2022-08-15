import sqlite3
from random import randint
from sqlite3 import Connection, IntegrityError
import logging

# Logging settings
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

DATABASE_NAME_BARCODE = "../../databases/barcode.sqlite"

SQL_QUERY_FOR_TABLE_NAMES = 'select name from sqlite_master'

SQL_QUERY_TO_CREATE_BARCODE_TABLE = '''create table barcodes
                (
                    barcode TEXT
                        primary key,
                        type TEXT not null,
                    constraint "Barcode Length Check"
                        check (length(barcode) is 13)
                );'''

SQL_QUERY_TO_INSERT_INTO_BARCODES = '''
    insert into barcodes values (%s, %s);
'''


def sqlite3_connection(database_name: str) -> Connection:
    connection = sqlite3.connect(database_name)
    return connection


def check_table_or_create_if_missing(table_name: str) -> bool:
    connection = sqlite3_connection(DATABASE_NAME_BARCODE)
    cursor = connection.cursor()
    try:
        if (table_name,) not in cursor.execute(SQL_QUERY_FOR_TABLE_NAMES):
            logger.info(f"Creating table {table_name}")
            cursor.execute(SQL_QUERY_TO_CREATE_BARCODE_TABLE)
        return True
    except Exception as e:
        logger.error("Error occurred during checking if the table name exists/ creation of the said table %s", e)
    finally:
        connection.close()


def barcode_generator() -> str:
    return "".join(list(map(str, [randint(0, 9) for _ in range(13)])))


def create_barcode(type_of_barcode: str):
    con = sqlite3_connection(DATABASE_NAME_BARCODE)
    cur = con.cursor()
    while True:
        try:
            query = f"insert into barcodes values ('{barcode_generator()}', '{type_of_barcode}');"
            print(query)
            cur.execute(query)
            break
        except IntegrityError as e:
            logger.info("Barcode already existing, attempting for a new barcode", e)
        finally:
            con.commit()
            con.close()
