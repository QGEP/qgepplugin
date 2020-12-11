import psycopg2
import os
import sys
import collections

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from geoalchemy2 import Geometry

PGHOST = '127.0.0.1'
PGDATABASE = 'qgep_prod'
PGUSER = 'postgres'
PGPASS = 'postgres'
PSQL = r'C:\OSGeo4W64\bin\psql'
QGEP_ILI_MODEL = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\vsa_kek_sia_405\sia405_interlis_files\SIA405_Abwasser_2015_2_d-20180417.ili'
QWAT_ILI_MODEL = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\vsa_kek_sia_405\sia405_interlis_files\SIA405_Wasser_2015_2_d-20181005.ili'
ILI2PG = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\vsa_kek_sia_405\ili2pg-4.4.2\ili2pg-4.4.2.jar'
QGEP_ILI_SCHEMA = 'pg2ili_abwasser'
QWAT_ILI_SCHEMA = 'pg2ili_wasser'
QGEP_SCHEMA = 'qgep_od'

"""
print("SETTING UP QGEP/QWAT DATABASE...")
os.system('docker run -d --rm -p 5432:5432 --name qgep opengisch/qgep_datamodel')
os.system('docker exec qgep init_qgep.sh wait')
os.system('docker exec qgep wget https://github.com/qwat/qwat-data-model/releases/download/1.3.4/qwat_v1.3.4_data_and_structure_sample.backup')
os.system('docker exec qgep pg_restore -U postgres --dbname qgep_prod --verbose --no-privileges --exit-on-error qwat_v1.3.4_data_and_structure_sample.backup')

print("CONNECTING TO DATABASE...")
connection = psycopg2.connect(f"host={PGHOST} dbname={PGDATABASE} user={PGUSER} password={PGPASS}")
connection.set_session(autocommit=True)
cursor = connection.cursor()

print("CREATING THE SCHEMA...")
for schema in [QGEP_ILI_SCHEMA, QWAT_ILI_SCHEMA]:
    cursor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE ;")
    cursor.execute(f"CREATE SCHEMA {schema};")
connection.commit()

print("CREATE ILIDB...")
for schema, model in [(QGEP_ILI_SCHEMA, QGEP_ILI_MODEL), (QWAT_ILI_SCHEMA, QWAT_ILI_MODEL)]:
    os.system(f"java -jar {ILI2PG} --schemaimport --dbhost {PGHOST} --dbusr {PGUSER} --dbpwd {PGPASS} --dbdatabase {PGDATABASE} --dbschema {schema} --setupPgExt --coalesceCatalogueRef --createEnumTabs --createNumChecks --coalesceMultiSurface --coalesceMultiLine --coalesceMultiPoint --coalesceArray --beautifyEnumDispName --createUnique --createGeomIdx --createFk --createFkIdx --expandMultilingual --createTypeConstraint --createTidCol --importTid --noSmartMapping --strokeArcs --defaultSrsCode 2056 --trace --log C:/Users/Olivier/Desktop/debug.txt {model}")
"""

print("EXPORTING")

MAPPING = {
    'wastewater_structure': {
        'accessibility': {
            None: None,
            3444: 'ueberdeckt',
            3447: 'unbekannt',
            3446: 'unzugaenglich',
            3445: 'zugaenglich',
        }
    },
    'manhole': {
        'function': {
            None: None,
            4532: 'Absturzbauwerk',
            5344: 'andere',
            4533: 'Be_Entlueftung',
            3267: 'Dachwasserschacht',
            3266: 'Einlaufschacht',
            3472: 'Entwaesserungsrinne',
            228: 'Geleiseschacht',
            204: 'Kontrollschacht',
            1008: 'Oelabscheider',
            4536: 'Pumpwerk',
            5346: 'Regenueberlauf',
            2742: 'Schlammsammler',
            5347: 'Schwimmstoffabscheider',
            4537: 'Spuelschacht',
            4798: 'Trennbauwerk',
            5345: 'unbekannt',
        },
    },
}

engine = create_engine(f'postgresql://{PGUSER}:{PGPASS}@{PGHOST}:5432/{PGDATABASE}')

def custom_name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation, avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    if constraint.name:
        return 'REF_'+constraint.name.lower()
    # if this didn't work, revert to the default behavior
    return 'REF_'+name_for_collection_relationship(base, local_cls, referred_cls, constraint)

# Define QGEP datamodel
QGEPBase = automap_base()

class QGEPWastewaterStructure(QGEPBase):
    __tablename__ = 'wastewater_structure'
    __table_args__ = {'schema': QGEP_SCHEMA}

class QGEPManhole(QGEPWastewaterStructure):
    __tablename__ = 'manhole'
    __table_args__ = {'schema': QGEP_SCHEMA}

QGEPBase.prepare(engine, reflect=True, schema=QGEP_SCHEMA, name_for_collection_relationship=custom_name_for_collection_relationship)

# QGEP ILI MODELS

SIABase = automap_base()

class SIABaseClass(SIABase):
    __tablename__ = 'baseclass'
    __table_args__ = {'schema': QGEP_ILI_SCHEMA}

class SIASia405BaseClass(SIABaseClass):
    __tablename__ = 'sia405_baseclass'
    __table_args__ = {'schema': QGEP_ILI_SCHEMA}

class SIAAbwasserbauwerk(SIASia405BaseClass):
    __tablename__ = 'abwasserbauwerk'
    __table_args__ = {'schema': QGEP_ILI_SCHEMA}

class SIANormschacht(SIAAbwasserbauwerk):
    __tablename__ = 'normschacht'
    __table_args__ = {'schema': QGEP_ILI_SCHEMA}

SIABase.prepare(engine, reflect=True, schema=QGEP_ILI_SCHEMA, name_for_collection_relationship=custom_name_for_collection_relationship)

# Autoincrementing ID
oid2tid = collections.defaultdict(lambda: len(oid2tid))

# Actual insert routing
session = Session(engine, autocommit=True)

print("Exporting manhole -> normschacht")
for row in session.query(QGEPManhole):
    session.add(
        SIANormschacht(
            t_id=oid2tid[row.obj_id],
            t_type='normschacht',
            t_ili_tid=row.obj_id,
            obj_id=row.obj_id,
            zugaenglichkeit=MAPPING['wastewater_structure']['accessibility'][row.accessibility],
            dimension1=row.dimension1,
            dimension2=row.dimension2,
            funktion=MAPPING['manhole']['function'][row.function],
        )
    )
    print(".", end="")
print("done !")

session.commit()

