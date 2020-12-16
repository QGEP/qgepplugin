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

template_path = os.path.join(os.path.dirname(__file__) , 'qwat.py.tpl')
template = open(template_path, 'w')
generator_path = os.path.join(os.path.dirname(__file__) , 'qwat_generator.py.tpl')
generator = open(generator_path, 'w')

###############################################
# Code generation
###############################################

TABLE_MAPPING = {
    QWATpipe: SIAleitung,
    QWAThydrant: SIAhydrant,
    QWATtank: SIAwasserbehaelter,
}


for qwat_class, sia_class in TABLE_MAPPING.items():
    available_fields = ', '.join(f.name for f in qwat_class.__table__.columns)
    template.write(f'print("Exporting {qwat_class.__name__} -> {sia_class.__name__}")\n')
    template.write(f'for row in session.query(QWAT{qwat_class.__name__}):\n')
    template.write(f'    # AVAILABLE FIELDS : {available_fields}\n')
    template.write(f'    session.add(\n')
    template.write(f'        SIA{sia_class.__name__}(\n')
    for sia_field in sia_class.__table__.columns:
        template.write(f'            # {sia_field.name}=None,\n')
    template.write(f'        )\n')
    template.write(f'    )\n')
    template.write(f'    print(".", end="")\n')
    template.write(f'print("done")\n\n')


print("\n"*5)
available_tables = ', '.join([f"SIA{c.__name__}" for c in SIA.classes if c not in TABLE_MAPPING.values()])
generator.write('TABLE_MAPPING = {\n')
for qwat_class, sia_class in TABLE_MAPPING.items():
    generator.write(f"    QWAT{qwat_class.__name__.lower()}: SIA{sia_class.__name__.lower()},\n")
generator.write(f'    # NOT MAPPED YET\n')
generator.write(f'    # AVAILABLE CLASSES : {available_tables}\n')
for qwat_class in QWAT.classes:
    if qwat_class not in TABLE_MAPPING.keys():
        generator.write(f"    # QWAT{qwat_class.__name__}: REPLACE_ME,\n")
generator.write('}\n\n')
