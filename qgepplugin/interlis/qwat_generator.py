"""
This script is a code generator, helping to implement QWAT/QGEP -> ILI migrations scripts.

Setup is made in TABLE_MAPPING, where one QWAT/QGEP class can be matched to one or more ILI classes.

The script will generate corresponding code in `qwat.py.tpl`, which can then
be diffed/merged into the original `qwat.py` (recommending `Diff & Merge` extension in VSCode).

It will also generate `qwat_generator.py.tpl`, which can be diffed/merged into this file, 
to update the list of classes that have not been mapped yet.
"""

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
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy import create_engine

from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Transform, ST_Force2D

from . import utils
from . import config

from .datamodels.qwat import Classes as QWAT
from .datamodels.wasser2015 import Classes as WASSER

def generate():

    template_path = os.path.join(os.path.dirname(__file__), 'qwat.py.tpl')
    template = open(template_path, 'w', newline='\n')
    generator_path = os.path.join(os.path.dirname(__file__), 'qwat_generator.py.tpl')
    generator = open(generator_path, 'w', newline='\n')

    ###############################################
    # Code generation
    ###############################################

    TABLE_MAPPING = {
        QWAT.network_element: [WASSER.noeud_hydraulique],
        QWAT.hydrant: [WASSER.hydrant],
        QWAT.tank: [WASSER.reservoir_d_eau],
        QWAT.pipe: [WASSER.troncon_hydraulique, WASSER.conduite],
        # NOT MAPPED YET
        # AVAILABLE WASSER CLASSES : sia405_15_lv95sia405_eaux_cs_conduite_texteassoc, conduite_troncon_assoc, sia405_15_lv95sia405_eaux_cs_noeud_de_conduite_texteassoc, noeud_de_conduite_noeud_assoc, sia405_15_lv95sia405_eaux_cs_construction_speciale_textessoc, sia405_15_lv95sia405_eaux_cs_construction_speciale_surface, sia405_15_lv95sia405_eaux_cs_construction_speciale_surfcssoc, sia405_15_lv95sia405_eaux_cs_construction_speciale_ligne, sia405_15_lv95sia405_eaux_cs_construction_speciale_lignessoc, t_ili2db_inheritance, t_ili2db_settings, t_ili2db_model, station_de_pompage_genre, installation_genre, determination_planimetrique, etat, conduite_determination_planimetrique, organe_de_fermeture_sens_de_fermeture, lieu_de_fuite_genre, conduite_qualite_eau, point_de_conduite_determination_altimetrique, type_de_plan, conduite_materiau, connexion_tubulaire_genre, etatvaleurs, conduite_fonction, construction_speciale_genre, organe_de_fermeture_etat_de_la_connexion, conduite_lit_de_pose, conduite_assurance_contre_la_poussee, noeud_de_conduite_determination_planimetrique, installation_materiau, composant_materiau, noeud_de_conduite_determination_altimetrique, installation_determination_altimetrique, valignment, reservoir_d_eau_materiau, branchement_d_immeuble_piece_isolante, conduite_protection_cathodique, organe_de_fermeture_genre, hydrant_genre, autres_genre, halignment, point_de_conduite_determination_planimetrique, conduite_genre_de_raccordement, sia4055_lv95sia405_eaux_conduite_materiau, lieu_de_fuite_cause, sia4055_lv95sia405_eaux_conduite_fonction, composant_raccordement, organe_de_fermeture_materiau, conduite_isolation_exterieure, branchement_d_immeuble_branchement_d_immeuble, installation_determination_planimetrique, installation_d_approvisionnement_en_eau_genre, sia4055_lv95sia405_eaux_installation_genre, point_de_conduite_genre, sia4055_lv95sia405_eaux_construction_speciale_genre, connexion_tubulaire_assurance_contre_la_poussee, composant_genre, conduite_isolation_interieure, sia4055_lv95sia405_eaux_cs_conduite_determination_planmtrque, conduite_rehabilitation_renovation, construction_speciale_materiau, organe_de_fermeture_commande, hydrant_materiau, noeud_hydraulique_type_de_noeud, conduite_mode_de_pose, reservoir_d_eau_genre, t_ili2db_classname, t_ili2db_attrname, sia405_15_lv95sia405_eaux_cs_construction_speciale, noeud_hydraulique, noeud_hydraulique_texte, troncon_hydraulique, troncon_hydraulique_texte, metaattributs, autres, branchement_d_immeuble, composant, connexion_tubulaire, construction_speciale, installation, installation_d_approvisionnement_en_eau, lieu_de_fuite, organe_de_fermeture, point_de_conduite, sia405_15_lv95sia405_eaux_cs_noeud_de_conduite, sia405_15_lv95sia405_eaux_cs_installation, sia405_15_lv95sia405_eaux_cs_conduite, station_de_pompage, conduite_texte, noeud_de_conduite_texte, construction_speciale_surface, construction_speciale_ligne, construction_speciale_texte, position_plan_d_ensemble, sia405_15_lv95sia405_eaux_cs_conduite_texte, sia405_15_lv95sia405_eaux_cs_noeud_de_conduite_texte, sia405_15_lv95sia405_eaux_cs_construction_speciale_texte, t_ili2db_dataset, t_ili2db_basket
        # QWAT.chamber: WASSER.REPLACE_ME,
        # QWAT.installation: WASSER.REPLACE_ME,
        # QWAT.remote_type: WASSER.REPLACE_ME,
        # QWAT.watertype: WASSER.REPLACE_ME,
        # QWAT.network_element: WASSER.REPLACE_ME,
        # QWAT.distributor: WASSER.REPLACE_ME,
        # QWAT.folder: WASSER.REPLACE_ME,
        # QWAT.object_reference: WASSER.REPLACE_ME,
        # QWAT.precision: WASSER.REPLACE_ME,
        # QWAT.precisionalti: WASSER.REPLACE_ME,
        # QWAT.status: WASSER.REPLACE_ME,
        # QWAT.node: WASSER.REPLACE_ME,
        # QWAT.district: WASSER.REPLACE_ME,
        # QWAT.visible: WASSER.REPLACE_ME,
        # QWAT.pressurezone: WASSER.REPLACE_ME,
        # QWAT.consumptionzone: WASSER.REPLACE_ME,
        # QWAT.crossing: WASSER.REPLACE_ME,
        # QWAT.bedding: WASSER.REPLACE_ME,
        # QWAT.pipe_function: WASSER.REPLACE_ME,
        # QWAT.pipe_installmethod: WASSER.REPLACE_ME,
        # QWAT.pipe_material: WASSER.REPLACE_ME,
        # QWAT.pipe_protection: WASSER.REPLACE_ME,
        # QWAT.damage: WASSER.REPLACE_ME,
        # QWAT.leak: WASSER.REPLACE_ME,
        # QWAT.leak_cause: WASSER.REPLACE_ME,
        # QWAT.meter: WASSER.REPLACE_ME,
        # QWAT.cover: WASSER.REPLACE_ME,
        # QWAT.cover_type: WASSER.REPLACE_ME,
        # QWAT.part: WASSER.REPLACE_ME,
        # QWAT.part_type: WASSER.REPLACE_ME,
        # QWAT.hydrant_material: WASSER.REPLACE_ME,
        # QWAT.hydrant_model_inf: WASSER.REPLACE_ME,
        # QWAT.hydrant_model_sup: WASSER.REPLACE_ME,
        # QWAT.hydrant_output: WASSER.REPLACE_ME,
        # QWAT.hydrant_provider: WASSER.REPLACE_ME,
        # QWAT.meter_reference: WASSER.REPLACE_ME,
        # QWAT.cistern: WASSER.REPLACE_ME,
        # QWAT.overflow: WASSER.REPLACE_ME,
        # QWAT.tank_firestorage: WASSER.REPLACE_ME,
        # QWAT.protectionzone: WASSER.REPLACE_ME,
        # QWAT.protectionzone_type: WASSER.REPLACE_ME,
        # QWAT.remote: WASSER.REPLACE_ME,
        # QWAT.surveypoint: WASSER.REPLACE_ME,
        # QWAT.survey_type: WASSER.REPLACE_ME,
        # QWAT.worker: WASSER.REPLACE_ME,
        # QWAT.treatment: WASSER.REPLACE_ME,
        # QWAT.valve: WASSER.REPLACE_ME,
        # QWAT.valve_function: WASSER.REPLACE_ME,
        # QWAT.nominal_diameter: WASSER.REPLACE_ME,
        # QWAT.valve_type: WASSER.REPLACE_ME,
        # QWAT.valve_actuation: WASSER.REPLACE_ME,
        # QWAT.pressurecontrol_type: WASSER.REPLACE_ME,
        # QWAT.printmap: WASSER.REPLACE_ME,
        # QWAT.pump: WASSER.REPLACE_ME,
        # QWAT.pump_operating: WASSER.REPLACE_ME,
        # QWAT.pump_type: WASSER.REPLACE_ME,
        # QWAT.samplingpoint: WASSER.REPLACE_ME,
        # QWAT.subscriber: WASSER.REPLACE_ME,
        # QWAT.subscriber_type: WASSER.REPLACE_ME,
        # QWAT.subscriber_reference: WASSER.REPLACE_ME,
        # QWAT.source: WASSER.REPLACE_ME,
        # QWAT.source_quality: WASSER.REPLACE_ME,
        # QWAT.source_type: WASSER.REPLACE_ME,
    }

    for qwat_class, sia_classes in TABLE_MAPPING.items():

        available_fields = collections.defaultdict(list)
        for attr_name, attr in list(qwat_class.__dict__.items()):
            # if attr_name.startswith('__'):
            #     continue
            if not isinstance(attr, InstrumentedAttribute):
                continue
            if not hasattr(attr.property, "columns"):
                key = "_relations_"
            else:
                key = attr.property.columns[0].table.name
            available_fields[key].append(attr_name)

        classes = ", ".join(f"WASSER.{c.__name__}" for c in sia_classes)
        template.write(f'    print("Exporting QWAT.{qwat_class.__name__} -> {classes}")\n')
        template.write(f'    for row in session.query(QWAT.{qwat_class.__name__}):\n')
        template.write(f'        # AVAILABLE FIELDS\n\n')
        for src_table, fields in available_fields.items():
            fields.sort()
            template.write(f'        # --- {src_table} ---\n')
            template.write(f'        # {", ".join(fields)}\n\n')

        for sia_class in sia_classes:

            fields_to_map = collections.defaultdict(list)
            for attr_name, attr in list(sia_class.__dict__.items()):
                # if attr_name.startswith('__'):
                #     continue
                if not isinstance(attr, InstrumentedAttribute):
                    continue
                if not hasattr(attr.property, "columns"):
                    continue
                key = attr.property.columns[0].table.name
                fields_to_map[key].append(attr_name)

            template.write(f'        {sia_class.__name__} = WASSER.{sia_class.__name__}(\n')
            template.write(f'            # FIELDS TO MAP\n')
            for dst_table, fields in fields_to_map.items():
                fields.sort()
                template.write(f'\n            # --- {dst_table} ---\n')
                for field in sorted(fields):
                    template.write(f'            # {field}=row.REPLACE_ME,\n')
            template.write(f'        )\n')
            template.write(f'        session.add({sia_class.__name__})\n')
        template.write(f'        print(".", end="")\n')
        template.write(f'    print("done")\n\n')

    print("\n"*5)
    available_tables = ', '.join(sorted(c.__name__ for c in WASSER if c not in TABLE_MAPPING.values()))
    generator.write('TABLE_MAPPING = {\n')
    for qwat_class, sia_classes in TABLE_MAPPING.items():
        sia_classes_str = ",".join(f"WASSER.{c.__name__}" for c in sia_classes)
        generator.write(f"    QWAT.{qwat_class.__name__}: [{sia_classes_str}],\n")
    generator.write(f'    # NOT MAPPED YET\n')
    generator.write(f'    # AVAILABLE WASSER CLASSES : {available_tables}\n')
    for qwat_class in sorted(list(QWAT), key=lambda q: q.__name__):
        if qwat_class not in TABLE_MAPPING.keys():
            generator.write(f"    # QWAT.{qwat_class.__name__}: WASSER.REPLACE_ME,\n")
    generator.write('}\n\n')
