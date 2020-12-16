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

# from .qwat_datamodel import *
from qwat_datamodel import *


###############################################
# Code generation
###############################################

TABLE_MAPPING = {
    QWATPipe: SIALeitung,
    QWATHydrant: SIAHydrant,
    QWATTank: SIAWasserbehaelter,
}

template_path = os.path.join(os.path.dirname(__file__) , 'qwat.tpl.py')

with open(template_path, 'w') as fh:
    for qwat_class, sia_class in TABLE_MAPPING.items():
        available_fields = ', '.join(f.name for f in qwat_class.__table__.columns)
        fh.write(f'print("Exporting {qwat_class.__name__} -> {sia_class.__name__}")\n')
        fh.write(f'for row in session.query(QWAT{qwat_class.__name__.title()}):\n')
        fh.write(f'    # AVAILABLE FIELDS : {available_fields}\n')
        fh.write(f'    session.add(\n')
        fh.write(f'        SIA{sia_class.__name__.title()}(\n')        
        for sia_field in sia_class.__table__.columns:
            fh.write(f'            # {sia_field.name}=None,\n')
        fh.write(f'        )\n')
        fh.write(f'    )\n')
        fh.write(f'    print(".", end="")\n')
        fh.write(f'print("done")\n\n')

for qwat_class in QWAT.classes:
    if qwat_class not in TABLE_MAPPING.keys():
        print(f"⚠️ QWAT table '{qwat_class.__name__}' is not mapped.")

for sia_class in SIA.classes:
    if sia_class not in TABLE_MAPPING.values():
        print(f"⚠️ SIA table '{sia_class.__name__}' is not mapped.")