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


SCHEMA = config.WASSER_SCHEMA

Base = automap_base()

class baseclass(Base):
    __tablename__ = "baseclass"
    __table_args__ = {'schema': SCHEMA}

class sia405_baseclass(baseclass):
    __tablename__ = "sia405_baseclass"
    __table_args__ = {'schema': SCHEMA}

class noeud_hydraulique(sia405_baseclass):
    __tablename__ = "noeud_hydraulique"
    __table_args__ = {'schema': SCHEMA}

class noeud_de_conduite(sia405_baseclass):
    __tablename__ = "noeud_de_conduite"
    __table_args__ = {'schema': SCHEMA}

class hydrant(noeud_de_conduite):
    __tablename__ = "hydrant"
    __table_args__ = {'schema': SCHEMA}

class reservoir_d_eau(noeud_de_conduite):
    __tablename__ = "reservoir_d_eau"
    __table_args__ = {'schema': SCHEMA}

class station_de_pompage(noeud_de_conduite):
    __tablename__ = "station_de_pompage"
    __table_args__ = {'schema': SCHEMA}

class troncon_hydraulique(sia405_baseclass):
    __tablename__ = "troncon_hydraulique"
    __table_args__ = {'schema': SCHEMA}

class conduite(sia405_baseclass):
    __tablename__ = "conduite"
    __table_args__ = {'schema': SCHEMA}

Base.prepare(utils.create_engine(), reflect=True, schema=SCHEMA, name_for_collection_relationship=utils.custom_name_for_collection_relationship)

Classes = Base.classes

# For some reason, automap_base doesn't add manually defined classes to Base.classes,
# so we do it manually here
def add_subclasses(Parent):
    for subclass in Parent.__subclasses__():
        if subclass.__name__ not in Classes:
            Classes[subclass.__name__] = subclass
        add_subclasses(subclass)
add_subclasses(Base)

