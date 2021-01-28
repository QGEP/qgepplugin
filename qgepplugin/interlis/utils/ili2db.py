import psycopg2
import os
import datetime
import tempfile
import collections

from sqlalchemy.ext.automap import AutomapBase

from .. import config
from .various import exec_


def _log_path(name):
    now = datetime.datetime.now()
    return os.path.join(tempfile.gettempdir(), f"ili2qgepqwat-{now:%Y-%m-%d-%H-%M-%S}-{name}.log")


def create_ili_schema(schema, model, recreate_schema=False):
    print("CONNECTING TO DATABASE...")
    connection = psycopg2.connect(
        f"host={config.PGHOST} dbname={config.PGDATABASE} user={config.PGUSER} password={config.PGPASS}"
    )
    connection.set_session(autocommit=True)
    cursor = connection.cursor()

    if not recreate_schema:
        # If the schema already exists, we just truncate all tables
        cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';")
        if cursor.rowcount > 0:
            print(f"Schema {schema} already exists, we truncate instead")
            cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';")
            for row in cursor.fetchall():
                cursor.execute(f"TRUNCATE TABLE {schema}.{row[0]} CASCADE;")
            return

    print(f"CREATING THE SCHEMA {schema}...")
    cursor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE ;")
    cursor.execute(f"CREATE SCHEMA {schema};")
    connection.commit()

    print(f"ILIDB SCHEMAIMPORT INTO {schema}...")
    # if "_f-" in model:
    #     lang = f'fr'
    # else:
    #     lang = f'de'
    lang = f"de"

    exec_(
        f'"{config.JAVA}" -jar {config.ILI2PG} --schemaimport --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --setupPgExt --createGeomIdx --createFk --createFkIdx --createTidCol --importTid --noSmartMapping --defaultSrsCode 2056 --strokeArcs --log {_log_path("create")} --nameLang {lang} {model}'
    )


def validate_xtf_data(xtf_file):
    print("VALIDATING XTF DATA...")
    exec_(f'"{config.JAVA}" -jar {config.ILIVALIDATOR} --modeldir {config.ILI_FOLDER} {xtf_file}')


def import_xtf_data(schema, xtf_file):
    print("IMPORTING XTF DATA...")
    exec_(
        f'"{config.JAVA}" -jar {config.ILI2PG} --import --deleteData --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --skipReferenceErrors --createTidCol --defaultSrsCode 2056 --log {_log_path("import")} {xtf_file}'
    )


def export_xtf_data(schema, model_name, xtf_file):

    print("EXPORT ILIDB...")

    exec_(
        f'"{config.JAVA}" -jar {config.ILI2PG} --export --models {model_name} --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --skipReferenceErrors --createTidCol --defaultSrsCode 2056 --log {_log_path("export")} {xtf_file}'
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
        return self._autoincrementer[key]
