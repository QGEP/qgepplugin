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

# utils.setup_test_db()

# CREATE TEMPORARY SCHEMA
# utils.create_ili_schema(config.QWAT_ILI_SCHEMA, config.QWAT_ILI_MODEL)

engine = utils.create_engine()

###############################################
# QWAT datamodel
###############################################

QWATPipe = utils.class_factory("pipe", [], config.QWAT_SCHEMA)
QWATHydrant = utils.class_factory("hydrant", [], config.QWAT_SCHEMA)
QWATTank = utils.class_factory("tank", [], config.QWAT_SCHEMA)
QWAT = utils.prepare(config.QWAT_SCHEMA, engine)

###############################################
# INTERLIS datamodel
###############################################

SIALeitung = utils.class_factory("leitung", [], config.QWAT_ILI_SCHEMA)
SIAHydrant = utils.class_factory("hydrant", [], config.QWAT_ILI_SCHEMA)
SIAWasserbehaelter = utils.class_factory("wasserbehaelter", [], config.QWAT_ILI_SCHEMA)
SIA = utils.prepare(config.QWAT_ILI_SCHEMA, engine)
