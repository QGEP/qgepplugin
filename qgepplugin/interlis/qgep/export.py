from sqlalchemy.orm import Session
from sqlalchemy import inspect
from geoalchemy2.functions import ST_Transform, ST_Force2D
import warnings

from .. import utils

from .model_qgep import QGEP
from .model_abwasser import ABWASSER


def export():

    session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    tid_maker = utils.ili2db.TidMaker(id_attribute="obj_id")

    def create_metaattributes(row, session):
        metaattribute = ABWASSER.metaattribute(
            # FIELDS TO MAP TO ABWASSER.metaattribute
            # --- metaattribute ---
            datenherr=row.fk_dataowner_REL.identifier if row.fk_dataowner_REL else "???",
            datenlieferant=row.fk_provider_REL.identifier if row.fk_provider_REL else "???",
            letzte_aenderung=row.last_modification,
            sia405_baseclass_metaattribute=tid_maker.tid_for_row(row),
            t_id=tid_maker.tid_for_row(
                row
            ),  # OD : is this OK ? Don't we need a different t_id from what inserted above in organisation ? if so, consider adding a "for_class" arg to tid_for_row
            t_seq=0,
        )
        session.add(metaattribute)

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
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="organisation",
            # --- sia405_baseclass ---
            obj_id=row.obj_id,
            # --- organisation ---
            auid=row.uid,
            bemerkung=row.remark,
            bezeichnung=row.identifier,
            t_id=tid_maker.tid_for_row(row),
        )
        session.add(organisation)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.channel -> ABWASSER.kanal, ABWASSER.metaattribute")
    for row in session.query(QGEP.channel):
        # AVAILABLE FIELDS IN QGEP.channel

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- channel ---
        # bedding_encasement, connection_type, function_hierarchic, function_hydraulic, jetting_interval, obj_id, pipe_length, usage_current, usage_planned

        # --- _relations_ ---
        # accessibility_REL, bedding_encasement_REL, connection_type_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_hierarchic_REL, function_hydraulic_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL, usage_current_REL, usage_planned_REL

        kanal = ABWASSER.kanal(
            # FIELDS TO MAP TO ABWASSER.kanal
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="kanal",
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
            zugaenglichkeit=row.accessibility_REL.value_de if row.accessibility_REL else None,
            # --- kanal ---
            bettung_umhuellung=row.bedding_encasement_REL.value_de if row.bedding_encasement_REL else None,
            # funktionhierarchisch=row.REPLACE_ME,
            # funktionhydraulisch=row.REPLACE_ME,
            nutzungsart_geplant=row.usage_planned_REL.value_de if row.usage_planned_REL else None,
            nutzungsart_ist=row.usage_current_REL.value_de if row.usage_current_REL else None,
            # rohrlaenge=row.REPLACE_ME,
            # spuelintervall=row.REPLACE_ME,
            t_id=tid_maker.tid_for_row(row),
            # verbindungsart=row.REPLACE_ME,
        )
        session.add(kanal)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.manhole -> ABWASSER.normschacht, ABWASSER.metaattribute")
    for row in session.query(QGEP.manhole):
        # AVAILABLE FIELDS IN QGEP.manhole

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- manhole ---
        # _orientation, dimension1, dimension2, function, material, obj_id, surface_inflow

        # --- _relations_ ---
        # accessibility_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_REL, material_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL, surface_inflow_REL

        normschacht = ABWASSER.normschacht(
            # FIELDS TO MAP TO ABWASSER.normschacht
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="normschacht",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.discharge_point -> ABWASSER.einleitstelle, ABWASSER.metaattribute")
    for row in session.query(QGEP.discharge_point):
        # AVAILABLE FIELDS IN QGEP.discharge_point

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- discharge_point ---
        # fk_sector_water_body, highwater_level, obj_id, relevance, terrain_level, upper_elevation, waterlevel_hydraulic

        # --- _relations_ ---
        # accessibility_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, fk_sector_water_body_REL, relevance_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL

        einleitstelle = ABWASSER.einleitstelle(
            # FIELDS TO MAP TO ABWASSER.einleitstelle
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="einleitstelle",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.special_structure -> ABWASSER.spezialbauwerk, ABWASSER.metaattribute")
    for row in session.query(QGEP.special_structure):
        # AVAILABLE FIELDS IN QGEP.special_structure

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- special_structure ---
        # bypass, emergency_spillway, function, obj_id, stormwater_tank_arrangement, upper_elevation

        # --- _relations_ ---
        # accessibility_REL, bypass_REL, emergency_spillway_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, stormwater_tank_arrangement_REL, structure_condition_REL

        spezialbauwerk = ABWASSER.spezialbauwerk(
            # FIELDS TO MAP TO ABWASSER.spezialbauwerk
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="spezialbauwerk",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.infiltration_installation -> ABWASSER.versickerungsanlage, ABWASSER.metaattribute")
    for row in session.query(QGEP.infiltration_installation):
        # AVAILABLE FIELDS IN QGEP.infiltration_installation

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- infiltration_installation ---
        # absorption_capacity, defects, dimension1, dimension2, distance_to_aquifer, effective_area, emergency_spillway, fk_aquifier, kind, labeling, obj_id, seepage_utilization, upper_elevation, vehicle_access, watertightness

        # --- _relations_ ---
        # accessibility_REL, defects_REL, emergency_spillway_REL, financing_REL, fk_aquifier_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, kind_REL, labeling_REL, renovation_necessity_REL, rv_construction_type_REL, seepage_utilization_REL, status_REL, structure_condition_REL, vehicle_access_REL, watertightness_REL

        versickerungsanlage = ABWASSER.versickerungsanlage(
            # FIELDS TO MAP TO ABWASSER.versickerungsanlage
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="versickerungsanlage",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.pipe_profile -> ABWASSER.rohrprofil, ABWASSER.metaattribute")
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
            t_type="rohrprofil",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.reach_point -> ABWASSER.haltungspunkt, ABWASSER.metaattribute")
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
            t_type="haltungspunkt",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.wastewater_node -> ABWASSER.abwasserknoten, ABWASSER.metaattribute")
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
            t_type="abwasserknoten",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.reach -> ABWASSER.haltung, ABWASSER.metaattribute")
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
            t_type="haltung",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.dryweather_downspout -> ABWASSER.trockenwetterfallrohr, ABWASSER.metaattribute")
    for row in session.query(QGEP.dryweather_downspout):
        # AVAILABLE FIELDS IN QGEP.dryweather_downspout

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- dryweather_downspout ---
        # diameter, obj_id

        # --- _relations_ ---
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, renovation_demand_REL

        trockenwetterfallrohr = ABWASSER.trockenwetterfallrohr(
            # FIELDS TO MAP TO ABWASSER.trockenwetterfallrohr
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="trockenwetterfallrohr",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.access_aid -> ABWASSER.einstiegshilfe, ABWASSER.metaattribute")
    for row in session.query(QGEP.access_aid):
        # AVAILABLE FIELDS IN QGEP.access_aid

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- access_aid ---
        # kind, obj_id

        # --- _relations_ ---
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, kind_REL, renovation_demand_REL

        einstiegshilfe = ABWASSER.einstiegshilfe(
            # FIELDS TO MAP TO ABWASSER.einstiegshilfe
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="einstiegshilfe",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.dryweather_flume -> ABWASSER.trockenwetterrinne, ABWASSER.metaattribute")
    for row in session.query(QGEP.dryweather_flume):
        # AVAILABLE FIELDS IN QGEP.dryweather_flume

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- dryweather_flume ---
        # material, obj_id

        # --- _relations_ ---
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, material_REL, renovation_demand_REL

        trockenwetterrinne = ABWASSER.trockenwetterrinne(
            # FIELDS TO MAP TO ABWASSER.trockenwetterrinne
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="trockenwetterrinne",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.cover -> ABWASSER.deckel, ABWASSER.metaattribute")
    for row in session.query(QGEP.cover):
        # AVAILABLE FIELDS IN QGEP.cover

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- cover ---
        # brand, cover_shape, diameter, fastening, level, material, obj_id, positional_accuracy, situation_geometry, sludge_bucket, venting

        # --- _relations_ ---
        # cover_shape_REL, fastening_REL, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, material_REL, positional_accuracy_REL, renovation_demand_REL, sludge_bucket_REL, venting_REL

        deckel = ABWASSER.deckel(
            # FIELDS TO MAP TO ABWASSER.deckel
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="deckel",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.benching -> ABWASSER.bankett, ABWASSER.metaattribute")
    for row in session.query(QGEP.benching):
        # AVAILABLE FIELDS IN QGEP.benching

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- benching ---
        # kind, obj_id

        # --- _relations_ ---
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, kind_REL, renovation_demand_REL

        bankett = ABWASSER.bankett(
            # FIELDS TO MAP TO ABWASSER.bankett
            # --- baseclass ---
            t_ili_tid=row.obj_id,
            t_type="bankett",
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
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.examination -> ABWASSER.untersuchung, ABWASSER.metaattribute")
    for row in session.query(QGEP.examination):
        # AVAILABLE FIELDS IN QGEP.examination

        # --- maintenance_event ---
        # active_zone, base_data, cost, data_details, duration, fk_dataowner, fk_operating_company, fk_provider, identifier, kind, last_modification, operator, reason, remark, result, status, time_point

        # --- examination ---
        # equipment, fk_reach_point, from_point_identifier, inspected_length, obj_id, recording_type, to_point_identifier, vehicle, videonumber, weather

        # --- _relations_ ---
        # fk_dataowner_REL, fk_operating_company_REL, fk_provider_REL, fk_reach_point_REL, kind_REL, recording_type_REL, status_REL, weather_REL

        untersuchung = ABWASSER.untersuchung(
            # FIELDS TO MAP TO ABWASSER.untersuchung
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,
            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,
            # --- erhaltungsereignis ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # art=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # ausfuehrende_firmaref=row.REPLACE_ME,
            # ausfuehrender=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # datengrundlage=row.REPLACE_ME,
            # dauer=row.REPLACE_ME,
            # detaildaten=row.REPLACE_ME,
            # ergebnis=row.REPLACE_ME,
            # grund=row.REPLACE_ME,
            # kosten=row.REPLACE_ME,
            # zeitpunkt=row.REPLACE_ME,
            # --- untersuchung ---
            # bispunktbezeichnung=row.REPLACE_ME,
            # erfassungsart=row.REPLACE_ME,
            # fahrzeug=row.REPLACE_ME,
            # geraet=row.REPLACE_ME,
            # haltungspunktref=row.REPLACE_ME,
            # inspizierte_laenge=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # videonummer=row.REPLACE_ME,
            # vonpunktbezeichnung=row.REPLACE_ME,
            # witterung=row.REPLACE_ME,
        )
        session.add(untersuchung)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.damage_manhole -> ABWASSER.normschachtschaden, ABWASSER.metaattribute")
    for row in session.query(QGEP.damage_manhole):
        # AVAILABLE FIELDS IN QGEP.damage_manhole

        # --- damage ---
        # comments, connection, damage_begin, damage_end, damage_reach, distance, fk_dataowner, fk_examination, fk_provider, last_modification, quantification1, quantification2, single_damage_class, video_counter, view_parameters

        # --- damage_manhole ---
        # manhole_damage_code, manhole_shaft_area, obj_id

        # --- _relations_ ---
        # connection_REL, fk_dataowner_REL, fk_examination_REL, fk_provider_REL, manhole_damage_code_REL, manhole_shaft_area_REL, single_damage_class_REL

        normschachtschaden = ABWASSER.normschachtschaden(
            # FIELDS TO MAP TO ABWASSER.normschachtschaden
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,
            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,
            # --- schaden ---
            # anmerkung=row.REPLACE_ME,
            # ansichtsparameter=row.REPLACE_ME,
            # einzelschadenklasse=row.REPLACE_ME,
            # streckenschaden=row.REPLACE_ME,
            # untersuchungref=row.REPLACE_ME,
            # verbindung=row.REPLACE_ME,
            # videozaehlerstand=row.REPLACE_ME,
            # --- normschachtschaden ---
            # distanz=row.REPLACE_ME,
            # quantifizierung1=row.REPLACE_ME,
            # quantifizierung2=row.REPLACE_ME,
            # schachtbereich=row.REPLACE_ME,
            # schachtschadencode=row.REPLACE_ME,
            # schadenlageanfang=row.REPLACE_ME,
            # schadenlageende=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
        )
        session.add(normschachtschaden)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.damage_channel -> ABWASSER.kanalschaden, ABWASSER.metaattribute")
    for row in session.query(QGEP.damage_channel):
        # AVAILABLE FIELDS IN QGEP.damage_channel

        # --- damage ---
        # comments, connection, damage_begin, damage_end, damage_reach, distance, fk_dataowner, fk_examination, fk_provider, last_modification, quantification1, quantification2, single_damage_class, video_counter, view_parameters

        # --- damage_channel ---
        # channel_damage_code, obj_id

        # --- _relations_ ---
        # channel_damage_code_REL, connection_REL, fk_dataowner_REL, fk_examination_REL, fk_provider_REL, single_damage_class_REL

        kanalschaden = ABWASSER.kanalschaden(
            # FIELDS TO MAP TO ABWASSER.kanalschaden
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,
            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,
            # --- schaden ---
            # anmerkung=row.REPLACE_ME,
            # ansichtsparameter=row.REPLACE_ME,
            # einzelschadenklasse=row.REPLACE_ME,
            # streckenschaden=row.REPLACE_ME,
            # untersuchungref=row.REPLACE_ME,
            # verbindung=row.REPLACE_ME,
            # videozaehlerstand=row.REPLACE_ME,
            # --- kanalschaden ---
            # distanz=row.REPLACE_ME,
            # kanalschadencode=row.REPLACE_ME,
            # quantifizierung1=row.REPLACE_ME,
            # quantifizierung2=row.REPLACE_ME,
            # schadenlageanfang=row.REPLACE_ME,
            # schadenlageende=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
        )
        session.add(kanalschaden)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.data_media -> ABWASSER.datentraeger, ABWASSER.metaattribute")
    for row in session.query(QGEP.data_media):
        # AVAILABLE FIELDS IN QGEP.data_media

        # --- data_media ---
        # fk_dataowner, fk_provider, identifier, kind, last_modification, location, obj_id, path, remark

        # --- _relations_ ---
        # fk_dataowner_REL, fk_provider_REL, kind_REL

        datentraeger = ABWASSER.datentraeger(
            # FIELDS TO MAP TO ABWASSER.datentraeger
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,
            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,
            # --- datentraeger ---
            # art=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # pfad=row.REPLACE_ME,
            # standort=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
        )
        session.add(datentraeger)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    print("Exporting QGEP.file -> ABWASSER.datei, ABWASSER.metaattribute")
    for row in session.query(QGEP.file):
        # AVAILABLE FIELDS IN QGEP.file

        # --- file ---
        # class, fk_data_media, fk_dataowner, fk_provider, identifier, kind, last_modification, obj_id, object, path_relative, remark

        # --- _relations_ ---
        # class_REL, fk_dataowner_REL, fk_provider_REL, kind_REL

        datei = ABWASSER.datei(
            # FIELDS TO MAP TO ABWASSER.datei
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,
            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,
            # --- datei ---
            # art=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # datentraegerref=row.REPLACE_ME,
            # klasse=row.REPLACE_ME,
            # objekt=row.REPLACE_ME,
            # relativpfad=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
        )
        session.add(datei)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")
    # session.flush()

    session.commit()
