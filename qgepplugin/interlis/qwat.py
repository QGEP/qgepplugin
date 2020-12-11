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
from geoalchemy2.functions import ST_Transform, ST_Force2D

# from . import utils
# from . import config
import utils
import config

utils.setup_test_db()

# CREATE TEMPORARY SCHEMA
utils.create_ili_schema(config.QWAT_ILI_SCHEMA, config.QWAT_ILI_MODEL)



engine = utils.create_engine()


###############################################
# QWAT datamodel
###############################################

QWATBase = automap_base()

class QWATPipe(QWATBase):
    __tablename__ = 'pipe'
    __table_args__ = {'schema': config.QWAT_SCHEMA}

QWATBase.prepare(engine, reflect=True, schema=config.QWAT_SCHEMA, name_for_collection_relationship=utils.custom_name_for_collection_relationship)

###############################################
# INTERLIS datamodel
###############################################

SIABase = automap_base()

class SIALeitung(SIABase):
    __tablename__ = 'leitung'
    __table_args__ = {'schema': config.QWAT_ILI_SCHEMA}

SIABase.prepare(engine, reflect=True, schema=config.QWAT_ILI_SCHEMA, name_for_collection_relationship=utils.custom_name_for_collection_relationship)


###############################################
# Actual export
###############################################

MAPPING = {
}

session = Session(engine)

print("Exporting pipe -> leitung")
for row in session.query(QWATPipe):
    session.add(
        SIALeitung(
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            material=row.pipe_material.value_fr,
            baujahr=max(1800, row.year or 0),
            astatus=row.status.value_en,
            druckzone=row.pressurezone.name,
            laenge=row._length2d,
            zustand='?',
        )
    )
    print(".", end="")
print("done !")

session.commit()

# EXPORT TEMPORARY SCHEMA
utils.export_ili_schema(config.QWAT_ILI_SCHEMA, config.QWAT_ILI_MODEL_NAME)
