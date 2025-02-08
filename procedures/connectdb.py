import psycopg2, psycopg2.extras
from psycopg2.extensions import cursor, connection
from config import connection_credentials
import logging
from typing import Tuple

def connect() -> Tuple[cursor, connection]:
    db_cursor = None
    connection = None
    try :
        params = connection_credentials()
        logging.info("Connecting to PostgreSQL Database ...")
        connection = psycopg2.connect(**params)                 # Connecting to PostgreSQL

        db_cursor = connection.cursor()          # Creating a cursor
        return db_cursor, connection

    except(Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        return None, None