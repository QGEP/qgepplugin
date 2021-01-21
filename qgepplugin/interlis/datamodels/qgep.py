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



class organisation(Base):
    __tablename__ = "organisation"
    __table_args__ = {'schema': SCHEMA}

class wastewater_structure(Base):
    __tablename__ = "wastewater_structure"
    __table_args__ = {'schema': SCHEMA}

class channel(wastewater_structure):
    __tablename__ = "channel"
    __table_args__ = {'schema': SCHEMA}

class manhole(wastewater_structure):
    __tablename__ = "manhole"
    __table_args__ = {'schema': SCHEMA}

class discharge_point(wastewater_structure):
    __tablename__ = "discharge_point"
    __table_args__ = {'schema': SCHEMA}

class special_structure(wastewater_structure):
    __tablename__ = "special_structure"
    __table_args__ = {'schema': SCHEMA}

class infiltration_installation(wastewater_structure):
    __tablename__ = "infiltration_installation"
    __table_args__ = {'schema': SCHEMA}

class pipe_profile(Base):
    __tablename__ = "pipe_profile"
    __table_args__ = {'schema': SCHEMA}

class wastewater_networkelement(Base):
    __tablename__ = "wastewater_networkelement"
    __table_args__ = {'schema': SCHEMA}

class reach_point(Base):
    __tablename__ = "reach_point"
    __table_args__ = {'schema': SCHEMA}

class wastewater_node(wastewater_networkelement):
    __tablename__ = "wastewater_node"
    __table_args__ = {'schema': SCHEMA}

class reach(wastewater_networkelement):
    __tablename__ = "reach"
    __table_args__ = {'schema': SCHEMA}

class structure_part(Base):
    __tablename__ = "structure_part"
    __table_args__ = {'schema': SCHEMA}

class dryweather_downspout(Base):
    __tablename__ = "dryweather_downspout"
    __table_args__ = {'schema': SCHEMA}

class access_aid(Base):
    __tablename__ = "access_aid"
    __table_args__ = {'schema': SCHEMA}

class dryweather_flume(Base):
    __tablename__ = "dryweather_flume"
    __table_args__ = {'schema': SCHEMA}

class cover(Base):
    __tablename__ = "cover"
    __table_args__ = {'schema': SCHEMA}

class benching(Base):
    __tablename__ = "benching"
    __table_args__ = {'schema': SCHEMA}


Base.prepare(
    utils.create_engine(),
    reflect=True,
    schema=SCHEMA,
    name_for_collection_relationship=utils.custom_name_for_collection_relationship,
    name_for_scalar_relationship=utils.custom_name_for_scalar_relationship,
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
