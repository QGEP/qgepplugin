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

class abwasserbauwerk(Base):
    __tablename__ = "abwasserbauwerk"
    __table_args__ = {'schema': SCHEMA}

class normschacht(abwasserbauwerk):
    __tablename__ = "normschacht"
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

