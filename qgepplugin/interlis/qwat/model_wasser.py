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
    __table_args__ = {"schema": SCHEMA}


class sia405_baseclass(baseclass):
    __tablename__ = "sia405_baseclass"
    __table_args__ = {"schema": SCHEMA}


class hydraulischer_knoten(sia405_baseclass):  # noeud_hydraulique
    __tablename__ = "hydraulischer_knoten"
    __table_args__ = {"schema": SCHEMA}


class leitungsknoten(sia405_baseclass):  # neud_de_conduite
    __tablename__ = "leitungsknoten"
    __table_args__ = {"schema": SCHEMA}


class anlage(leitungsknoten):
    __tablename__ = "anlage"
    __table_args__ = {"schema": SCHEMA}


class hausanschluss(leitungsknoten):
    __tablename__ = "hausanschluss"
    __table_args__ = {"schema": SCHEMA}


class hydrant(leitungsknoten):  # hydrant
    __tablename__ = "hydrant"
    __table_args__ = {"schema": SCHEMA}


class wasserbehaelter(leitungsknoten):  # reservoir_d_eau
    __tablename__ = "wasserbehaelter"
    __table_args__ = {"schema": SCHEMA}


class foerderanlage(leitungsknoten):  # station_de_pompage
    __tablename__ = "foerderanlage"
    __table_args__ = {"schema": SCHEMA}


class wassergewinnungsanlage(leitungsknoten):
    __tablename__ = "wassergewinnungsanlage"
    __table_args__ = {"schema": SCHEMA}


class hydraulischer_strang(sia405_baseclass):  # troncon_hydraulique
    __tablename__ = "hydraulischer_strang"
    __table_args__ = {"schema": SCHEMA}


class leitung(sia405_baseclass):  # conduite
    __tablename__ = "leitung"
    __table_args__ = {"schema": SCHEMA}


_prepared = False
def get_wasser_model():
    global _prepared
    if not _prepared:
        utils.sqlalchemy.prepare_automap_base(Base, SCHEMA)
        _prepared = True
    return Base.classes
