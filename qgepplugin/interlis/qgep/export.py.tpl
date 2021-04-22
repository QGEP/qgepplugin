from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from .. import utils

from .model_qgep import QGEP
from .model_abwasser import ABWASSER


def export():

    qgep_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    abwasser_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    tid_maker = utils.ili2db.TidMaker(id_attribute='obj_id')

    def create_metaattributes(row, session):
        metaattribute = ABWASSER.metaattribute(
            # FIELDS TO MAP TO ABWASSER.metaattribute
            # --- metaattribute ---
            # datenherr=row.REPLACE_ME,
            # datenlieferant=row.REPLACE_ME,
            # letzte_aenderung=row.REPLACE_ME,
            # sia405_baseclass_metaattribute=row.REPLACE_ME,
            # t_id=row.REPLACE_ME
            # t_seq=row.REPLACE_ME,
        )
        session.add(metaattribute)

    print("Exporting QGEP.organisation -> ABWASSER.organisation, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.organisation):

        # organisation --- fk_dataowner, fk_provider, identifier, last_modification, obj_id, remark, uid
        # _bwrel_ --- accident__BWREL_fk_dataowner, accident__BWREL_fk_provider, administrative_office__BWREL_obj_id, aquifier__BWREL_fk_dataowner, aquifier__BWREL_fk_provider, bathing_area__BWREL_fk_dataowner, bathing_area__BWREL_fk_provider, canton__BWREL_obj_id, catchment_area__BWREL_fk_dataowner, catchment_area__BWREL_fk_provider, connection_object__BWREL_fk_dataowner, connection_object__BWREL_fk_operator, connection_object__BWREL_fk_owner, connection_object__BWREL_fk_provider, control_center__BWREL_fk_dataowner, control_center__BWREL_fk_provider, cooperative__BWREL_obj_id, damage__BWREL_fk_dataowner, damage__BWREL_fk_provider, data_media__BWREL_fk_dataowner, data_media__BWREL_fk_provider, file__BWREL_fk_dataowner, file__BWREL_fk_provider, fish_pass__BWREL_fk_dataowner, fish_pass__BWREL_fk_provider, hazard_source__BWREL_fk_dataowner, hazard_source__BWREL_fk_owner, hazard_source__BWREL_fk_provider, hq_relation__BWREL_fk_dataowner, hq_relation__BWREL_fk_provider, hydr_geom_relation__BWREL_fk_dataowner, hydr_geom_relation__BWREL_fk_provider, hydr_geometry__BWREL_fk_dataowner, hydr_geometry__BWREL_fk_provider, hydraulic_char_data__BWREL_fk_dataowner, hydraulic_char_data__BWREL_fk_provider, maintenance_event__BWREL_fk_dataowner, maintenance_event__BWREL_fk_operating_company, maintenance_event__BWREL_fk_provider, measurement_result__BWREL_fk_dataowner, measurement_result__BWREL_fk_provider, measurement_series__BWREL_fk_dataowner, measurement_series__BWREL_fk_provider, measuring_device__BWREL_fk_dataowner, measuring_device__BWREL_fk_provider, measuring_point__BWREL_fk_dataowner, measuring_point__BWREL_fk_operator, measuring_point__BWREL_fk_provider, mechanical_pretreatment__BWREL_fk_dataowner, mechanical_pretreatment__BWREL_fk_provider, municipality__BWREL_obj_id, mutation__BWREL_fk_dataowner, mutation__BWREL_fk_provider, organisation__BWREL_fk_dataowner, organisation__BWREL_fk_provider, overflow__BWREL_fk_dataowner, overflow__BWREL_fk_provider, overflow_char__BWREL_fk_dataowner, overflow_char__BWREL_fk_provider, pipe_profile__BWREL_fk_dataowner, pipe_profile__BWREL_fk_provider, private__BWREL_obj_id, profile_geometry__BWREL_fk_dataowner, profile_geometry__BWREL_fk_provider, reach_point__BWREL_fk_dataowner, reach_point__BWREL_fk_provider, retention_body__BWREL_fk_dataowner, retention_body__BWREL_fk_provider, river_bank__BWREL_fk_dataowner, river_bank__BWREL_fk_provider, river_bed__BWREL_fk_dataowner, river_bed__BWREL_fk_provider, sector_water_body__BWREL_fk_dataowner, sector_water_body__BWREL_fk_provider, sludge_treatment__BWREL_fk_dataowner, sludge_treatment__BWREL_fk_provider, structure_part__BWREL_fk_dataowner, structure_part__BWREL_fk_provider, substance__BWREL_fk_dataowner, substance__BWREL_fk_provider, surface_runoff_parameters__BWREL_fk_dataowner, surface_runoff_parameters__BWREL_fk_provider, surface_water_bodies__BWREL_fk_dataowner, surface_water_bodies__BWREL_fk_provider, throttle_shut_off_unit__BWREL_fk_dataowner, throttle_shut_off_unit__BWREL_fk_provider, txt_symbol__BWREL_fk_dataowner, txt_symbol__BWREL_fk_provider, waste_water_association__BWREL_obj_id, waste_water_treatment__BWREL_fk_dataowner, waste_water_treatment__BWREL_fk_provider, waste_water_treatment_plant__BWREL_obj_id, wastewater_networkelement__BWREL_fk_dataowner, wastewater_networkelement__BWREL_fk_provider, wastewater_structure__BWREL_fk_dataowner, wastewater_structure__BWREL_fk_operator, wastewater_structure__BWREL_fk_owner, wastewater_structure__BWREL_fk_provider, wastewater_structure_symbol__BWREL_fk_dataowner, wastewater_structure_symbol__BWREL_fk_provider, water_catchment__BWREL_fk_dataowner, water_catchment__BWREL_fk_provider, water_control_structure__BWREL_fk_dataowner, water_control_structure__BWREL_fk_provider, water_course_segment__BWREL_fk_dataowner, water_course_segment__BWREL_fk_provider, wwtp_energy_use__BWREL_fk_dataowner, wwtp_energy_use__BWREL_fk_provider, zone__BWREL_fk_dataowner, zone__BWREL_fk_provider
        # _rel_ --- fk_dataowner__REL, fk_provider__REL

        organisation = ABWASSER.organisation(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- organisation ---
            # auid=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # bezeichnung=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
        )
        abwasser_session.add(organisation)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.channel -> ABWASSER.kanal, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.channel):

        # wastewater_structure --- _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # channel --- bedding_encasement, connection_type, function_hierarchic, function_hydraulic, jetting_interval, obj_id, pipe_length, usage_current, usage_planned
        # _bwrel_ --- measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id
        # _rel_ --- accessibility__REL, bedding_encasement__REL, connection_type__REL, financing__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, function_hierarchic__REL, function_hydraulic__REL, renovation_necessity__REL, rv_construction_type__REL, status__REL, structure_condition__REL, usage_current__REL, usage_planned__REL

        kanal = ABWASSER.kanal(

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
        abwasser_session.add(kanal)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.manhole -> ABWASSER.normschacht, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.manhole):

        # wastewater_structure --- _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # manhole --- _orientation, dimension1, dimension2, function, material, obj_id, surface_inflow
        # _bwrel_ --- measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id
        # _rel_ --- accessibility__REL, financing__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, function__REL, material__REL, renovation_necessity__REL, rv_construction_type__REL, status__REL, structure_condition__REL, surface_inflow__REL

        normschacht = ABWASSER.normschacht(

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
        abwasser_session.add(normschacht)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.discharge_point -> ABWASSER.einleitstelle, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.discharge_point):

        # wastewater_structure --- _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # discharge_point --- fk_sector_water_body, highwater_level, obj_id, relevance, terrain_level, upper_elevation, waterlevel_hydraulic
        # _bwrel_ --- measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id
        # _rel_ --- accessibility__REL, financing__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, fk_sector_water_body__REL, relevance__REL, renovation_necessity__REL, rv_construction_type__REL, status__REL, structure_condition__REL

        einleitstelle = ABWASSER.einleitstelle(

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
        abwasser_session.add(einleitstelle)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.special_structure -> ABWASSER.spezialbauwerk, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.special_structure):

        # wastewater_structure --- _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # special_structure --- bypass, emergency_spillway, function, obj_id, stormwater_tank_arrangement, upper_elevation
        # _bwrel_ --- measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id
        # _rel_ --- accessibility__REL, bypass__REL, emergency_spillway__REL, financing__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, function__REL, renovation_necessity__REL, rv_construction_type__REL, status__REL, stormwater_tank_arrangement__REL, structure_condition__REL

        spezialbauwerk = ABWASSER.spezialbauwerk(

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
        abwasser_session.add(spezialbauwerk)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.infiltration_installation -> ABWASSER.versickerungsanlage, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.infiltration_installation):

        # wastewater_structure --- _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # infiltration_installation --- absorption_capacity, defects, dimension1, dimension2, distance_to_aquifer, effective_area, emergency_spillway, fk_aquifier, kind, labeling, obj_id, seepage_utilization, upper_elevation, vehicle_access, watertightness
        # _bwrel_ --- measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_infiltration_installation, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, retention_body__BWREL_fk_infiltration_installation, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id
        # _rel_ --- accessibility__REL, defects__REL, emergency_spillway__REL, financing__REL, fk_aquifier__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, kind__REL, labeling__REL, renovation_necessity__REL, rv_construction_type__REL, seepage_utilization__REL, status__REL, structure_condition__REL, vehicle_access__REL, watertightness__REL

        versickerungsanlage = ABWASSER.versickerungsanlage(

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
        abwasser_session.add(versickerungsanlage)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.pipe_profile -> ABWASSER.rohrprofil, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.pipe_profile):

        # pipe_profile --- fk_dataowner, fk_provider, height_width_ratio, identifier, last_modification, obj_id, profile_type, remark
        # _bwrel_ --- profile_geometry__BWREL_fk_pipe_profile, reach__BWREL_fk_pipe_profile
        # _rel_ --- fk_dataowner__REL, fk_provider__REL, profile_type__REL

        rohrprofil = ABWASSER.rohrprofil(

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
        abwasser_session.add(rohrprofil)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.reach_point -> ABWASSER.haltungspunkt, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.reach_point):

        # reach_point --- elevation_accuracy, fk_dataowner, fk_provider, fk_wastewater_networkelement, identifier, last_modification, level, obj_id, outlet_shape, position_of_connection, remark, situation_geometry
        # _bwrel_ --- examination__BWREL_fk_reach_point, reach__BWREL_fk_reach_point_from, reach__BWREL_fk_reach_point_to
        # _rel_ --- elevation_accuracy__REL, fk_dataowner__REL, fk_provider__REL, fk_wastewater_networkelement__REL, outlet_shape__REL

        haltungspunkt = ABWASSER.haltungspunkt(

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
        abwasser_session.add(haltungspunkt)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.wastewater_node -> ABWASSER.abwasserknoten, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.wastewater_node):

        # wastewater_networkelement --- fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark
        # wastewater_node --- backflow_level, bottom_level, fk_hydr_geometry, obj_id, situation_geometry
        # _bwrel_ --- catchment_area__BWREL_fk_wastewater_networkelement_rw_current, catchment_area__BWREL_fk_wastewater_networkelement_rw_planned, catchment_area__BWREL_fk_wastewater_networkelement_ww_current, catchment_area__BWREL_fk_wastewater_networkelement_ww_planned, connection_object__BWREL_fk_wastewater_networkelement, hydraulic_char_data__BWREL_fk_wastewater_node, overflow__BWREL_fk_overflow_to, overflow__BWREL_fk_wastewater_node, reach_point__BWREL_fk_wastewater_networkelement, throttle_shut_off_unit__BWREL_fk_wastewater_node, wastewater_structure__BWREL_fk_main_wastewater_node
        # _rel_ --- fk_dataowner__REL, fk_hydr_geometry__REL, fk_provider__REL, fk_wastewater_structure__REL

        abwasserknoten = ABWASSER.abwasserknoten(

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
        abwasser_session.add(abwasserknoten)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.reach -> ABWASSER.haltung, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.reach):

        # wastewater_networkelement --- fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark
        # reach --- clear_height, coefficient_of_friction, elevation_determination, fk_pipe_profile, fk_reach_point_from, fk_reach_point_to, horizontal_positioning, inside_coating, length_effective, material, obj_id, progression_geometry, reliner_material, reliner_nominal_size, relining_construction, relining_kind, ring_stiffness, slope_building_plan, wall_roughness
        # _bwrel_ --- catchment_area__BWREL_fk_wastewater_networkelement_rw_current, catchment_area__BWREL_fk_wastewater_networkelement_rw_planned, catchment_area__BWREL_fk_wastewater_networkelement_ww_current, catchment_area__BWREL_fk_wastewater_networkelement_ww_planned, connection_object__BWREL_fk_wastewater_networkelement, reach_point__BWREL_fk_wastewater_networkelement, reach_text__BWREL_fk_reach, txt_text__BWREL_fk_reach
        # _rel_ --- elevation_determination__REL, fk_dataowner__REL, fk_pipe_profile__REL, fk_provider__REL, fk_reach_point_from__REL, fk_reach_point_to__REL, fk_wastewater_structure__REL, horizontal_positioning__REL, inside_coating__REL, material__REL, reliner_material__REL, relining_construction__REL, relining_kind__REL

        haltung = ABWASSER.haltung(

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
        abwasser_session.add(haltung)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.dryweather_downspout -> ABWASSER.trockenwetterfallrohr, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.dryweather_downspout):

        # structure_part --- fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand
        # dryweather_downspout --- diameter, obj_id
        # _bwrel_ --- access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id
        # _rel_ --- fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, renovation_demand__REL

        trockenwetterfallrohr = ABWASSER.trockenwetterfallrohr(

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
        abwasser_session.add(trockenwetterfallrohr)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.access_aid -> ABWASSER.einstiegshilfe, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.access_aid):

        # structure_part --- fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand
        # access_aid --- kind, obj_id
        # _bwrel_ --- access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id
        # _rel_ --- fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, kind__REL, renovation_demand__REL

        einstiegshilfe = ABWASSER.einstiegshilfe(

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
        abwasser_session.add(einstiegshilfe)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.dryweather_flume -> ABWASSER.trockenwetterrinne, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.dryweather_flume):

        # structure_part --- fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand
        # dryweather_flume --- material, obj_id
        # _bwrel_ --- access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id
        # _rel_ --- fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, material__REL, renovation_demand__REL

        trockenwetterrinne = ABWASSER.trockenwetterrinne(

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
        abwasser_session.add(trockenwetterrinne)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.cover -> ABWASSER.deckel, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.cover):

        # structure_part --- fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand
        # cover --- brand, cover_shape, diameter, fastening, level, material, obj_id, positional_accuracy, situation_geometry, sludge_bucket, venting
        # _bwrel_ --- access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id, wastewater_structure__BWREL_fk_main_cover
        # _rel_ --- cover_shape__REL, fastening__REL, fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, material__REL, positional_accuracy__REL, renovation_demand__REL, sludge_bucket__REL, venting__REL

        deckel = ABWASSER.deckel(

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
        abwasser_session.add(deckel)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.benching -> ABWASSER.bankett, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.benching):

        # structure_part --- fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand
        # benching --- kind, obj_id
        # _bwrel_ --- access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id
        # _rel_ --- fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, kind__REL, renovation_demand__REL

        bankett = ABWASSER.bankett(

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
        abwasser_session.add(bankett)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.examination -> ABWASSER.untersuchung, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.examination):

        # maintenance_event --- active_zone, base_data, cost, data_details, duration, fk_dataowner, fk_operating_company, fk_provider, identifier, kind, last_modification, operator, reason, remark, result, status, time_point
        # examination --- equipment, fk_reach_point, from_point_identifier, inspected_length, obj_id, recording_type, to_point_identifier, vehicle, videonumber, weather
        # _bwrel_ --- damage__BWREL_fk_examination, re_maintenance_event_wastewater_structure__BWREL_fk_maintenance_event
        # _rel_ --- fk_dataowner__REL, fk_operating_company__REL, fk_provider__REL, fk_reach_point__REL, kind__REL, recording_type__REL, status__REL, weather__REL

        untersuchung = ABWASSER.untersuchung(

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
        abwasser_session.add(untersuchung)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.damage_manhole -> ABWASSER.normschachtschaden, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.damage_manhole):

        # damage --- comments, connection, damage_begin, damage_end, damage_reach, distance, fk_dataowner, fk_examination, fk_provider, last_modification, quantification1, quantification2, single_damage_class, video_counter, view_parameters
        # damage_manhole --- manhole_damage_code, manhole_shaft_area, obj_id
        # _bwrel_ --- damage_channel_channel_damage_code__BWREL_obj_id
        # _rel_ --- connection__REL, fk_dataowner__REL, fk_examination__REL, fk_provider__REL, manhole_damage_code__REL, manhole_shaft_area__REL, single_damage_class__REL

        normschachtschaden = ABWASSER.normschachtschaden(

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
        abwasser_session.add(normschachtschaden)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.damage_channel -> ABWASSER.kanalschaden, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.damage_channel):

        # damage --- comments, connection, damage_begin, damage_end, damage_reach, distance, fk_dataowner, fk_examination, fk_provider, last_modification, quantification1, quantification2, single_damage_class, video_counter, view_parameters
        # damage_channel --- channel_damage_code, obj_id
        # _bwrel_ --- damage_channel_channel_damage_code__BWREL_obj_id
        # _rel_ --- channel_damage_code__REL, connection__REL, fk_dataowner__REL, fk_examination__REL, fk_provider__REL, single_damage_class__REL

        kanalschaden = ABWASSER.kanalschaden(

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
        abwasser_session.add(kanalschaden)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.data_media -> ABWASSER.datentraeger, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.data_media):

        # data_media --- fk_dataowner, fk_provider, identifier, kind, last_modification, location, obj_id, path, remark
        # _rel_ --- fk_dataowner__REL, fk_provider__REL, kind__REL

        datentraeger = ABWASSER.datentraeger(

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
        abwasser_session.add(datentraeger)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    print("Exporting QGEP.file -> ABWASSER.datei, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.file):

        # file --- class, fk_data_media, fk_dataowner, fk_provider, identifier, kind, last_modification, obj_id, object, path_relative, remark
        # _rel_ --- class__REL, fk_dataowner__REL, fk_provider__REL, kind__REL

        datei = ABWASSER.datei(

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
        abwasser_session.add(datei)
        create_metaattributes(row, session)
        print(".", end="")
    print("done")

    abwasser_session.commit()

    qgep_session.close()
    abwasser_session.close()