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

from sqlalchemy.exc import InvalidRequestError, ArgumentError
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

from .datamodels.qgep import Classes as QGEP
from .datamodels.abwasser2015 import Classes as ABWASSER

def generate():

    template_path = os.path.join(os.path.dirname(__file__), 'qgep.py.tpl')
    template = open(template_path, 'w', newline='\n')
    generator_path = os.path.join(os.path.dirname(__file__), 'qgep_generator.py.tpl')
    generator = open(generator_path, 'w', newline='\n')

    ###############################################
    # Code generation
    ###############################################

    TABLE_MAPPING = {
        QGEP.organisation: [ABWASSER.organisation, ABWASSER.metaattribute],
        QGEP.channel: [ABWASSER.kanal],
        QGEP.manhole: [ABWASSER.normschacht],
        QGEP.discharge_point: [ABWASSER.einleitstelle],
        QGEP.special_structure: [ABWASSER.spezialbauwerk],
        QGEP.infiltration_installation: [ABWASSER.versickerungsanlage],
        QGEP.pipe_profile: [ABWASSER.rohrprofil],
        QGEP.reach_point: [ABWASSER.haltungspunkt],
        QGEP.wastewater_node: [ABWASSER.abwasserknoten],
        QGEP.reach: [ABWASSER.haltung],
        QGEP.dryweather_downspout: [ABWASSER.trockenwetterfallrohr],
        QGEP.access_aid: [ABWASSER.einstiegshilfe],
        QGEP.dryweather_flume: [ABWASSER.trockenwetterrinne],
        QGEP.cover: [ABWASSER.deckel],
        QGEP.benching: [ABWASSER.bankett],

        # NOT MAPPED YET
        # AVAILABLE ABWASSER CLASSES : abwasserbauwerk, abwasserknoten, abwassernetzelement, bankett, baseclass, bauwerksteil, datei, datentraeger, deckel, einleitstelle, einstiegshilfe, erhaltungsereignis, haltung, haltung_alternativverlauf, haltungspunkt, kanal, kanalschaden, metaattribute, normschacht, normschachtschaden, organisation, organisation_teil_vonassoc, rohrprofil, schaden, sia405_baseclass, sia405_symbolpos, sia405_textpos, spezialbauwerk, symbolpos, t_ili2db_attrname, t_ili2db_basket, t_ili2db_classname, t_ili2db_dataset, t_ili2db_inheritance, t_ili2db_model, t_ili2db_settings, textpos, trockenwetterfallrohr, trockenwetterrinne, untersuchung, versickerungsanlage, videozaehlerstand
        # QGEP.access_aid: [ABWASSER.REPLACE_ME],
        # QGEP.access_aid_kind: [ABWASSER.REPLACE_ME],
        # QGEP.accident: [ABWASSER.REPLACE_ME],
        # QGEP.administrative_office: [ABWASSER.REPLACE_ME],
        # QGEP.aquifier: [ABWASSER.REPLACE_ME],
        # QGEP.backflow_prevention: [ABWASSER.REPLACE_ME],
        # QGEP.backflow_prevention_kind: [ABWASSER.REPLACE_ME],
        # QGEP.bathing_area: [ABWASSER.REPLACE_ME],
        # QGEP.benching: [ABWASSER.REPLACE_ME],
        # QGEP.benching_kind: [ABWASSER.REPLACE_ME],
        # QGEP.blocking_debris: [ABWASSER.REPLACE_ME],
        # QGEP.building: [ABWASSER.REPLACE_ME],
        # QGEP.canton: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_direct_discharge_current: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_direct_discharge_planned: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_drainage_system_current: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_drainage_system_planned: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_infiltration_current: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_infiltration_planned: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_retention_current: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_retention_planned: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_text: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_text_plantype: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_text_texthali: [ABWASSER.REPLACE_ME],
        # QGEP.catchment_area_text_textvali: [ABWASSER.REPLACE_ME],
        # QGEP.channel: [ABWASSER.REPLACE_ME],
        # QGEP.channel_bedding_encasement: [ABWASSER.REPLACE_ME],
        # QGEP.channel_connection_type: [ABWASSER.REPLACE_ME],
        # QGEP.channel_function_hierarchic: [ABWASSER.REPLACE_ME],
        # QGEP.channel_function_hydraulic: [ABWASSER.REPLACE_ME],
        # QGEP.channel_usage_current: [ABWASSER.REPLACE_ME],
        # QGEP.channel_usage_planned: [ABWASSER.REPLACE_ME],
        # QGEP.chute: [ABWASSER.REPLACE_ME],
        # QGEP.chute_kind: [ABWASSER.REPLACE_ME],
        # QGEP.chute_material: [ABWASSER.REPLACE_ME],
        # QGEP.connection_object: [ABWASSER.REPLACE_ME],
        # QGEP.control_center: [ABWASSER.REPLACE_ME],
        # QGEP.cooperative: [ABWASSER.REPLACE_ME],
        # QGEP.cover: [ABWASSER.REPLACE_ME],
        # QGEP.cover_cover_shape: [ABWASSER.REPLACE_ME],
        # QGEP.cover_fastening: [ABWASSER.REPLACE_ME],
        # QGEP.cover_material: [ABWASSER.REPLACE_ME],
        # QGEP.cover_positional_accuracy: [ABWASSER.REPLACE_ME],
        # QGEP.cover_sludge_bucket: [ABWASSER.REPLACE_ME],
        # QGEP.cover_venting: [ABWASSER.REPLACE_ME],
        # QGEP.dam: [ABWASSER.REPLACE_ME],
        # QGEP.dam_kind: [ABWASSER.REPLACE_ME],
        # QGEP.damage: [ABWASSER.REPLACE_ME],
        # QGEP.damage_channel_channel_damage_code: [ABWASSER.REPLACE_ME],
        # QGEP.damage_connection: [ABWASSER.REPLACE_ME],
        # QGEP.damage_manhole: [ABWASSER.REPLACE_ME],
        # QGEP.damage_manhole_manhole_damage_code: [ABWASSER.REPLACE_ME],
        # QGEP.damage_manhole_manhole_shaft_area: [ABWASSER.REPLACE_ME],
        # QGEP.damage_single_damage_class: [ABWASSER.REPLACE_ME],
        # QGEP.data_media: [ABWASSER.REPLACE_ME],
        # QGEP.data_media_kind: [ABWASSER.REPLACE_ME],
        # QGEP.discharge_point: [ABWASSER.REPLACE_ME],
        # QGEP.discharge_point_relevance: [ABWASSER.REPLACE_ME],
        # QGEP.drainage_system: [ABWASSER.REPLACE_ME],
        # QGEP.drainage_system_kind: [ABWASSER.REPLACE_ME],
        # QGEP.dryweather_downspout: [ABWASSER.REPLACE_ME],
        # QGEP.dryweather_flume: [ABWASSER.REPLACE_ME],
        # QGEP.dryweather_flume_material: [ABWASSER.REPLACE_ME],
        # QGEP.electric_equipment: [ABWASSER.REPLACE_ME],
        # QGEP.electric_equipment_kind: [ABWASSER.REPLACE_ME],
        # QGEP.electromechanical_equipment: [ABWASSER.REPLACE_ME],
        # QGEP.electromechanical_equipment_kind: [ABWASSER.REPLACE_ME],
        # QGEP.examination: [ABWASSER.REPLACE_ME],
        # QGEP.examination_recording_type: [ABWASSER.REPLACE_ME],
        # QGEP.examination_weather: [ABWASSER.REPLACE_ME],
        # QGEP.file: [ABWASSER.REPLACE_ME],
        # QGEP.file_class: [ABWASSER.REPLACE_ME],
        # QGEP.file_kind: [ABWASSER.REPLACE_ME],
        # QGEP.fish_pass: [ABWASSER.REPLACE_ME],
        # QGEP.ford: [ABWASSER.REPLACE_ME],
        # QGEP.fountain: [ABWASSER.REPLACE_ME],
        # QGEP.ground_water_protection_perimeter: [ABWASSER.REPLACE_ME],
        # QGEP.groundwater_protection_zone: [ABWASSER.REPLACE_ME],
        # QGEP.groundwater_protection_zone_kind: [ABWASSER.REPLACE_ME],
        # QGEP.hazard_source: [ABWASSER.REPLACE_ME],
        # QGEP.hq_relation: [ABWASSER.REPLACE_ME],
        # QGEP.hydr_geom_relation: [ABWASSER.REPLACE_ME],
        # QGEP.hydr_geometry: [ABWASSER.REPLACE_ME],
        # QGEP.hydraulic_char_data: [ABWASSER.REPLACE_ME],
        # QGEP.hydraulic_char_data_is_overflowing: [ABWASSER.REPLACE_ME],
        # QGEP.hydraulic_char_data_main_weir_kind: [ABWASSER.REPLACE_ME],
        # QGEP.hydraulic_char_data_pump_characteristics: [ABWASSER.REPLACE_ME],
        # QGEP.hydraulic_char_data_pump_usage_current: [ABWASSER.REPLACE_ME],
        # QGEP.hydraulic_char_data_status: [ABWASSER.REPLACE_ME],
        # QGEP.individual_surface: [ABWASSER.REPLACE_ME],
        # QGEP.individual_surface_function: [ABWASSER.REPLACE_ME],
        # QGEP.individual_surface_pavement: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation_defects: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation_emergency_spillway: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation_kind: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation_labeling: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation_seepage_utilization: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation_vehicle_access: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_installation_watertightness: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_zone: [ABWASSER.REPLACE_ME],
        # QGEP.infiltration_zone_infiltration_capacity: [ABWASSER.REPLACE_ME],
        # QGEP.lake: [ABWASSER.REPLACE_ME],
        # QGEP.leapingweir: [ABWASSER.REPLACE_ME],
        # QGEP.leapingweir_opening_shape: [ABWASSER.REPLACE_ME],
        # QGEP.lock: [ABWASSER.REPLACE_ME],
        # QGEP.maintenance_event: [ABWASSER.REPLACE_ME],
        # QGEP.maintenance_event_kind: [ABWASSER.REPLACE_ME],
        # QGEP.maintenance_event_status: [ABWASSER.REPLACE_ME],
        # QGEP.manhole_function: [ABWASSER.REPLACE_ME],
        # QGEP.manhole_material: [ABWASSER.REPLACE_ME],
        # QGEP.manhole_surface_inflow: [ABWASSER.REPLACE_ME],
        # QGEP.measurement_result: [ABWASSER.REPLACE_ME],
        # QGEP.measurement_result_measurement_type: [ABWASSER.REPLACE_ME],
        # QGEP.measurement_series: [ABWASSER.REPLACE_ME],
        # QGEP.measurement_series_kind: [ABWASSER.REPLACE_ME],
        # QGEP.measuring_device: [ABWASSER.REPLACE_ME],
        # QGEP.measuring_device_kind: [ABWASSER.REPLACE_ME],
        # QGEP.measuring_point: [ABWASSER.REPLACE_ME],
        # QGEP.measuring_point_damming_device: [ABWASSER.REPLACE_ME],
        # QGEP.measuring_point_purpose: [ABWASSER.REPLACE_ME],
        # QGEP.mechanical_pretreatment: [ABWASSER.REPLACE_ME],
        # QGEP.mechanical_pretreatment_kind: [ABWASSER.REPLACE_ME],
        # QGEP.municipality: [ABWASSER.REPLACE_ME],
        # QGEP.mutation: [ABWASSER.REPLACE_ME],
        # QGEP.mutation_kind: [ABWASSER.REPLACE_ME],
        # QGEP.overflow: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_actuation: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_adjustability: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_char: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_char_kind_overflow_characteristic: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_char_overflow_characteristic_digital: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_control: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_function: [ABWASSER.REPLACE_ME],
        # QGEP.overflow_signal_transmission: [ABWASSER.REPLACE_ME],
        # QGEP.param_ca_general: [ABWASSER.REPLACE_ME],
        # QGEP.param_ca_mouse1: [ABWASSER.REPLACE_ME],
        # QGEP.passage: [ABWASSER.REPLACE_ME],
        # QGEP.pipe_profile: [ABWASSER.REPLACE_ME],
        # QGEP.pipe_profile_profile_type: [ABWASSER.REPLACE_ME],
        # QGEP.planning_zone: [ABWASSER.REPLACE_ME],
        # QGEP.planning_zone_kind: [ABWASSER.REPLACE_ME],
        # QGEP.prank_weir: [ABWASSER.REPLACE_ME],
        # QGEP.prank_weir_weir_edge: [ABWASSER.REPLACE_ME],
        # QGEP.prank_weir_weir_kind: [ABWASSER.REPLACE_ME],
        # QGEP.private: [ABWASSER.REPLACE_ME],
        # QGEP.profile_geometry: [ABWASSER.REPLACE_ME],
        # QGEP.pump: [ABWASSER.REPLACE_ME],
        # QGEP.pump_contruction_type: [ABWASSER.REPLACE_ME],
        # QGEP.pump_placement_of_actuation: [ABWASSER.REPLACE_ME],
        # QGEP.pump_placement_of_pump: [ABWASSER.REPLACE_ME],
        # QGEP.pump_usage_current: [ABWASSER.REPLACE_ME],
        # QGEP.re_maintenance_event_wastewater_structure: [ABWASSER.REPLACE_ME],
        # QGEP.reach: [ABWASSER.REPLACE_ME],
        # QGEP.reach_elevation_determination: [ABWASSER.REPLACE_ME],
        # QGEP.reach_horizontal_positioning: [ABWASSER.REPLACE_ME],
        # QGEP.reach_inside_coating: [ABWASSER.REPLACE_ME],
        # QGEP.reach_material: [ABWASSER.REPLACE_ME],
        # QGEP.reach_point: [ABWASSER.REPLACE_ME],
        # QGEP.reach_point_elevation_accuracy: [ABWASSER.REPLACE_ME],
        # QGEP.reach_point_outlet_shape: [ABWASSER.REPLACE_ME],
        # QGEP.reach_reliner_material: [ABWASSER.REPLACE_ME],
        # QGEP.reach_relining_construction: [ABWASSER.REPLACE_ME],
        # QGEP.reach_relining_kind: [ABWASSER.REPLACE_ME],
        # QGEP.reach_text: [ABWASSER.REPLACE_ME],
        # QGEP.reach_text_plantype: [ABWASSER.REPLACE_ME],
        # QGEP.reach_text_texthali: [ABWASSER.REPLACE_ME],
        # QGEP.reach_text_textvali: [ABWASSER.REPLACE_ME],
        # QGEP.reservoir: [ABWASSER.REPLACE_ME],
        # QGEP.retention_body: [ABWASSER.REPLACE_ME],
        # QGEP.retention_body_kind: [ABWASSER.REPLACE_ME],
        # QGEP.river_bank: [ABWASSER.REPLACE_ME],
        # QGEP.river_bank_control_grade_of_river: [ABWASSER.REPLACE_ME],
        # QGEP.river_bank_river_control_type: [ABWASSER.REPLACE_ME],
        # QGEP.river_bank_shores: [ABWASSER.REPLACE_ME],
        # QGEP.river_bank_side: [ABWASSER.REPLACE_ME],
        # QGEP.river_bank_utilisation_of_shore_surroundings: [ABWASSER.REPLACE_ME],
        # QGEP.river_bank_vegetation: [ABWASSER.REPLACE_ME],
        # QGEP.river_bed: [ABWASSER.REPLACE_ME],
        # QGEP.river_bed_control_grade_of_river: [ABWASSER.REPLACE_ME],
        # QGEP.river_bed_kind: [ABWASSER.REPLACE_ME],
        # QGEP.river_bed_river_control_type: [ABWASSER.REPLACE_ME],
        # QGEP.river_kind: [ABWASSER.REPLACE_ME],
        # QGEP.rock_ramp: [ABWASSER.REPLACE_ME],
        # QGEP.rock_ramp_stabilisation: [ABWASSER.REPLACE_ME],
        # QGEP.sector_water_body: [ABWASSER.REPLACE_ME],
        # QGEP.sector_water_body_kind: [ABWASSER.REPLACE_ME],
        # QGEP.sludge_treatment: [ABWASSER.REPLACE_ME],
        # QGEP.sludge_treatment_stabilisation: [ABWASSER.REPLACE_ME],
        # QGEP.solids_retention: [ABWASSER.REPLACE_ME],
        # QGEP.solids_retention_type: [ABWASSER.REPLACE_ME],
        # QGEP.special_structure: [ABWASSER.REPLACE_ME],
        # QGEP.special_structure_bypass: [ABWASSER.REPLACE_ME],
        # QGEP.special_structure_emergency_spillway: [ABWASSER.REPLACE_ME],
        # QGEP.special_structure_function: [ABWASSER.REPLACE_ME],
        # QGEP.special_structure_stormwater_tank_arrangement: [ABWASSER.REPLACE_ME],
        # QGEP.structure_part: [ABWASSER.REPLACE_ME],
        # QGEP.structure_part_renovation_demand: [ABWASSER.REPLACE_ME],
        # QGEP.substance: [ABWASSER.REPLACE_ME],
        # QGEP.surface_runoff_parameters: [ABWASSER.REPLACE_ME],
        # QGEP.surface_water_bodies: [ABWASSER.REPLACE_ME],
        # QGEP.symbol_plantype: [ABWASSER.REPLACE_ME],
        # QGEP.tank_cleaning: [ABWASSER.REPLACE_ME],
        # QGEP.tank_cleaning_type: [ABWASSER.REPLACE_ME],
        # QGEP.tank_emptying: [ABWASSER.REPLACE_ME],
        # QGEP.tank_emptying_type: [ABWASSER.REPLACE_ME],
        # QGEP.text_plantype: [ABWASSER.REPLACE_ME],
        # QGEP.text_texthali: [ABWASSER.REPLACE_ME],
        # QGEP.text_textvali: [ABWASSER.REPLACE_ME],
        # QGEP.throttle_shut_off_unit: [ABWASSER.REPLACE_ME],
        # QGEP.throttle_shut_off_unit_actuation: [ABWASSER.REPLACE_ME],
        # QGEP.throttle_shut_off_unit_adjustability: [ABWASSER.REPLACE_ME],
        # QGEP.throttle_shut_off_unit_control: [ABWASSER.REPLACE_ME],
        # QGEP.throttle_shut_off_unit_kind: [ABWASSER.REPLACE_ME],
        # QGEP.throttle_shut_off_unit_signal_transmission: [ABWASSER.REPLACE_ME],
        # QGEP.txt_symbol: [ABWASSER.REPLACE_ME],
        # QGEP.txt_text: [ABWASSER.REPLACE_ME],
        # QGEP.waste_water_association: [ABWASSER.REPLACE_ME],
        # QGEP.waste_water_treatment: [ABWASSER.REPLACE_ME],
        # QGEP.waste_water_treatment_kind: [ABWASSER.REPLACE_ME],
        # QGEP.waste_water_treatment_plant: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_networkelement: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_node: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_accessibility: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_financing: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_renovation_necessity: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_rv_construction_type: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_status: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_structure_condition: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_symbol: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_symbol_plantype: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_text: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_text_plantype: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_text_texthali: [ABWASSER.REPLACE_ME],
        # QGEP.wastewater_structure_text_textvali: [ABWASSER.REPLACE_ME],
        # QGEP.water_body_protection_sector: [ABWASSER.REPLACE_ME],
        # QGEP.water_body_protection_sector_kind: [ABWASSER.REPLACE_ME],
        # QGEP.water_catchment: [ABWASSER.REPLACE_ME],
        # QGEP.water_catchment_kind: [ABWASSER.REPLACE_ME],
        # QGEP.water_control_structure: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_algae_growth: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_altitudinal_zone: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_dead_wood: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_depth_variability: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_discharge_regime: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_ecom_classification: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_kind: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_length_profile: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_macrophyte_coverage: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_section_morphology: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_slope: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_utilisation: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_water_hardness: [ABWASSER.REPLACE_ME],
        # QGEP.water_course_segment_width_variability: [ABWASSER.REPLACE_ME],
        # QGEP.wwtp_energy_use: [ABWASSER.REPLACE_ME],
        # QGEP.wwtp_structure_kind: [ABWASSER.REPLACE_ME],
        # QGEP.zone: [ABWASSER.REPLACE_ME],
    }

    for qgep_class, sia_classes in TABLE_MAPPING.items():

        available_fields = collections.defaultdict(list)
        for attr_name, attr in list(qgep_class.__dict__.items()):
            try:
                # if attr_name.startswith('__'):
                #     continue
                if not isinstance(attr, InstrumentedAttribute):
                    continue
                if not hasattr(attr.property, "columns"):
                    key = "_relations_"
                else:
                    key = attr.property.columns[0].table.name
                available_fields[key].append(attr_name)
            except (InvalidRequestError, ArgumentError):
                # TODO : not sure why this happens
                pass

        ordered_tables = ["_relations_"]+list(c.__table__.name for c in qgep_class.__mro__ if hasattr(c, '__table__'))
        available_fields = sorted(available_fields.items(), key=lambda i: ordered_tables.index(i[0]), reverse=True)

        classes = ", ".join(f"ABWASSER.{c.__name__}" for c in sia_classes)
        template.write(f'    print("Exporting QGEP.{qgep_class.__name__} -> {classes}")\n')
        template.write(f'    for row in session.query(QGEP.{qgep_class.__name__}):\n')
        template.write(f'        # AVAILABLE FIELDS IN QGEP.{qgep_class.__name__}\n\n')
        for src_table, fields in available_fields:
            fields.sort()
            template.write(f'        # --- {src_table} ---\n')
            template.write(f'        # {", ".join(fields)}\n\n')

        for sia_class in sia_classes:

            fields_to_map = collections.defaultdict(list)
            for attr_name, attr in list(sia_class.__dict__.items()):
                try:
                    # if attr_name.startswith('__'):
                    #     continue
                    if not isinstance(attr, InstrumentedAttribute):
                        continue
                    if not hasattr(attr.property, "columns"):
                        continue
                    key = attr.property.columns[0].table.name
                    fields_to_map[key].append(attr_name)
                except (InvalidRequestError, ArgumentError):
                    # TODO : not sure why this happens
                    pass
            ordered_tables = list(c.__table__.name for c in sia_class.__mro__ if hasattr(c, '__table__'))
            fields_to_map = sorted(fields_to_map.items(), key=lambda i: ordered_tables.index(i[0]), reverse=True)

            template.write(f'        {sia_class.__name__} = ABWASSER.{sia_class.__name__}(\n')
            template.write(f'            # FIELDS TO MAP TO ABWASSER.{sia_class.__name__}\n')
            for dst_table, fields in fields_to_map:
                fields.sort()
                template.write(f'\n            # --- {dst_table} ---\n')
                for field in sorted(fields):
                    template.write(f'            # {field}=row.REPLACE_ME,\n')
            template.write(f'        )\n')
            template.write(f'        session.add({sia_class.__name__})\n')
        template.write(f'        print(".", end="")\n')
        template.write(f'    print("done")\n')
        template.write(f'    session.commit()\n\n')

    print("\n"*5)
    available_tables = ', '.join(sorted(c.__name__ for c in ABWASSER if c not in TABLE_MAPPING.values()))
    generator.write('    TABLE_MAPPING = {\n')
    for qgep_class, sia_classes in TABLE_MAPPING.items():
        sia_classes_str = ", ".join(f"ABWASSER.{c.__name__}" for c in sia_classes)
        generator.write(f"        QGEP.{qgep_class.__name__}: [{sia_classes_str}],\n")
    generator.write(f'        # NOT MAPPED YET\n')
    generator.write(f'        # AVAILABLE ABWASSER CLASSES : {available_tables}\n')
    for qgep_class in sorted(list(QGEP), key=lambda q: q.__name__):
        if qgep_class not in TABLE_MAPPING.keys():
            generator.write(f"        # QGEP.{qgep_class.__name__}: [ABWASSER.REPLACE_ME],\n")
    generator.write('    }\n\n')
