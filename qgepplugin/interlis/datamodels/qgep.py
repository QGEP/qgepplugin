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

###############################################
# QGEP datamodel
# All tables will be loaded from the QGEP schema as a SqlAlchemy ORM class.
# Only table specific relationships (e.g. inheritance) need to be manually
# defined here. Other attributes will be loaded automatically.
###############################################

Base = automap_base()

SCHEMA = config.QGEP_SCHEMA

# Helper to convert IDs to ili-compatible tids (autoincrementing)
_autoincrementer = collections.defaultdict(lambda: len(_autoincrementer))
def make_tid(cls, id):
    # if verbose:
    #     star = '*' if (cls, id) not in _autoincrementer else ''
    #     result = _autoincrementer[(cls, id)]
    #     print(f"{star}{cls.__name__}/{id}=>{result}   ", end="")
    #     return result
    return str(_autoincrementer[(cls, id)])

class wastewater_networkelement(Base):
    __tablename__ = "wastewater_networkelement"
    __table_args__ = {'schema': SCHEMA}

    @staticmethod
    def make_tid(id):
        return make_tid(wastewater_networkelement, id)

class wastewater_node(wastewater_networkelement):
    __tablename__ = "wastewater_node"
    __table_args__ = {'schema': SCHEMA}

class reach(wastewater_networkelement):
    __tablename__ = "reach"
    __table_args__ = {'schema': SCHEMA}

class wastewater_structure(Base):
    __tablename__ = "wastewater_structure"
    __table_args__ = {'schema': SCHEMA}

    @staticmethod
    def make_tid(id):
        return make_tid(wastewater_structure, id)

class manhole(wastewater_structure):
    __tablename__ = "manhole"
    __table_args__ = {'schema': SCHEMA}

class channel(wastewater_structure):
    __tablename__ = "channel"
    __table_args__ = {'schema': SCHEMA}

Base.prepare(
    utils.create_engine(),
    reflect=True,
    schema=SCHEMA,
    name_for_collection_relationship=utils.custom_name_for_collection_relationship
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
