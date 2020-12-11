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
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from geoalchemy2 import Geometry

# from . import utils
# from . import config
import utils
import config

utils.setup_test_db()

# CREATE TEMPORARY SCHEMA
utils.create_ili_schema(config.QGEP_ILI_SCHEMA, config.QGEP_ILI_MODEL)



engine = utils.create_engine()


###############################################
# QGEP datamodel
###############################################

QGEPBase = automap_base()

class QGEPWastewaterStructure(QGEPBase):
    __tablename__ = 'wastewater_structure'
    __table_args__ = {'schema': config.QGEP_SCHEMA}

class QGEPManhole(QGEPWastewaterStructure):
    __tablename__ = 'manhole'
    __table_args__ = {'schema': config.QGEP_SCHEMA}

QGEPBase.prepare(engine, reflect=True, schema=config.QGEP_SCHEMA, name_for_collection_relationship=utils.custom_name_for_collection_relationship)

###############################################
# INTERLIS datamodel
###############################################

SIABase = automap_base()

class SIANormschacht(SIABase):
    __tablename__ = 'normschacht'
    __table_args__ = {'schema': config.QGEP_ILI_SCHEMA}

SIABase.prepare(engine, reflect=True, schema=config.QGEP_ILI_SCHEMA, name_for_collection_relationship=utils.custom_name_for_collection_relationship)


###############################################
# Actual export
###############################################

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

session = Session(engine)

print("Exporting manhole -> normschacht")
for row in session.query(QGEPManhole):
    session.add(
        SIANormschacht(
            bezeichnung=row.identifier,
            t_ili_tid=row.obj_id,
            obj_id=row.obj_id,
            zugaenglichkeit=MAPPING['wastewater_structure']['accessibility'][row.accessibility],
            dimension1=min(4000, row.dimension1 or 0),
            dimension2=min(4000, row.dimension2 or 0),
            funktion=MAPPING['manhole']['function'][row.function],
        )
    )
    print(".", end="")
print("done !")

session.commit()

# EXPORT TEMPORARY SCHEMA
utils.export_ili_schema(config.QGEP_ILI_SCHEMA, config.QGEP_ILI_MODEL_NAME)
