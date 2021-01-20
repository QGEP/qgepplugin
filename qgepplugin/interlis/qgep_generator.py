"""
This script is a code generator, helping to implement QGEP/QGEP -> ILI migrations scripts.

Setup is made in TABLE_MAPPING, where one QGEP/QGEP class can be matched to one or more ILI classes.

The script will generate corresponding code in `qgep.py.tpl`, which can then
be diffed/merged into the original `qgep.py` (recommending `Diff & Merge` extension in VSCode).

It will also generate `qgep_generator.py.tpl`, which can be diffed/merged into this file, 
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
from .ili2py import Ili2Py

from .datamodels.qgep import Classes as QGEP

def generate():

    template_path = os.path.join(os.path.dirname(__file__), 'qgep.py.tpl')
    template = open(template_path, 'w', newline='\n')
    generator_path = os.path.join(os.path.dirname(__file__), 'qgep_generator.py.tpl')
    generator = open(generator_path, 'w', newline='\n')

    ###############################################
    # Code generation
    ###############################################

    ili = Ili2Py([config.BASE_ILI_MODEL_FR, config.BASE_SIA_ILI_MODEL_FR, config.ABWASSER_ILI_MODEL_FR])


    TABLE_MAPPING = {
        QGEP.organisation: ["SIA405_EAUX_USEES_2015.ORGANISATION"],
        QGEP.wastewater_structure: ["SIA405_EAUX_USEES_2015.OUVRAGE_RESEAU_AS"],
        QGEP.channel: ["SIA405_EAUX_USEES_2015.CANALISATION"],
        QGEP.manhole: ["SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD"],
        QGEP.discharge_point: ["SIA405_EAUX_USEES_2015.EXUTOIRE"],
        QGEP.special_structure: ["SIA405_EAUX_USEES_2015.OUVRAGE_SPECIAL"],
        QGEP.infiltration_installation: ["SIA405_EAUX_USEES_2015.INSTALLATION_INFILTRATION"],
        QGEP.pipe_profile: ["SIA405_EAUX_USEES_2015.PROFIL_TUYAU"],
        QGEP.wastewater_networkelement: ["SIA405_EAUX_USEES_2015.ELEMENT_RESEAU_EVACUATION"],
        QGEP.reach_point: ["SIA405_EAUX_USEES_2015.POINT_TRONCON"],
        QGEP.wastewater_node: ["SIA405_EAUX_USEES_2015.NOEUD_RESEAU"],
        QGEP.reach: ["SIA405_EAUX_USEES_2015.TRONCON"],
        QGEP.structure_part: ["SIA405_EAUX_USEES_2015.ELEMENT_OUVRAGE"],
        QGEP.dryweather_downspout: ["SIA405_EAUX_USEES_2015.TUYAU_CHUTE"],
        # QGEP.access_aid: ["SIA405_EAUX_USEES_2015.DISPOSITIF_D_ACCES"],  # why is access_aid missing from QGEP ?
        # QGEP.dryweather_flume: ["SIA405_EAUX_USEES_2015.CUNETTE_DEBIT_TEMPS_SEC"],  # why is dryweather_flume missing from QGEP ?
        QGEP.cover: ["SIA405_EAUX_USEES_2015.COUVERCLE"],
        # QGEP.benching: ["SIA405_EAUX_USEES_2015.BANQUETTE"],  # why is benching missing from QGEP ?

        # NOT MAPPED YET
        # AVAILABLE WASSER CLASSES : Base_f.BaseClass, Base_f.SymbolePos, Base_f.TextePos, Base_f_LV95.BaseClass, Base_f_LV95.SymbolePos, Base_f_LV95.TextePos, SIA405_Base_f.SIA405_BaseClass, SIA405_Base_f.SIA405_SymbolePos, SIA405_Base_f.SIA405_TextePos, SIA405_Base_f_LV95.SIA405_BaseClass, SIA405_Base_f_LV95.SIA405_SymbolePos, SIA405_Base_f_LV95.SIA405_TextePos, SIA405_EAUX_USEES_2015., SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD, SIA405_EAUX_USEES_2015.COUVERCLE, SIA405_EAUX_USEES_2015., SIA405_EAUX_USEES_2015., SIA405_EAUX_USEES_2015.ELEMENT_OUVRAGE, SIA405_EAUX_USEES_2015.ELEMENT_RESEAU_EVACUATION, SIA405_EAUX_USEES_2015.INSTALLATION_INFILTRATION, SIA405_EAUX_USEES_2015., SIA405_EAUX_USEES_2015.ORGANISATION, SIA405_EAUX_USEES_2015.OUVRAGE_RESEAU_AS_Symbole, SIA405_EAUX_USEES_2015.OUVRAGE_RESEAU_AS_Texte, SIA405_EAUX_USEES_2015.OUVRAGE_SPECIAL, SIA405_EAUX_USEES_2015., SIA405_EAUX_USEES_2015.PROFIL_TUYAU, SIA405_EAUX_USEES_2015., SIA405_EAUX_USEES_2015.TRONCON_TRACE_ALTERNATIVE, SIA405_EAUX_USEES_2015.TRONCON_Texte, SIA405_EAUX_USEES_2015.
        # QGEP.accident: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.administrative_office: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.aquifier: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.backflow_prevention: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.bathing_area: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.blocking_debris: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.building: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.canton: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.catchment_area: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.catchment_area_text: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.channel: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.chute: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.connection_object: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.control_center: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.cooperative: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.dam: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.damage: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.damage_manhole: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.data_media: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.discharge_point: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.drainage_system: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.dryweather_downspout: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.electric_equipment: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.electromechanical_equipment: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.examination: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.file: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.fish_pass: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.ford: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.fountain: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.ground_water_protection_perimeter: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.groundwater_protection_zone: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.hazard_source: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.hq_relation: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.hydr_geom_relation: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.hydr_geometry: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.hydraulic_char_data: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.individual_surface: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.infiltration_installation: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.infiltration_zone: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.lake: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.leapingweir: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.lock: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.maintenance_event: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.measurement_result: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.measurement_series: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.measuring_device: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.measuring_point: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.mechanical_pretreatment: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.municipality: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.mutation: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.overflow: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.overflow_char: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.param_ca_general: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.param_ca_mouse1: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.passage: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.pipe_profile: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.planning_zone: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.prank_weir: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.private: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.profile_geometry: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.pump: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.re_maintenance_event_wastewater_structure: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.reach: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.reach_point: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.reach_text: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.reservoir: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.retention_body: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.river_bank: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.river_bed: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.rock_ramp: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.sector_water_body: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.sludge_treatment: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.solids_retention: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.special_structure: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.structure_part: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.substance: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.surface_runoff_parameters: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.surface_water_bodies: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.tank_cleaning: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.tank_emptying: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.throttle_shut_off_unit: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.txt_symbol: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.txt_text: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.waste_water_association: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.waste_water_treatment: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.waste_water_treatment_plant: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.wastewater_networkelement: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.wastewater_node: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.wastewater_structure: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.wastewater_structure_symbol: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.wastewater_structure_text: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.water_body_protection_sector: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.water_catchment: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.water_control_structure: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.water_course_segment: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.wwtp_energy_use: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
        # QGEP.zone: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],
    }

    for qgep_class, sia_classes in TABLE_MAPPING.items():

        available_fields = collections.defaultdict(list)
        for attr_name, attr in list(qgep_class.__dict__.items()):
            # if attr_name.startswith('__'):
            #     continue
            if not isinstance(attr, InstrumentedAttribute):
                continue
            if not hasattr(attr.property, "columns"):
                key = "_relations_"
            else:
                key = attr.property.columns[0].table.name
            available_fields[key].append(attr_name)
        ordered_tables = ["_relations_"]+list(c.__table__.name for c in qgep_class.__mro__ if hasattr(c, '__table__'))
        available_fields = sorted(available_fields.items(), key=lambda i: ordered_tables.index(i[0]), reverse=True)

        template.write(f'    print("Exporting QGEP.{qgep_class.__name__} -> {", ".join(sia_classes)}")\n')
        template.write(f'    for row in session.query(QGEP.{qgep_class.__name__}):\n')

        for src_table, fields in available_fields:
            fields.sort()
            template.write(f'        # AVAILABLE FIELDS FROM {src_table}\n')
            template.write(f'        # {", ".join(fields)}\n')
        
        template.write('\n')

        for sia_class in sia_classes:
            
            template.write(f'        e = ET.SubElement(\n')
            template.write(f'            datasection,\n')
            template.write(f'            "{sia_class}",\n')
            template.write(f'            {{"TID": row.obj_id}},\n')
            template.write(f'        )\n')      

            class_ = ili.classes[sia_class]
            prev_dst_table = None
            for dst_table, field in class_.all_attributes:
                if prev_dst_table != dst_table:                    
                    template.write(f'\n        # --- {dst_table} ---\n')
                    prev_dst_table = dst_table
                template.write(f'        # ET.SubElement(e, "{field}").text = row.REPLACE_ME\n')
        template.write(f'        print(".", end="")\n')
        template.write(f'    print("done")\n\n')

    print("\n"*5)
    available_tables = ', '.join(sorted(c for c in ili.classes if c not in TABLE_MAPPING.values() and not c.startswith('SIA405_EAUX_USEES_2015_LV95')))
    generator.write('    TABLE_MAPPING = {\n')
    for qgep_class, sia_classes in TABLE_MAPPING.items():
        quoted_classes = ', '.join(f'"{c}"' for c in sia_classes)
        generator.write(f"        QGEP.{qgep_class.__name__}: [{quoted_classes}],\n")
    generator.write(f'        # NOT MAPPED YET\n')
    generator.write(f'        # AVAILABLE CLASSES : {available_tables}\n')
    for qgep_class in sorted(list(QGEP), key=lambda q: q.__name__):
        if qgep_class not in TABLE_MAPPING.keys():
            if qgep_class.__table__.schema == 'qgep_od':
                generator.write(f'        # QGEP.{qgep_class.__name__}: ["SIA405_EAUX_USEES_2015.REPLACE_ME"],\n')
    generator.write('    }\n\n')