import sqlite3
from sqlite3 import Connection
import logging

# Logging settings
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


DATABASE_NAME_BARCODE = "../../databases/barcode.sqlite"

SQL_QUERY_FOR_TABLE_NAMES = 'select name from sqlite_master'


def sqlite3_connection(database_name: str) -> Connection:
    connection = sqlite3.connect(database_name)
    return connection


def check_table_or_create_if_missing(table_name: str) -> bool:
    connection = sqlite3_connection(DATABASE_NAME_BARCODE)
    cursor = connection.cursor()
    try:
        if (table_name,) not in cursor.execute(SQL_QUERY_FOR_TABLE_NAMES):
            logger.info(f"Creating table {table_name}")
            cursor.execute('''create table barcodes
                            (
                                barcode TEXT
                                    primary key,
                                constraint "Barcode Length Check"
                                    check (length(barcode) is 13)
                            );''')
        return True
    except Exception as e:
        logger.error("Error occured during checking if the table name exists/ creation of the said table %s", e)
    finally:
        connection.close()

def barcode_generator()
