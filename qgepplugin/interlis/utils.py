import psycopg2
import os
import subprocess

import sqlalchemy
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship, name_for_scalar_relationship, generate_relationship

from . import config


def exec_(command, check=True):
    print("")
    print("!"*80)
    print(f"EXECUTING: {command}")
    if check:
        return subprocess.check_call(command)
    else:
        return subprocess.call(command)


def setup_test_db():

    print("SETTING UP QGEP/QWAT DATABASE...")
    r = exec_("docker inspect -f '{{.State.Running}}' qgepqwat", check=False)
    if r == 0:
        print("Already running")
        return


    exec_(f'docker run -d --rm -p 5432:5432 --name qgepqwat -e POSTGRES_PASSWORD={config.PGPASS} -e POSTGRES_DB={config.PGDATABASE} postgis/postgis')
    exec_('docker exec qgepqwat apt-get update')
    exec_('docker exec qgepqwat apt-get install -y wget')

    exec_('docker exec qgepqwat wget https://github.com/QGEP/datamodel/releases/download/1.5.3/qgep_1.5.3_structure_and_demo_data.backup')
    exec_(f'docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qgep_1.5.3_structure_and_demo_data.backup')

    exec_('docker exec qgepqwat wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_data_and_structure_sample.backup')
    exec_(f'docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qwat_v1.3.5_data_and_structure_sample.backup')

    # add our QWAT migrations
    exec_(r'docker cp C:\Users\Olivier\Code\QWAT\data-model\update\delta\delta_1.3.6_add_vl_for_SIA_export.sql qgepqwat:/delta_1.3.6_add_vl_for_SIA_export.sql')
    exec_(f'docker exec qgepqwat psql -U postgres -d qgep_prod -f /delta_1.3.6_add_vl_for_SIA_export.sql')


def create_ili_schema(schema, model):
    print("CONNECTING TO DATABASE...")
    connection = psycopg2.connect(f"host={config.PGHOST} dbname={config.PGDATABASE} user={config.PGUSER} password={config.PGPASS}")
    connection.set_session(autocommit=True)
    cursor = connection.cursor()

    # cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';");

    # if cursor.rowcount > 0:
    #     print("Already created, we truncate instead")
    #     cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';")
    #     for row in cursor.fetchall():
    #         cursor.execute(f"TRUNCATE TABLE {schema}.{row[0]} CASCADE;")
    #     return

    print("CREATING THE SCHEMA...")
    cursor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE ;")
    cursor.execute(f"CREATE SCHEMA {schema};")
    connection.commit()

    print("CREATE ILIDB...")
    # if "_f-" in model:
    #     lang = f'fr'
    # else:
    #     lang = f'de'
    lang = f'de'

    exec_(
        f"java -jar {config.ILI2PG} --schemaimport --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --setupPgExt --createGeomIdx --createFk --createFkIdx --createTidCol --importTid --noSmartMapping --defaultSrsCode 2056 --strokeArcs --log debug-create.txt --nameLang {lang} {model}"
    )


def import_xtf_data(schema, xtf_file):
    print("IMPORTING XTF DATA...")
    exec_(
        f"java -jar {config.ILI2PG} --import --deleteData --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --createTidCol --defaultSrsCode 2056 --log debug-import.txt {xtf_file}"
    )


def export_xtf_data(schema, model_name):

    print("EXPORT ILIDB...")

    exec_(
        f"java -jar {config.ILI2PG} --export --models {model_name} --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --createTidCol --defaultSrsCode 2056 --log debug-export.txt export_{model_name}.xtf"
    )


def create_engine():
    return sqlalchemy.create_engine(f'postgresql://{config.PGUSER}:{config.PGPASS}@{config.PGHOST}:5432/{config.PGDATABASE}')


def custom_name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation, avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    if constraint.name:
        return 'BWREL_'+constraint.name.lower()
    # if this didn't work, revert to the default behavior
    return 'BWREL_'+name_for_collection_relationship(base, local_cls, referred_cls, constraint)

def custom_name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation, avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    if len(constraint.columns) == 1:
        return constraint.columns.keys()[0] + "_REL"
    if constraint.name:
        return 'REL_'+constraint.name.lower()
    # if this didn't work, revert to the default behavior
    return 'REL_'+name_for_scalar_relationship(base, local_cls, referred_cls, constraint)

def custom_generate_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    # This skips backrefs
    if return_fn is sqlalchemy.orm.backref:
        return None
    return generate_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw)

def capfirst(s):
    return s[0].upper()+s[1:]