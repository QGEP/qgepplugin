import psycopg2
import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker


PGHOST = '127.0.0.1'
PGDATABASE = 'qgep_prod'
PGUSER = 'postgres'
PGPASS = 'postgres'
PSQL = r'C:\OSGeo4W64\bin\psql'
ILI_MODEL = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\ili\SIA405_Abwasser_2015_2_d-20180417.ili'
ILI2PG = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\ili2pg-3.12.2\ili2pg-3.12.2.jar'
TEMP_SCHEMA = 'vsa_dss_2015_2_d'
SCRIPTS = [
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\01_vsa_dss_2015_2_d_tid_generate.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\02_vsa_dss_2015_2_d_tid_lookup.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\021_vsa_dss_2015_2_d_create_seq_ili2db.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\022_vsa_dss_2015_2_d_basket_update.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\046_vsa_dss_2015_2_d_t_key_object_insert_metadata.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\051_vsa_dss_2015_2_d_interlisexport2.sql',
    # r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\052a_vsa_dss_2015_2_d_interlisexport2.sql',
]

print("CONNECTING TO DATABASE...")
connection = psycopg2.connect(f"host={PGHOST} dbname={PGDATABASE} user={PGUSER} password={PGPASS}")
connection.set_session(autocommit=True)
cursor = connection.cursor()

print("CREATING THE SCHEMA...")
cursor.execute(f"DROP SCHEMA IF EXISTS {TEMP_SCHEMA} CASCADE ;")
cursor.execute(f"CREATE SCHEMA {TEMP_SCHEMA};")
connection.commit()

print("CREATE ILIDB...")
os.system(f"java -jar {ILI2PG} --createEnumTxtCol --schemaimport --importTid --sqlEnableNull --createEnumTabs --createFk  --noSmartMapping --dbdatabase {PGDATABASE} --dbschema {TEMP_SCHEMA} --dbusr {PGUSER} --dbpwd {PGPASS}  --log createschema_VSA_DSS_2015_2_d.log {ILI_MODEL}")


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

class QGEPWastewaterNetworkelement(QGEPBase):
    __tablename__ = 'wastewater_networkelement'
    __table_args__ = {'schema': 'qgep_od'}

class QGEPWastewaterStructure(QGEPBase):
    __tablename__ = 'wastewater_structure'
    __table_args__ = {'schema': 'qgep_od'}

class QGEPManhole(QGEPWastewaterStructure):
    __tablename__ = 'manhole'
    __table_args__ = {'schema': 'qgep_od'}

QGEPBase.prepare(engine, reflect=True, schema='qgep_od', name_for_collection_relationship=custom_name_for_collection_relationship)

# Define Interlis datamodel
SIABase = automap_base()

classes = {}

def class_factory(name, bases):
    if name in classes:
        return name    
    if len(bases) > 0:
        base = class_factory(bases[0], bases[1:])
    class CLASS(base):
        __tablename__ = name
        __table_args__ = {'schema': TEMP_SCHEMA}
    classes[name] = CLASS
    return CLASS


SIAAbwassernetzelement = class_factory("abwassernetzelement", ["sia405_baseclass", "baseclass"])
SIANormschacht = class_factory("normschacht", ["abwasserbauwerk", "sia405_baseclass", "baseclass"])

class SIABaseClass(SIABase):
    __tablename__ = 'baseclass'
    __table_args__ = {'schema': TEMP_SCHEMA}

class SIASia405BaseClass(SIABaseClass):
    __tablename__ = 'sia405_baseclass'
    __table_args__ = {'schema': TEMP_SCHEMA}

class SIAAbwassernetzelement(SIASia405BaseClass):
    __tablename__ = 'abwassernetzelement'
    __table_args__ = {'schema': TEMP_SCHEMA}

class SIAAbwasserbauwerk(SIASia405BaseClass):
    __tablename__ = 'abwasserbauwerk'
    __table_args__ = {'schema': TEMP_SCHEMA}

class SIANormschacht(SIAAbwasserbauwerk):
    __tablename__ = 'normschacht'
    __table_args__ = {'schema': TEMP_SCHEMA}

SIABase.prepare(engine, reflect=True, schema=TEMP_SCHEMA, name_for_collection_relationship=custom_name_for_collection_relationship)

# Autoincrementing ID
oid2tid = collections.defaultdict(lambda: len(oid2tid))

# Actual insert routing
session = Session(engine)

print("Exporting wastewaternetworkelement -> abwassernetzelement")
for row in session.query(QGEPWastewaterNetworkelement):
    session.add(
        SIAAbwassernetzelement(
            t_id=oid2tid[row.obj_id],
            t_type='abwassernetzelement',
            t_ili_tid=row.obj_id,
            obj_id=row.obj_id,
            bezeichnung=row.identifier,
        )
    )
    print(".", end="")
print("done !")

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

