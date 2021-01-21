from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

import xml.etree.ElementTree as ET
import xml.dom.minidom


from . import utils
from . import config

from .datamodels.qgep import Classes as QGEP
from .datamodels.abwasser2015 import Classes as ABWASSER

###############################################
# Actual export (see qgep_generator to pregenerate some of this code)
###############################################

MAPPING = {
    'wastewater_structure': {
        'accessibility': {
            None: None,
            3444: 'ueberdeckt',
            3447: 'unbekannt',
            3446: 'unzugaenglich',
            3445: 'zugaenglich',
        }
    },
    'manhole': {
        'function': {
            None: None,
            4532: 'Absturzbauwerk',
            5344: 'andere',
            4533: 'Be_Entlueftung',
            3267: 'Dachwasserschacht',
            3266: 'Einlaufschacht',
            3472: 'Entwaesserungsrinne',
            228: 'Geleiseschacht',
            204: 'Kontrollschacht',
            1008: 'Oelabscheider',
            4536: 'Pumpwerk',
            5346: 'Regenueberlauf',
            2742: 'Schlammsammler',
            5347: 'Schwimmstoffabscheider',
            4537: 'Spuelschacht',
            4798: 'Trennbauwerk',
            5345: 'unbekannt',
        },
    },
}

def export():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

    # ADAPTED FROM 052a_sia405_abwasser_2015_2_d_interlisexport2.sql
    



    print("Exporting QGEP.organisation -> ABWASSER.organisation, ABWASSER.metaattribute")
    for row in session.query(QGEP.organisation):
        # AVAILABLE FIELDS IN QGEP.organisation

        # --- organisation ---
        # fk_dataowner, fk_provider, identifier, last_modification, obj_id, remark, uid

        # --- _relations_ ---
        # fk_dataowner_REL, fk_provider_REL

        organisation = ABWASSER.organisation(
            # FIELDS TO MAP TO ABWASSER.organisation

            # --- organisation ---
            auid=row.uid,
            bemerkung=row.remark,
            bezeichnung=row.identifier,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(organisation)
        metaattribute = ABWASSER.metaattribute(
            # FIELDS TO MAP TO ABWASSER.metaattribute
            
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='organisation',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- metaattribute ---
            datenherr=row.fk_dataowner_REL.identifier if row.fk_dataowner_REL else '???',
            datenlieferant=row.fk_provider_REL.identifier if row.fk_provider_REL else '???',
            letzte_aenderung=row.last_modification,
            sia405_baseclass_metaattribute=tid_maker.tid_for_row(row),
            t_id=tid_maker.tid_for_row(row),  # OD : is this OK ? Don't we need a different t_id from what inserted above in organisation ? if so, consider adding a "for_class" arg to tid_for_row
            t_seq=0,
        )
        session.add(metaattribute)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.channel -> ABWASSER.kanal")
    for row in session.query(QGEP.channel):
        # AVAILABLE FIELDS IN QGEP.channel

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- channel ---
        # bedding_encasement, connection_type, function_hierarchic, function_hydraulic, jetting_interval, obj_id, pipe_length, usage_current, usage_planned

        # --- _relations_ ---
        # BWREL_oorel_od_wwtp_structure_wastewater_structure, accessibility_REL, bedding_encasement_REL, connection_type_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_hierarchic_REL, function_hydraulic_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL, usage_current_REL, usage_planned_REL

        kanal = ABWASSER.kanal(
            # FIELDS TO MAP TO ABWASSER.kanal

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='kanal',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # bruttokosten=row.REPLACE_ME,
            # detailgeometrie=row.REPLACE_ME,
            # eigentuemerref=row.REPLACE_ME,
            # ersatzjahr=row.REPLACE_ME,
            # finanzierung=row.REPLACE_ME,
            # inspektionsintervall=row.REPLACE_ME,
            # sanierungsbedarf=row.REPLACE_ME,
            # standortname=row.REPLACE_ME,
            # subventionen=row.REPLACE_ME,
            # wbw_basisjahr=row.REPLACE_ME,
            # wbw_bauart=row.REPLACE_ME,
            # wiederbeschaffungswert=row.REPLACE_ME,
            zugaenglichkeit=MAPPING['wastewater_structure']['accessibility'][row.accessibility],

            # --- kanal ---
            # bettung_umhuellung=row.REPLACE_ME,
            # funktionhierarchisch=row.REPLACE_ME,
            # funktionhydraulisch=row.REPLACE_ME,
            # nutzungsart_geplant=row.REPLACE_ME,
            # nutzungsart_ist=row.REPLACE_ME,
            # rohrlaenge=row.REPLACE_ME,
            # spuelintervall=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
            # verbindungsart=row.REPLACE_ME,
        )
        session.add(kanal)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.manhole -> ABWASSER.normschacht")
    for row in session.query(QGEP.manhole):
        # AVAILABLE FIELDS IN QGEP.manhole

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- manhole ---
        # _orientation, dimension1, dimension2, function, material, obj_id, surface_inflow

        # --- _relations_ ---
        # BWREL_oorel_od_wwtp_structure_wastewater_structure, accessibility_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_REL, material_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL, surface_inflow_REL

        normschacht = ABWASSER.normschacht(
            # FIELDS TO MAP TO ABWASSER.normschacht

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='normschacht',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # bruttokosten=row.REPLACE_ME,
            # detailgeometrie=row.REPLACE_ME,
            # eigentuemerref=row.REPLACE_ME,
            # ersatzjahr=row.REPLACE_ME,
            # finanzierung=row.REPLACE_ME,
            # inspektionsintervall=row.REPLACE_ME,
            # sanierungsbedarf=row.REPLACE_ME,
            # standortname=row.REPLACE_ME,
            # subventionen=row.REPLACE_ME,
            # wbw_basisjahr=row.REPLACE_ME,
            # wbw_bauart=row.REPLACE_ME,
            # wiederbeschaffungswert=row.REPLACE_ME,
            # zugaenglichkeit=row.REPLACE_ME,

            # --- normschacht ---
            # dimension1=row.REPLACE_ME,
            # dimension2=row.REPLACE_ME,
            # funktion=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # oberflaechenzulauf=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(normschacht)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.discharge_point -> ABWASSER.einleitstelle")
    for row in session.query(QGEP.discharge_point):
        # AVAILABLE FIELDS IN QGEP.discharge_point

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- discharge_point ---
        # fk_sector_water_body, highwater_level, obj_id, relevance, terrain_level, upper_elevation, waterlevel_hydraulic

        # --- _relations_ ---
        # BWREL_oorel_od_wwtp_structure_wastewater_structure, accessibility_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, fk_sector_water_body_REL, relevance_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL

        einleitstelle = ABWASSER.einleitstelle(
            # FIELDS TO MAP TO ABWASSER.einleitstelle

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='einleitstelle',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # bruttokosten=row.REPLACE_ME,
            # detailgeometrie=row.REPLACE_ME,
            # eigentuemerref=row.REPLACE_ME,
            # ersatzjahr=row.REPLACE_ME,
            # finanzierung=row.REPLACE_ME,
            # inspektionsintervall=row.REPLACE_ME,
            # sanierungsbedarf=row.REPLACE_ME,
            # standortname=row.REPLACE_ME,
            # subventionen=row.REPLACE_ME,
            # wbw_basisjahr=row.REPLACE_ME,
            # wbw_bauart=row.REPLACE_ME,
            # wiederbeschaffungswert=row.REPLACE_ME,
            # zugaenglichkeit=row.REPLACE_ME,

            # --- einleitstelle ---
            # hochwasserkote=row.REPLACE_ME,
            # relevanz=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
            # terrainkote=row.REPLACE_ME,
            # wasserspiegel_hydraulik=row.REPLACE_ME,
        )
        session.add(einleitstelle)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.special_structure -> ABWASSER.spezialbauwerk")
    for row in session.query(QGEP.special_structure):
        # AVAILABLE FIELDS IN QGEP.special_structure

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- special_structure ---
        # bypass, emergency_spillway, function, obj_id, stormwater_tank_arrangement, upper_elevation

        # --- _relations_ ---
        # BWREL_oorel_od_wwtp_structure_wastewater_structure, accessibility_REL, bypass_REL, emergency_spillway_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, stormwater_tank_arrangement_REL, structure_condition_REL

        spezialbauwerk = ABWASSER.spezialbauwerk(
            # FIELDS TO MAP TO ABWASSER.spezialbauwerk

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='spezialbauwerk',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # bruttokosten=row.REPLACE_ME,
            # detailgeometrie=row.REPLACE_ME,
            # eigentuemerref=row.REPLACE_ME,
            # ersatzjahr=row.REPLACE_ME,
            # finanzierung=row.REPLACE_ME,
            # inspektionsintervall=row.REPLACE_ME,
            # sanierungsbedarf=row.REPLACE_ME,
            # standortname=row.REPLACE_ME,
            # subventionen=row.REPLACE_ME,
            # wbw_basisjahr=row.REPLACE_ME,
            # wbw_bauart=row.REPLACE_ME,
            # wiederbeschaffungswert=row.REPLACE_ME,
            # zugaenglichkeit=row.REPLACE_ME,

            # --- spezialbauwerk ---
            # bypass=row.REPLACE_ME,
            # funktion=row.REPLACE_ME,
            # notueberlauf=row.REPLACE_ME,
            # regenbecken_anordnung=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(spezialbauwerk)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.infiltration_installation -> ABWASSER.versickerungsanlage")
    for row in session.query(QGEP.infiltration_installation):
        # AVAILABLE FIELDS IN QGEP.infiltration_installation

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- infiltration_installation ---
        # absorption_capacity, defects, dimension1, dimension2, distance_to_aquifer, effective_area, emergency_spillway, fk_aquifier, kind, labeling, obj_id, seepage_utilization, upper_elevation, vehicle_access, watertightness

        # --- _relations_ ---
        # BWREL_oorel_od_wwtp_structure_wastewater_structure, accessibility_REL, defects_REL, emergency_spillway_REL, financing_REL, fk_aquifier_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, kind_REL, labeling_REL, renovation_necessity_REL, rv_construction_type_REL, seepage_utilization_REL, status_REL, structure_condition_REL, vehicle_access_REL, watertightness_REL

        versickerungsanlage = ABWASSER.versickerungsanlage(
            # FIELDS TO MAP TO ABWASSER.versickerungsanlage

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='versickerungsanlage',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # bruttokosten=row.REPLACE_ME,
            # detailgeometrie=row.REPLACE_ME,
            # eigentuemerref=row.REPLACE_ME,
            # ersatzjahr=row.REPLACE_ME,
            # finanzierung=row.REPLACE_ME,
            # inspektionsintervall=row.REPLACE_ME,
            # sanierungsbedarf=row.REPLACE_ME,
            # standortname=row.REPLACE_ME,
            # subventionen=row.REPLACE_ME,
            # wbw_basisjahr=row.REPLACE_ME,
            # wbw_bauart=row.REPLACE_ME,
            # wiederbeschaffungswert=row.REPLACE_ME,
            # zugaenglichkeit=row.REPLACE_ME,

            # --- versickerungsanlage ---
            # art=row.REPLACE_ME,
            # beschriftung=row.REPLACE_ME,
            # dimension1=row.REPLACE_ME,
            # dimension2=row.REPLACE_ME,
            # gwdistanz=row.REPLACE_ME,
            # maengel=row.REPLACE_ME,
            # notueberlauf=row.REPLACE_ME,
            # saugwagen=row.REPLACE_ME,
            # schluckvermoegen=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
            # versickerungswasser=row.REPLACE_ME,
            # wasserdichtheit=row.REPLACE_ME,
            # wirksameflaeche=row.REPLACE_ME,
        )
        session.add(versickerungsanlage)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.pipe_profile -> ABWASSER.rohrprofil")
    for row in session.query(QGEP.pipe_profile):
        # AVAILABLE FIELDS IN QGEP.pipe_profile

        # --- pipe_profile ---
        # fk_dataowner, fk_provider, height_width_ratio, identifier, last_modification, obj_id, profile_type, remark

        # --- _relations_ ---
        # fk_dataowner_REL, fk_provider_REL, profile_type_REL

        rohrprofil = ABWASSER.rohrprofil(
            # FIELDS TO MAP TO ABWASSER.rohrprofil

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='rohrprofil',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- rohrprofil ---
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # hoehenbreitenverhaeltnis=row.REPLACE_ME,
            # profiltyp=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(rohrprofil)
        print(".", end="")
    print("done")
    session.commit()


    print("Exporting QGEP.reach_point -> ABWASSER.haltungspunkt")
    for row in session.query(QGEP.reach_point):
        # AVAILABLE FIELDS IN QGEP.reach_point

        # --- reach_point ---
        # elevation_accuracy, fk_dataowner, fk_provider, fk_wastewater_networkelement, identifier, last_modification, level, obj_id, outlet_shape, position_of_connection, remark, situation_geometry

        # --- _relations_ ---
        # elevation_accuracy_REL, fk_dataowner_REL, fk_provider_REL, fk_wastewater_networkelement_REL, outlet_shape_REL

        haltungspunkt = ABWASSER.haltungspunkt(
            # FIELDS TO MAP TO ABWASSER.haltungspunkt

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='haltungspunkt',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- haltungspunkt ---
            # abwassernetzelementref=row.REPLACE_ME,
            # auslaufform=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # hoehengenauigkeit=row.REPLACE_ME,
            # kote=row.REPLACE_ME,
            # lage=row.REPLACE_ME,
            # lage_anschluss=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(haltungspunkt)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.wastewater_node -> ABWASSER.abwasserknoten")
    for row in session.query(QGEP.wastewater_node):
        # AVAILABLE FIELDS IN QGEP.wastewater_node

        # --- wastewater_networkelement ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark

        # --- wastewater_node ---
        # backflow_level, bottom_level, fk_hydr_geometry, obj_id, situation_geometry

        # --- _relations_ ---
        # fk_dataowner_REL, fk_hydr_geometry_REL, fk_provider_REL, fk_wastewater_structure_REL

        abwasserknoten = ABWASSER.abwasserknoten(
            # FIELDS TO MAP TO ABWASSER.abwasserknoten

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='abwasserknoten',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- abwassernetzelement ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,

            # --- abwasserknoten ---
            # lage=row.REPLACE_ME,
            # rueckstaukote=row.REPLACE_ME,
            # sohlenkote=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(abwasserknoten)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.reach -> ABWASSER.haltung")
    for row in session.query(QGEP.reach):
        # AVAILABLE FIELDS IN QGEP.reach

        # --- wastewater_networkelement ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark

        # --- reach ---
        # clear_height, coefficient_of_friction, elevation_determination, fk_pipe_profile, fk_reach_point_from, fk_reach_point_to, horizontal_positioning, inside_coating, length_effective, material, obj_id, progression_geometry, reliner_material, reliner_nominal_size, relining_construction, relining_kind, ring_stiffness, slope_building_plan, wall_roughness

        # --- _relations_ ---
        # elevation_determination_REL, fk_dataowner_REL, fk_pipe_profile_REL, fk_provider_REL, fk_reach_point_from_REL, fk_reach_point_to_REL, fk_wastewater_structure_REL, horizontal_positioning_REL, inside_coating_REL, material_REL, reliner_material_REL, relining_construction_REL, relining_kind_REL
        
        haltung = ABWASSER.haltung(
            # FIELDS TO MAP TO ABWASSER.haltung

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='haltung',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- abwassernetzelement ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,

            # --- haltung ---
            # innenschutz=row.REPLACE_ME,
            # laengeeffektiv=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # lichte_hoehe=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            nachhaltungspunktref=tid_maker.tid_for_row(row.fk_reach_point_to_REL),
            # plangefaelle=row.REPLACE_ME,
            # reibungsbeiwert=row.REPLACE_ME,
            # reliner_art=row.REPLACE_ME,
            # reliner_bautechnik=row.REPLACE_ME,
            # reliner_material=row.REPLACE_ME,
            # reliner_nennweite=row.REPLACE_ME,
            # ringsteifigkeit=row.REPLACE_ME,
            # rohrprofilref=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
            # verlauf=row.REPLACE_ME,
            vonhaltungspunktref=tid_maker.tid_for_row(row.fk_reach_point_from_REL),
            # wandrauhigkeit=row.REPLACE_ME,
        )
        session.add(haltung)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.dryweather_downspout -> ABWASSER.trockenwetterfallrohr")
    for row in session.query(QGEP.dryweather_downspout):
        # AVAILABLE FIELDS IN QGEP.dryweather_downspout

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- dryweather_downspout ---
        # diameter, obj_id

        # --- _relations_ ---
        # BWREL_oorel_od_access_aid_structure_part, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, renovation_demand_REL

        trockenwetterfallrohr = ABWASSER.trockenwetterfallrohr(
            # FIELDS TO MAP TO ABWASSER.trockenwetterfallrohr

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='trockenwetterfallrohr',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- bauwerksteil ---
            abwasserbauwerkref=tid_maker.tid_for_row(row.fk_wastewater_structure_REL),
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # instandstellung=row.REPLACE_ME,

            # --- trockenwetterfallrohr ---
            # durchmesser=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(trockenwetterfallrohr)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.access_aid -> ABWASSER.einstiegshilfe")
    for row in session.query(QGEP.access_aid):
        # AVAILABLE FIELDS IN QGEP.access_aid

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- access_aid ---
        # kind, obj_id

        # --- _relations_ ---
        # BWREL_oorel_od_access_aid_structure_part, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, kind_REL, renovation_demand_REL

        einstiegshilfe = ABWASSER.einstiegshilfe(
            # FIELDS TO MAP TO ABWASSER.einstiegshilfe

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='einstiegshilfe',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- bauwerksteil ---
            abwasserbauwerkref=tid_maker.tid_for_row(row.fk_wastewater_structure_REL),
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # instandstellung=row.REPLACE_ME,

            # --- einstiegshilfe ---
            # art=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(einstiegshilfe)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.dryweather_flume -> ABWASSER.trockenwetterrinne")
    for row in session.query(QGEP.dryweather_flume):
        # AVAILABLE FIELDS IN QGEP.dryweather_flume

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- dryweather_flume ---
        # material, obj_id

        # --- _relations_ ---
        # BWREL_oorel_od_access_aid_structure_part, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, material_REL, renovation_demand_REL

        trockenwetterrinne = ABWASSER.trockenwetterrinne(
            # FIELDS TO MAP TO ABWASSER.trockenwetterrinne

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='trockenwetterrinne',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- bauwerksteil ---
            abwasserbauwerkref=tid_maker.tid_for_row(row.fk_wastewater_structure_REL),
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # instandstellung=row.REPLACE_ME,

            # --- trockenwetterrinne ---
            # material=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(trockenwetterrinne)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.cover -> ABWASSER.deckel")
    for row in session.query(QGEP.cover):
        # AVAILABLE FIELDS IN QGEP.cover

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- cover ---
        # brand, cover_shape, diameter, fastening, level, material, obj_id, positional_accuracy, situation_geometry, sludge_bucket, venting

        # --- _relations_ ---
        # BWREL_oorel_od_access_aid_structure_part, cover_shape_REL, fastening_REL, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, material_REL, positional_accuracy_REL, renovation_demand_REL, sludge_bucket_REL, venting_REL

        deckel = ABWASSER.deckel(
            # FIELDS TO MAP TO ABWASSER.deckel

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='deckel',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- bauwerksteil ---
            abwasserbauwerkref=tid_maker.tid_for_row(row.fk_wastewater_structure_REL),
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # instandstellung=row.REPLACE_ME,

            # --- deckel ---
            # deckelform=row.REPLACE_ME,
            # durchmesser=row.REPLACE_ME,
            # entlueftung=row.REPLACE_ME,
            # fabrikat=row.REPLACE_ME,
            # kote=row.REPLACE_ME,
            # lage=row.REPLACE_ME,
            # lagegenauigkeit=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # schlammeimer=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
            # verschluss=row.REPLACE_ME,
        )
        session.add(deckel)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.benching -> ABWASSER.bankett")
    for row in session.query(QGEP.benching):
        # AVAILABLE FIELDS IN QGEP.benching

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- benching ---
        # kind, obj_id

        # --- _relations_ ---
        # BWREL_oorel_od_access_aid_structure_part, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, kind_REL, renovation_demand_REL

        bankett = ABWASSER.bankett(
            # FIELDS TO MAP TO ABWASSER.bankett

            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type='bankett',

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- bauwerksteil ---
            abwasserbauwerkref=tid_maker.tid_for_row(row.fk_wastewater_structure_REL),
            # bemerkung=row.REPLACE_ME,
            bezeichnung=row.identifier,
            # instandstellung=row.REPLACE_ME,

            # --- bankett ---
            # art=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(bankett)
        print(".", end="")
    print("done")
    session.commit()
