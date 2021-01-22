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

from .. import utils
from .. import config


SCHEMA = config.ABWASSER_SCHEMA

Base = automap_base()

class baseclass(Base):
    __tablename__ = "baseclass"
    __table_args__ = {'schema': SCHEMA}

class sia405_baseclass(baseclass):
    __tablename__ = "sia405_baseclass"
    __table_args__ = {'schema': SCHEMA}

class organisation(Base):
    __tablename__ = "organisation"
    __table_args__ = {'schema': SCHEMA}

class abwasserbauwerk(sia405_baseclass):
    __tablename__ = "abwasserbauwerk"
    __table_args__ = {'schema': SCHEMA}

class kanal(abwasserbauwerk):
    __tablename__ = "kanal"
    __table_args__ = {'schema': SCHEMA}

class normschacht(abwasserbauwerk):
    __tablename__ = "normschacht"
    __table_args__ = {'schema': SCHEMA}

class einleitstelle(abwasserbauwerk):
    __tablename__ = "einleitstelle"
    __table_args__ = {'schema': SCHEMA}

class spezialbauwerk(abwasserbauwerk):
    __tablename__ = "spezialbauwerk"
    __table_args__ = {'schema': SCHEMA}

class versickerungsanlage(abwasserbauwerk):
    __tablename__ = "versickerungsanlage"
    __table_args__ = {'schema': SCHEMA}

class rohrprofil(sia405_baseclass):
    __tablename__ = "rohrprofil"
    __table_args__ = {'schema': SCHEMA}

class abwassernetzelement(sia405_baseclass):
    __tablename__ = "abwassernetzelement"
    __table_args__ = {'schema': SCHEMA}

class haltungspunkt(sia405_baseclass):
    __tablename__ = "haltungspunkt"
    __table_args__ = {'schema': SCHEMA}

class abwasserknoten(abwassernetzelement):
    __tablename__ = "abwasserknoten"
    __table_args__ = {'schema': SCHEMA}

class haltung(abwassernetzelement):
    __tablename__ = "haltung"
    __table_args__ = {'schema': SCHEMA}

class bauwerksteil(sia405_baseclass):
    __tablename__ = "bauwerksteil"
    __table_args__ = {'schema': SCHEMA}

class trockenwetterfallrohr(bauwerksteil):
    __tablename__ = "trockenwetterfallrohr"
    __table_args__ = {'schema': SCHEMA}

class einstiegshilfe(bauwerksteil):
    __tablename__ = "einstiegshilfe"
    __table_args__ = {'schema': SCHEMA}

class trockenwetterrinne(bauwerksteil):
    __tablename__ = "trockenwetterrinne"
    __table_args__ = {'schema': SCHEMA}

class deckel(bauwerksteil):
    __tablename__ = "deckel"
    __table_args__ = {'schema': SCHEMA}

class bankett(bauwerksteil):
    __tablename__ = "bankett"
    __table_args__ = {'schema': SCHEMA}

class metaattribute(Base):
    __tablename__ = "metaattribute"
    __table_args__ = {'schema': SCHEMA}

Base.prepare(
    utils.create_engine(),
    reflect=True,
    schema=SCHEMA,
    name_for_collection_relationship=utils.custom_name_for_collection_relationship,
    name_for_scalar_relationship=utils.custom_name_for_scalar_relationship,
    generate_relationship=utils.custom_generate_relationship,
)

Classes = Base.classes

# For some reason, automap_base doesn't add manually defined classes to Base.classes,
# so we do it manually here
def add_subclasses(Parent):
    for subclass in Parent.__subclasses__():
        if subclass.__name__ not in Classes:
            Classes[subclass.__name__] = subclass
        add_subclasses(subclass)
add_subclasses(Base)

