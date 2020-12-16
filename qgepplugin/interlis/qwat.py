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
# Actual export (see qwat_generator to pregenerate some of this code)
###############################################

session = Session(engine)

print("Exporting Pipe -> Leitung")
for row in session.query(QWATPipe):
    # AVAILABLE FIELDS : id, fk_parent, fk_function, fk_installmethod, fk_material, fk_distributor, fk_precision, fk_bedding, fk_protection, fk_status, fk_watertype, fk_locationtype, fk_folder, year, year_rehabilitation, year_end, tunnel_or_bridge, pressure_nominal, remark, _valve_count, _valve_closed, label_1_visible, label_1_text, label_2_visible, label_2_text, fk_node_a, fk_node_b, fk_district, fk_pressurezone, fk_printmap, _length2d, _length3d, _diff_elevation, _printmaps, _geometry_alt1_used, _geometry_alt2_used, update_geometry_alt1, update_geometry_alt2, geometry, geometry_alt1, geometry_alt2, schema_force_visible, _schema_visible
    session.add(
        SIALeitung(
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            material=row.pipe_material.value_fr,
            baujahr=max(1800, row.year or 0),
            astatus=row.status.value_en,
            druckzone=row.pressurezone.name,
            laenge=row._length2d,
            zustand='?',
            # t_id=None,
            # t_ili_tid=None,
            # name_nummer=None,
            # funktion=None,
            # durchmesserinnen=None,
            # durchmesseraussen=None,
            # durchmesser=None,
            # nennweite=None,
            # wasserqualitaet=None,
            # lagebestimmung=None,
            # verbindungsart=None,
            # aussenbeschichtung=None,
            # innenbeschichtung=None,
            # verlegeart=None,
            # schubsicherung=None,
            # ueberdeckung=None,
            # sanierung_erneuerung=None,
            # bettung=None,
            # kathodischer_schutz=None,
            # zulaessiger_bauteil_betriebsdruck=None,
            # betriebsdruck=None,
            # hydraulische_rauheit=None,
            # unterhalt=None,
            # eigentuemer=None,
            # betreiber=None,
            # konzessionaer=None,
            # unterhaltspflichtiger=None,
            # bemerkung=None,
            # strangref=None,
            # obj_id=None,
        )
    )
    print(".", end="")
print("done")

print("Exporting Hydrant -> Hydrant")
for row in session.query(QWATHydrant):
    # AVAILABLE FIELDS : id, fk_provider, fk_model_sup, fk_model_inf, fk_material, fk_output, underground, marked, pressure_static, pressure_dynamic, flow, observation_date, observation_source
    session.add(
        SIAHydrant(
            # t_id
            # t_ili_tid
            # name_nummer
            # art
            # material
            # dimension
            # hersteller
            # versorgungsdruck
            # fliessdruck
            # entnahme
            # typ
            # zustand
            # geometrie
            # symbolori
            # lagebestimmung
            # hoehe
            # hoehenbestimmung
            # einbaujahr
            # druckzone
            # eigentuemer
            # bemerkung
            # knotenref
            # obj_id
        )
    )
    print(".", end="")
print("done")

print("Exporting Tank -> Wasserbehaelter")
for row in session.query(QWATTank):
    # AVAILABLE FIELDS : id, fk_overflow, fk_tank_firestorage, storage_total, storage_supply, storage_fire, altitude_overflow, altitude_apron, height_max, fire_valve, fire_remote, _litrepercm, cistern1_fk_type, cistern1_dimension_1, cistern1_dimension_2, cistern1_storage, _cistern1_litrepercm, cistern2_fk_type, cistern2_dimension_1, cistern2_dimension_2, cistern2_storage, _cistern2_litrepercm
    session.add(
        SIAWasserbehaelter(
            # t_id=None,
            # t_ili_tid=None,
            # name_nummer=None,
            # art=None,
            # material=None,
            # beschichtung=None,
            # ueberlaufhoehe=None,
            # fassungsvermoegen=None,
            # brauchwasserreserve=None,
            # loeschwasserreserve=None,
            # leistung=None,
            # zustand=None,
            # geometrie=None,
            # symbolori=None,
            # lagebestimmung=None,
            # hoehe=None,
            # hoehenbestimmung=None,
            # einbaujahr=None,
            # druckzone=None,
            # eigentuemer=None,
            # bemerkung=None,
            # knotenref=None,
            # obj_id=None,
        )
    )
    print(".", end="")
print("done")





session.commit()

# EXPORT TEMPORARY SCHEMA
utils.export_ili_schema(config.QWAT_ILI_SCHEMA, config.QWAT_ILI_MODEL_NAME)
