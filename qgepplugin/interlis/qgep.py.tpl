from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from . import utils

from .datamodels.qgep import Classes as QGEP
from .datamodels.abwasser import Classes as ABWASSER


###############################################
# Export                                      #
###############################################

def export():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

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
            # auid=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

        )
        session.add(organisation)
        metaattribute = ABWASSER.metaattribute(
            # FIELDS TO MAP TO ABWASSER.metaattribute
            # --- metaattribute ---
            # datenherr=row.REPLACE_ME,
            # datenlieferant=row.REPLACE_ME,
            # letzte_aenderung=row.REPLACE_ME,
            # sia405_baseclass_metaattribute=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # t_seq=row.REPLACE_ME,

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
        # accessibility_REL, bedding_encasement_REL, connection_type_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_hierarchic_REL, function_hydraulic_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL, usage_current_REL, usage_planned_REL

        kanal = ABWASSER.kanal(
            # FIELDS TO MAP TO ABWASSER.kanal
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
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

            # --- kanal ---
            # bettung_umhuellung=row.REPLACE_ME,
            # funktionhierarchisch=row.REPLACE_ME,
            # funktionhydraulisch=row.REPLACE_ME,
            # nutzungsart_geplant=row.REPLACE_ME,
            # nutzungsart_ist=row.REPLACE_ME,
            # rohrlaenge=row.REPLACE_ME,
            # spuelintervall=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
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
        # accessibility_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_REL, material_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL, surface_inflow_REL

        normschacht = ABWASSER.normschacht(
            # FIELDS TO MAP TO ABWASSER.normschacht
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
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
            # t_id=row.REPLACE_ME,

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
        # accessibility_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, fk_sector_water_body_REL, relevance_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL

        einleitstelle = ABWASSER.einleitstelle(
            # FIELDS TO MAP TO ABWASSER.einleitstelle
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
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
            # t_id=row.REPLACE_ME,
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
        # accessibility_REL, bypass_REL, emergency_spillway_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, stormwater_tank_arrangement_REL, structure_condition_REL

        spezialbauwerk = ABWASSER.spezialbauwerk(
            # FIELDS TO MAP TO ABWASSER.spezialbauwerk
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
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
            # t_id=row.REPLACE_ME,

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
        # accessibility_REL, defects_REL, emergency_spillway_REL, financing_REL, fk_aquifier_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, kind_REL, labeling_REL, renovation_necessity_REL, rv_construction_type_REL, seepage_utilization_REL, status_REL, structure_condition_REL, vehicle_access_REL, watertightness_REL

        versickerungsanlage = ABWASSER.versickerungsanlage(
            # FIELDS TO MAP TO ABWASSER.versickerungsanlage
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- abwasserbauwerk ---
            # akten=row.REPLACE_ME,
            # astatus=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # baulicherzustand=row.REPLACE_ME,
            # baulos=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiberref=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
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
            # t_id=row.REPLACE_ME,
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
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- rohrprofil ---
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # hoehenbreitenverhaeltnis=row.REPLACE_ME,
            # profiltyp=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

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
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- haltungspunkt ---
            # abwassernetzelementref=row.REPLACE_ME,
            # auslaufform=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # hoehengenauigkeit=row.REPLACE_ME,
            # kote=row.REPLACE_ME,
            # lage=row.REPLACE_ME,
            # lage_anschluss=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

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
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- abwassernetzelement ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,

            # --- abwasserknoten ---
            # lage=row.REPLACE_ME,
            # rueckstaukote=row.REPLACE_ME,
            # sohlenkote=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

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
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- abwassernetzelement ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,

            # --- haltung ---
            # innenschutz=row.REPLACE_ME,
            # laengeeffektiv=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # lichte_hoehe=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # nachhaltungspunktref=row.REPLACE_ME,
            # plangefaelle=row.REPLACE_ME,
            # reibungsbeiwert=row.REPLACE_ME,
            # reliner_art=row.REPLACE_ME,
            # reliner_bautechnik=row.REPLACE_ME,
            # reliner_material=row.REPLACE_ME,
            # reliner_nennweite=row.REPLACE_ME,
            # ringsteifigkeit=row.REPLACE_ME,
            # rohrprofilref=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # verlauf=row.REPLACE_ME,
            # vonhaltungspunktref=row.REPLACE_ME,
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
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, renovation_demand_REL

        trockenwetterfallrohr = ABWASSER.trockenwetterfallrohr(
            # FIELDS TO MAP TO ABWASSER.trockenwetterfallrohr
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- bauwerksteil ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # instandstellung=row.REPLACE_ME,

            # --- trockenwetterfallrohr ---
            # durchmesser=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

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
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, kind_REL, renovation_demand_REL

        einstiegshilfe = ABWASSER.einstiegshilfe(
            # FIELDS TO MAP TO ABWASSER.einstiegshilfe
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- bauwerksteil ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # instandstellung=row.REPLACE_ME,

            # --- einstiegshilfe ---
            # art=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

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
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, material_REL, renovation_demand_REL

        trockenwetterrinne = ABWASSER.trockenwetterrinne(
            # FIELDS TO MAP TO ABWASSER.trockenwetterrinne
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- bauwerksteil ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # instandstellung=row.REPLACE_ME,

            # --- trockenwetterrinne ---
            # material=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

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
        # cover_shape_REL, fastening_REL, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, material_REL, positional_accuracy_REL, renovation_demand_REL, sludge_bucket_REL, venting_REL

        deckel = ABWASSER.deckel(
            # FIELDS TO MAP TO ABWASSER.deckel
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- bauwerksteil ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
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
            # t_id=row.REPLACE_ME,
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
        # fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, kind_REL, renovation_demand_REL

        bankett = ABWASSER.bankett(
            # FIELDS TO MAP TO ABWASSER.bankett
            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- bauwerksteil ---
            # abwasserbauwerkref=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # instandstellung=row.REPLACE_ME,

            # --- bankett ---
            # art=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,

        )
        session.add(bankett)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QGEP.examination -> ABWASSER.untersuchung")
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
        print(".", end="")
    print("done")
    session.commit()



###############################################
# Import                                      #
###############################################

def import_():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

    print("Importing ABWASSER.organisation, ABWASSER.metaattribute -> QGEP.organisation")
    for row in session.query(ABWASSER.organisation):
    # TODO : somehow join ABWASSER.metaattribute
        # AVAILABLE FIELDS IN ABWASSER.organisation

        # --- organisation ---
        # auid, bemerkung, bezeichnung, t_id

        # --- _relations_ ---
        # t_id_REL

        organisation = QGEP.organisation(
            # FIELDS TO MAP TO QGEP.organisation
            # --- organisation ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # uid=row.REPLACE_ME,

        )
        session.add(organisation)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.kanal -> QGEP.channel")
    for row in session.query(ABWASSER.kanal):
        # AVAILABLE FIELDS IN ABWASSER.kanal

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- kanal ---
        # bettung_umhuellung, funktionhierarchisch, funktionhydraulisch, nutzungsart_geplant, nutzungsart_ist, rohrlaenge, spuelintervall, t_id, verbindungsart

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        channel = QGEP.channel(
            # FIELDS TO MAP TO QGEP.channel
            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- channel ---
            # bedding_encasement=row.REPLACE_ME,
            # connection_type=row.REPLACE_ME,
            # function_hierarchic=row.REPLACE_ME,
            # function_hydraulic=row.REPLACE_ME,
            # jetting_interval=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # pipe_length=row.REPLACE_ME,
            # usage_current=row.REPLACE_ME,
            # usage_planned=row.REPLACE_ME,

        )
        session.add(channel)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.normschacht -> QGEP.manhole")
    for row in session.query(ABWASSER.normschacht):
        # AVAILABLE FIELDS IN ABWASSER.normschacht

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- normschacht ---
        # dimension1, dimension2, funktion, material, oberflaechenzulauf, t_id

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        manhole = QGEP.manhole(
            # FIELDS TO MAP TO QGEP.manhole
            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- manhole ---
            # _orientation=row.REPLACE_ME,
            # dimension1=row.REPLACE_ME,
            # dimension2=row.REPLACE_ME,
            # function=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # surface_inflow=row.REPLACE_ME,

        )
        session.add(manhole)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.einleitstelle -> QGEP.discharge_point")
    for row in session.query(ABWASSER.einleitstelle):
        # AVAILABLE FIELDS IN ABWASSER.einleitstelle

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- einleitstelle ---
        # hochwasserkote, relevanz, t_id, terrainkote, wasserspiegel_hydraulik

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        discharge_point = QGEP.discharge_point(
            # FIELDS TO MAP TO QGEP.discharge_point
            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- discharge_point ---
            # fk_sector_water_body=row.REPLACE_ME,
            # highwater_level=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # relevance=row.REPLACE_ME,
            # terrain_level=row.REPLACE_ME,
            # upper_elevation=row.REPLACE_ME,
            # waterlevel_hydraulic=row.REPLACE_ME,

        )
        session.add(discharge_point)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.spezialbauwerk -> QGEP.special_structure")
    for row in session.query(ABWASSER.spezialbauwerk):
        # AVAILABLE FIELDS IN ABWASSER.spezialbauwerk

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- spezialbauwerk ---
        # bypass, funktion, notueberlauf, regenbecken_anordnung, t_id

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        special_structure = QGEP.special_structure(
            # FIELDS TO MAP TO QGEP.special_structure
            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- special_structure ---
            # bypass=row.REPLACE_ME,
            # emergency_spillway=row.REPLACE_ME,
            # function=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # stormwater_tank_arrangement=row.REPLACE_ME,
            # upper_elevation=row.REPLACE_ME,

        )
        session.add(special_structure)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.versickerungsanlage -> QGEP.infiltration_installation")
    for row in session.query(ABWASSER.versickerungsanlage):
        # AVAILABLE FIELDS IN ABWASSER.versickerungsanlage

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- versickerungsanlage ---
        # art, beschriftung, dimension1, dimension2, gwdistanz, maengel, notueberlauf, saugwagen, schluckvermoegen, t_id, versickerungswasser, wasserdichtheit, wirksameflaeche

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        infiltration_installation = QGEP.infiltration_installation(
            # FIELDS TO MAP TO QGEP.infiltration_installation
            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- infiltration_installation ---
            # absorption_capacity=row.REPLACE_ME,
            # defects=row.REPLACE_ME,
            # dimension1=row.REPLACE_ME,
            # dimension2=row.REPLACE_ME,
            # distance_to_aquifer=row.REPLACE_ME,
            # effective_area=row.REPLACE_ME,
            # emergency_spillway=row.REPLACE_ME,
            # fk_aquifier=row.REPLACE_ME,
            # kind=row.REPLACE_ME,
            # labeling=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # seepage_utilization=row.REPLACE_ME,
            # upper_elevation=row.REPLACE_ME,
            # vehicle_access=row.REPLACE_ME,
            # watertightness=row.REPLACE_ME,

        )
        session.add(infiltration_installation)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.rohrprofil -> QGEP.pipe_profile")
    for row in session.query(ABWASSER.rohrprofil):
        # AVAILABLE FIELDS IN ABWASSER.rohrprofil

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- rohrprofil ---
        # bemerkung, bezeichnung, hoehenbreitenverhaeltnis, profiltyp, t_id

        pipe_profile = QGEP.pipe_profile(
            # FIELDS TO MAP TO QGEP.pipe_profile
            # --- pipe_profile ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # height_width_ratio=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # profile_type=row.REPLACE_ME,
            # remark=row.REPLACE_ME,

        )
        session.add(pipe_profile)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.haltungspunkt -> QGEP.reach_point")
    for row in session.query(ABWASSER.haltungspunkt):
        # AVAILABLE FIELDS IN ABWASSER.haltungspunkt

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- haltungspunkt ---
        # abwassernetzelementref, auslaufform, bemerkung, bezeichnung, hoehengenauigkeit, kote, lage, lage_anschluss, t_id

        # --- _relations_ ---
        # abwassernetzelementref_REL

        reach_point = QGEP.reach_point(
            # FIELDS TO MAP TO QGEP.reach_point
            # --- reach_point ---
            # elevation_accuracy=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_networkelement=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # level=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # outlet_shape=row.REPLACE_ME,
            # position_of_connection=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # situation_geometry=row.REPLACE_ME,

        )
        session.add(reach_point)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.abwasserknoten -> QGEP.wastewater_node")
    for row in session.query(ABWASSER.abwasserknoten):
        # AVAILABLE FIELDS IN ABWASSER.abwasserknoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwassernetzelement ---
        # abwasserbauwerkref, bemerkung, bezeichnung

        # --- abwasserknoten ---
        # lage, rueckstaukote, sohlenkote, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        wastewater_node = QGEP.wastewater_node(
            # FIELDS TO MAP TO QGEP.wastewater_node
            # --- wastewater_networkelement ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,

            # --- wastewater_node ---
            # backflow_level=row.REPLACE_ME,
            # bottom_level=row.REPLACE_ME,
            # fk_hydr_geometry=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # situation_geometry=row.REPLACE_ME,

        )
        session.add(wastewater_node)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.haltung -> QGEP.reach")
    for row in session.query(ABWASSER.haltung):
        # AVAILABLE FIELDS IN ABWASSER.haltung

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwassernetzelement ---
        # abwasserbauwerkref, bemerkung, bezeichnung

        # --- haltung ---
        # innenschutz, laengeeffektiv, lagebestimmung, lichte_hoehe, material, nachhaltungspunktref, plangefaelle, reibungsbeiwert, reliner_art, reliner_bautechnik, reliner_material, reliner_nennweite, ringsteifigkeit, rohrprofilref, t_id, verlauf, vonhaltungspunktref, wandrauhigkeit

        # --- _relations_ ---
        # abwasserbauwerkref_REL, nachhaltungspunktref_REL, rohrprofilref_REL, vonhaltungspunktref_REL

        reach = QGEP.reach(
            # FIELDS TO MAP TO QGEP.reach
            # --- wastewater_networkelement ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,

            # --- reach ---
            # clear_height=row.REPLACE_ME,
            # coefficient_of_friction=row.REPLACE_ME,
            # elevation_determination=row.REPLACE_ME,
            # fk_pipe_profile=row.REPLACE_ME,
            # fk_reach_point_from=row.REPLACE_ME,
            # fk_reach_point_to=row.REPLACE_ME,
            # horizontal_positioning=row.REPLACE_ME,
            # inside_coating=row.REPLACE_ME,
            # length_effective=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # progression_geometry=row.REPLACE_ME,
            # reliner_material=row.REPLACE_ME,
            # reliner_nominal_size=row.REPLACE_ME,
            # relining_construction=row.REPLACE_ME,
            # relining_kind=row.REPLACE_ME,
            # ring_stiffness=row.REPLACE_ME,
            # slope_building_plan=row.REPLACE_ME,
            # wall_roughness=row.REPLACE_ME,

        )
        session.add(reach)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.trockenwetterfallrohr -> QGEP.dryweather_downspout")
    for row in session.query(ABWASSER.trockenwetterfallrohr):
        # AVAILABLE FIELDS IN ABWASSER.trockenwetterfallrohr

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- trockenwetterfallrohr ---
        # durchmesser, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        dryweather_downspout = QGEP.dryweather_downspout(
            # FIELDS TO MAP TO QGEP.dryweather_downspout
            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- dryweather_downspout ---
            # diameter=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,

        )
        session.add(dryweather_downspout)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.einstiegshilfe -> QGEP.access_aid")
    for row in session.query(ABWASSER.einstiegshilfe):
        # AVAILABLE FIELDS IN ABWASSER.einstiegshilfe

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- einstiegshilfe ---
        # art, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        access_aid = QGEP.access_aid(
            # FIELDS TO MAP TO QGEP.access_aid
            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- access_aid ---
            # kind=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,

        )
        session.add(access_aid)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.trockenwetterrinne -> QGEP.dryweather_flume")
    for row in session.query(ABWASSER.trockenwetterrinne):
        # AVAILABLE FIELDS IN ABWASSER.trockenwetterrinne

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- trockenwetterrinne ---
        # material, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        dryweather_flume = QGEP.dryweather_flume(
            # FIELDS TO MAP TO QGEP.dryweather_flume
            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- dryweather_flume ---
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,

        )
        session.add(dryweather_flume)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.deckel -> QGEP.cover")
    for row in session.query(ABWASSER.deckel):
        # AVAILABLE FIELDS IN ABWASSER.deckel

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- deckel ---
        # deckelform, durchmesser, entlueftung, fabrikat, kote, lage, lagegenauigkeit, material, schlammeimer, t_id, verschluss

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        cover = QGEP.cover(
            # FIELDS TO MAP TO QGEP.cover
            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- cover ---
            # brand=row.REPLACE_ME,
            # cover_shape=row.REPLACE_ME,
            # diameter=row.REPLACE_ME,
            # fastening=row.REPLACE_ME,
            # level=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # positional_accuracy=row.REPLACE_ME,
            # situation_geometry=row.REPLACE_ME,
            # sludge_bucket=row.REPLACE_ME,
            # venting=row.REPLACE_ME,

        )
        session.add(cover)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing ABWASSER.bankett -> QGEP.benching")
    for row in session.query(ABWASSER.bankett):
        # AVAILABLE FIELDS IN ABWASSER.bankett

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- bankett ---
        # art, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        benching = QGEP.benching(
            # FIELDS TO MAP TO QGEP.benching
            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- benching ---
            # kind=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,

        )
        session.add(benching)
        print(".", end="")
    print("done")
    session.commit()
