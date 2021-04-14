import psycopg2
import os
import datetime
import tempfile
import collections

from sqlalchemy.ext.automap import AutomapBase

from .. import config
from .various import logger, exec_, get_pgconf


def _log_path(name):
    now = datetime.datetime.now()
    return os.path.join(tempfile.gettempdir(), f"ili2qgepqwat-{now:%Y-%m-%d-%H-%M-%S}-{name}.log")


def create_ili_schema(schema, model, recreate_schema=False):
    logger.info("CONNECTING TO DATABASE...")

    pgconf = get_pgconf()

    connection = psycopg2.connect(
        f"host={pgconf['host']} port={pgconf['port']} dbname={pgconf['dbname']} user={pgconf['user']} password={pgconf['password']}"
    )
    connection.set_session(autocommit=True)
    cursor = connection.cursor()

    if not recreate_schema:
        # If the schema already exists, we just truncate all tables
        cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';")
        if cursor.rowcount > 0:
            logger.info(f"Schema {schema} already exists, we truncate instead")
            cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';")
            for row in cursor.fetchall():
                cursor.execute(f"TRUNCATE TABLE {schema}.{row[0]} CASCADE;")
            return

    logger.info(f"DROPPING THE SCHEMA {schema}...")
    cursor.execute(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE ;')
    logger.info(f"CREATING THE SCHEMA {schema}...")
    cursor.execute(f'CREATE SCHEMA "{schema}";')
    connection.commit()
    connection.close()

    logger.info(f"ILIDB SCHEMAIMPORT INTO {schema}...")
    pgconf = get_pgconf()
    exec_(f'"{config.JAVA}" -jar {config.ILI2PG} --schemaimport --dbhost {pgconf["host"]} --dbport {pgconf["port"]} --dbusr {pgconf["user"]} --dbpwd {pgconf["password"]} --dbdatabase {pgconf["dbname"]} --dbschema {schema} --setupPgExt --createGeomIdx --createFk --createFkIdx --createTidCol --importTid --noSmartMapping --defaultSrsCode 2056 --log {_log_path("create")} --nameLang de {model}')


def validate_xtf_data(xtf_file):
    logger.info("VALIDATING XTF DATA...")
    exec_(f'"{config.JAVA}" -jar {config.ILIVALIDATOR} --modeldir {config.ILI_FOLDER} {xtf_file}')


def import_xtf_data(schema, xtf_file):
    logger.info("IMPORTING XTF DATA...")
    pgconf = get_pgconf()
    exec_(
        f'"{config.JAVA}" -jar {config.ILI2PG} --import --deleteData --dbhost {pgconf["host"]} --dbport {pgconf["port"]} --dbusr {pgconf["user"]} --dbpwd {pgconf["password"]} --dbdatabase {pgconf["dbname"]} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --skipReferenceErrors --createTidCol --noSmartMapping --defaultSrsCode 2056 --log {_log_path("import")} {xtf_file}'
    )


def export_xtf_data(schema, model_name, xtf_file):
    logger.info("EXPORT ILIDB...")
    pgconf = get_pgconf()
    exec_(
        f'"{config.JAVA}" -jar {config.ILI2PG} --export --models {model_name} --dbhost {pgconf["host"]} --dbport {pgconf["port"]} --dbusr {pgconf["user"]} --dbpwd {pgconf["password"]} --dbdatabase {pgconf["dbname"]} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --skipReferenceErrors --createTidCol --noSmartMapping --defaultSrsCode 2056 --log {_log_path("export")} --trace {xtf_file}'
    )


class TidMaker:
    """
    Helper class that creates globally unique integer primary key forili2pg class (t_id)
    from a a QGEP/QWAT id (obj_id or id).
    """

    def __init__(self, id_attribute="id"):
        self._id_attr = id_attribute
        self._autoincrementer = collections.defaultdict(lambda: len(self._autoincrementer))

    def tid_for_row(self, row, for_class=None):
        # tid are globally unique, while ids are only guaranteed unique per table,
        # so include the base table in the key
        # this finds the base class (the first parent class before sqlalchemy.ext.automap.Base)
        class_for_id = row.__class__.__mro__[row.__class__.__mro__.index(AutomapBase) - 2]
        key = (class_for_id, getattr(row, self._id_attr), for_class)
        # was_created = key not in self._autoincrementer  # just for debugging
        tid = self._autoincrementer[key]
        # if was_created:
        #     # just for debugging
        #     logger.info(f"created tid {tid} for {key}")
        return tid
