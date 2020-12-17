import psycopg2
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship

from . import config


def setup_test_db():
    print("SETTING UP QGEP/QWAT DATABASE...")
    r = os.system("docker inspect -f '{{.State.Running}}' qgepqwat")
    if r == 0:
        print("Already running")
        return

    os.system(f'docker run -d --rm -p 5432:5432 --name qgepqwat -e POSTGRES_PASSWORD={config.PGPASS} -e POSTGRES_DB={config.PGDATABASE} postgis/postgis')
    os.system('docker exec qgepqwat apt-get update')
    os.system('docker exec qgepqwat apt-get install -y wget')

    os.system('docker exec qgepqwat wget https://github.com/QGEP/datamodel/releases/download/1.5.3/qgep_1.5.3_structure_and_demo_data.backup')
    os.system(f'docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qgep_1.5.3_structure_and_demo_data.backup')

    os.system('docker exec qgepqwat wget https://github.com/qwat/qwat-data-model/releases/download/1.3.4/qwat_v1.3.4_data_and_structure_sample.backup')
    os.system(f'docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qwat_v1.3.4_data_and_structure_sample.backup')


def create_ili_schema(schema, model, smart=True):
    print("CONNECTING TO DATABASE...")
    connection = psycopg2.connect(f"host={config.PGHOST} dbname={config.PGDATABASE} user={config.PGUSER} password={config.PGPASS}")
    connection.set_session(autocommit=True)
    cursor = connection.cursor()

    cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';");

    if cursor.rowcount > 0:
        print("Already created")
        # TODO : truncate all
        return

    print("CREATING THE SCHEMA...")
    cursor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE ;")
    cursor.execute(f"CREATE SCHEMA {schema};")
    connection.commit()

    print("CREATE ILIDB...")
    smart_inheritance = '--smart2Inheritance' if smart else ''
    # TODO : remove --nameLang fr and retranslate everything to DE
    os.system(
        f"java -jar {config.ILI2PG} --schemaimport --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --setupPgExt --coalesceCatalogueRef --createEnumTabs --createNumChecks --coalesceMultiSurface --coalesceMultiLine --coalesceMultiPoint --coalesceArray --beautifyEnumDispName --createUnique --createGeomIdx --createFk --createFkIdx --expandMultilingual --createTypeConstraint --createTidCol --importTid {smart_inheritance} --strokeArcs --defaultSrsCode 2056 --trace --log C:/Users/Olivier/Desktop/debug.txt --nameLang fr {model}"
    )


def export_ili_schema(schema, model_name):

    print("EXPORT ILIDB...")
    os.system(f"java -jar {config.ILI2PG} --export --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --models {model_name} export_{model_name}.xtf")

    # java -jar C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\interlis\ili2pg-4.4.2\ili2pg-4.4.2.jar --export --dbhost 127.0.0.1 --dbusr postgres --dbpwd postgres --dbdatabase qgep_prod --dbschema pg2ili_abwasser --setupPgExt --coalesceCatalogueRef --createEnumTabs --createNumChecks --coalesceMultiSurface --coalesceMultiLine --coalesceMultiPoint --coalesceArray --beautifyEnumDispName --createUnique --createGeomIdx --createFk --createFkIdx --expandMultilingual --createTypeConstraint --createTidCol --importTid --smart2Inheritance --strokeArcs --defaultSrsCode 2056 --trace --log C:/Users/Olivier/Desktop/debug.txt --models SIA405_ABWASSER_2015 export.xtf

def create_engine():
    return sqlalchemy.create_engine(f'postgresql://{config.PGUSER}:{config.PGPASS}@{config.PGHOST}:5432/{config.PGDATABASE}')


def custom_name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation, avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    if constraint.name:
        return 'REF_'+constraint.name.lower()
    # if this didn't work, revert to the default behavior
    return 'REF_'+name_for_collection_relationship(base, local_cls, referred_cls, constraint)


classes = {}

# Helper that recursively creates hierarchical classes for sqlalchemy
def class_factory(name, bases, schema):
    print(f"Called class factory with args {name} {bases} {schema}")
    if name in classes:
        return classes[name]
    if len(bases) > 0:
        base = class_factory(bases[0], bases[1:], schema)
    else:
        base_name = f"{schema}_automapbase"
        if base_name not in classes:
            print(f"Created automap_base {base_name} for schema {schema}")
            classes[base_name] = automap_base()
        base = classes[base_name]
    class CLASS(base):
        __tablename__ = f"{schema}.{name}"
        __table_args__ = {'schema': schema}
    CLASS.__name__ = name
    # CLASS.__qualname__ = f"{schema}.{name}"
    print(f"Creating class {CLASS.__name__} / {CLASS.__qualname__} / {CLASS.__module__}")
    # classes[name] = CLASS
    return CLASS

def prepare(schema, engine):
    Base = classes[f"{schema}_automapbase"]
    Base.prepare(engine, reflect=True, schema=schema, name_for_collection_relationship=custom_name_for_collection_relationship)
    return Base

def capfirst(s):
    return s[0].upper()+s[1:]