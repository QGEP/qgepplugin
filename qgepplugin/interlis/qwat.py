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

from . import utils
from . import config

from .datamodels.qwat import Classes as QWAT
from .datamodels.wasser2015 import Classes as WASSER

###############################################
# Actual export (see qwat_generator to pregenerate some of this code)
###############################################

def export():

    session = Session(utils.create_engine())

    print("Exporting QWAT.pipe -> WASSER.conduite")
    for row in session.query(QWAT.pipe):
        # AVAILABLE FIELDS : id, fk_parent, fk_function, fk_installmethod, fk_material, fk_distributor, fk_precision, fk_bedding, fk_protection, fk_status, fk_watertype, fk_locationtype, fk_folder, year, year_rehabilitation, year_end, tunnel_or_bridge, pressure_nominal, remark, _valve_count, _valve_closed, label_1_visible, label_1_text, label_2_visible, label_2_text, fk_node_a, fk_node_b, fk_district, fk_pressurezone, fk_printmap, _length2d, _length3d, _diff_elevation, _printmaps, _geometry_alt1_used, _geometry_alt2_used, update_geometry_alt1, update_geometry_alt2,  geometry_alt1, geometry_alt2, schema_force_visible, _schema_visible
        session.add(
            WASSER.conduite(
                # t_id=None,
                # t_ili_tid=None,
                # nom_numero=None,
                geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
                # fonction=None,
                materiau=row.pipe_material.value_fr,
                # diametre_interieur=None,
                # diametre_exterieur=None,
                # diametre=None,
                # largeur_nominale=None,
                # qualite_eau=None,
                # determination_planimetrique=None,
                etat="?",
                annee_de_construction=max(1800, row.year or 0),
                # genre_de_raccordement=None,
                # isolation_exterieure=None,
                # isolation_interieure=None,
                # mode_de_pose=None,
                # assurance_contre_la_poussee=None,
                # couverture=None,
                # rehabilitation_renovation=None,
                # lit_de_pose=None,
                # protection_cathodique=None,
                zone_de_pression=row.pressurezone.name,
                # pression_de_fonctionnement_admissible=None,
                # pression_exploitation=None,
                # rugosite_hydraulique=None,
                longueur=row._length2d,
                # entretien=None,
                acondition=row.status.value_en,
                # proprietaire=None,
                # exploitant=None,
                # concessionnaire=None,
                # responsable_entretien=None,
                # remarque=None,
                # tronconref=None,
                # obj_id=None,
            )
        )
        print(".", end="")
    print("done")

    print("Exporting QWAT.hydrant -> WASSER.hydrant")
    for row in session.query(WASSER.hydrant):
        # AVAILABLE FIELDS : id, fk_provider, fk_model_sup, fk_model_inf, fk_material, fk_output, underground, marked, pressure_static, pressure_dynamic, flow, observation_date, observation_source
        session.add(
            WASSER.hydrant(
                # t_id=None,
                # t_ili_tid=None,
                # nom_numero=None,
                # genre=None,
                # materiau=None,
                # dimension=None,
                # fabricant=None,
                # pression_de_distribution=None,
                # pression_ecoulement=None,
                # soutirage=None,
                # atype=None,
                # acondition=None,
                # geometrie=None,
                # symboleori=None,
                # determination_planimetrique=None,
                # altitude=None,
                # determination_altimetrique=None,
                # annee_de_construction=None,
                # zone_de_pression=None,
                # proprietaire=None,
                # remarque=None,
                # noeudref=None,
                # obj_id=None,
            )
        )
        print(".", end="")
    print("done")

    print("Exporting QWAT.tank -> WASSER.reservoir_d_eau")
    for row in session.query(QWAT.tank):
        # AVAILABLE FIELDS : id, fk_overflow, fk_tank_firestorage, storage_total, storage_supply, storage_fire, altitude_overflow, altitude_apron, height_max, fire_valve, fire_remote, _litrepercm, cistern1_fk_type, cistern1_dimension_1, cistern1_dimension_2, cistern1_storage, _cistern1_litrepercm, cistern2_fk_type, cistern2_dimension_1, cistern2_dimension_2, cistern2_storage, _cistern2_litrepercm
        session.add(
            WASSER.reservoir_d_eau(
                # t_id=None,
                # t_ili_tid=None,
                # nom_numero=None,
                # genre=None,
                # materiau=None,
                # revetement=None,
                # hauteur_de_refoulement=None,
                # capacite_de_stockage=None,
                # reserve_eau_alimentation=None,
                # reserve_eau_incendie=None,
                # puissance=None,
                # acondition=None,
                # geometrie=None,
                # symboleori=None,
                # determination_planimetrique=None,
                # altitude=None,
                # determination_altimetrique=None,
                # annee_de_construction=None,
                # zone_de_pression=None,
                # proprietaire=None,
                # remarque=None,
                # noeudref=None,
                # obj_id=None,
            )
        )
        print(".", end="")
    print("done")

    session.commit()

    # EXPORT TEMPORARY SCHEMA
    utils.export_ili_schema(config.QWAT_ILI_SCHEMA, config.QWAT_ILI_MODEL_NAME)
