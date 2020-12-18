import psycopg2
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship

from . import config


def make_file():
    print("CONNECTING TO DATABASE...")
    connection = psycopg2.connect(f"host={config.PGHOST} dbname={config.PGDATABASE} user={config.PGUSER} password={config.PGPASS}")
    connection.set_session(autocommit=True)
    cursor = connection.cursor()

    for schema in [config.QGEP_SCHEMA, config.QWAT_SCHEMA, config.WASSER_SCHEMA, config.ABWASSER_SCHEMA]:
        matchmaker_file_path = os.path.join(os.path.dirname(__file__), f'match_maker_{schema}.txt')
        matchmaker_file = open(matchmaker_file_path, 'w', newline='\n')
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' ORDER BY table_name;")
        for row_table in cursor.fetchall():
            table_name = row_table[0]
            matchmaker_file.write(f"--- TABLE {schema}.{table_name} ---\n")
            cursor.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{table_name}' ORDER BY ordinal_position;")
            for row_column in cursor.fetchall():
                column_name = row_column[0]
                data_type = row_column[1]
                is_nullable = '* ' if row_column[2]=='NO' else ''
                matchmaker_file.write(f"{column_name} ({is_nullable}{data_type})\n")
            matchmaker_file.write("\n")
        matchmaker_file.close()
