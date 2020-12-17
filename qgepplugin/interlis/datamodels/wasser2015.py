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
# class conduite(Base):
#     __tablename__ = "conduite"
#     __table_args__ = {'schema': SCHEMA}
# class hydrant(Base):
#     __tablename__ = "hydrant"
#     __table_args__ = {'schema': SCHEMA}
# class reservoir_d_eau(Base):
#     __tablename__ = "reservoir_d_eau"
#     __table_args__ = {'schema': SCHEMA}
Base.prepare(utils.create_engine(), reflect=True, schema=SCHEMA, name_for_collection_relationship=utils.custom_name_for_collection_relationship)

Classes = Base.classes
