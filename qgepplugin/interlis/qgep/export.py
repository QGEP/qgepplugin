from sqlalchemy.orm import Session
from sqlalchemy import inspect
from geoalchemy2.functions import ST_Transform, ST_Force2D, ST_CurveToLine
import warnings

from .. import utils

from .model_qgep import get_qgep_model
from .model_abwasser import get_abwasser_model

from ..utils.various import logger


def qgep_export(downstream_of=None, upstream_of=None):
    """
    Export data from the QGEP model into the ili2pg model.

    Args:
        downstream_of:  if provided, limits the export to nodes that are downstream of the provided node
        upstream_of:    if provided, limits the export to nodes that are upstream of the provided node
    """


    QGEP = get_qgep_model()
    ABWASSER = get_abwasser_model()

    # TODO: use two different sessions for reading and writing as in qgep.import_
    qgep_session = Session(utils.sqlalchemy.create_engine(logger_name="qgep"), autocommit=False, autoflush=False)
    abwasser_session = Session(utils.sqlalchemy.create_engine(logger_name="abwasser"), autocommit=False, autoflush=False)
    tid_maker = utils.ili2db.TidMaker(id_attribute='obj_id')

    # Upstream/Downstream filtering
    upstream_of='ch13p7mzWN008128'
    downstream_of='ch13p7mzWN005856'

    upstream_query = """
        WITH RECURSIVE node_with_child AS (
            SELECT n.obj_id, s.to_obj_id AS child_id FROM qgep_od.vw_network_node n
            LEFT JOIN qgep_od.vw_network_segment s ON s.from_obj_id = n.obj_id
        ),
        upstream AS (
            SELECT obj_id, child_id, 0 AS depth
            FROM node_with_child
            WHERE obj_id = :upstream_of_node_id

            UNION ALL

            SELECT n.obj_id, n.child_id, upstream.depth - 1
            FROM node_with_child n
            INNER JOIN upstream ON upstream.obj_id = n.child_id
        )
        SELECT obj_id
        FROM upstream;
    """

    # rows = qgep_session.execute(upstream_query, {'upstream_of_node_id':upstream_of})
    # limit_ids = list(row[0] for row in rows)
    # print(limit_ids)
    # exit(0)

        # ids = ...

    def get_tid(relation):
        """
        Makes a tid for a relation
        """
        if relation is None:
            return None
        return tid_maker.tid_for_row(relation)

    def get_vl(relation):
        """
        Gets a literal value from a value list relation
        """
        if relation is None:
            return None
        return relation.value_de

    def create_metaattributes(row):
        metaattribute = ABWASSER.metaattribute(
            # FIELDS TO MAP TO ABWASSER.metaattribute
            # --- metaattribute ---
            datenherr=getattr(row.fk_dataowner__REL, "name", 'unknown'),  # TODO : is unknown ok ?
            datenlieferant=getattr(row.fk_provider__REL, "name", 'unknown'),  # TODO : is unknown ok ?
            letzte_aenderung=row.last_modification,
            sia405_baseclass_metaattribute=get_tid(row),
            # OD : is this OK ? Don't we need a different t_id from what inserted above in organisation ? if so, consider adding a "for_class" arg to tid_for_row
            t_id=get_tid(row),
            t_seq=0,
        )
        abwasser_session.add(metaattribute)

    def base_common(row, type_name):
        """
        Returns common attributes for base
        """
        return {
            "t_ili_tid": row.obj_id,
            "t_type": type_name,
            "obj_id": row.obj_id,
            "t_id": get_tid(row),
        }

    def wastewater_structure_common(row):
        """
        Returns common attributes for wastewater_structure
        """
        warnings.warn(f'Mapping of wastewater_structure->abwasserbauwerk is not fully implemented.')
        return {
            # --- abwasserbauwerk ---
            # 'akten': row.REPLACE_ME,  # TODO : not sure, is it contract_section or records ?
            'astatus': get_vl(row.status__REL),
            'baujahr': row.year_of_construction,
            'baulicherzustand': row.structure_condition,
            # 'baulos': row.REPLACE_ME,  # TODO : not sure, is it contract_section or records ?
            'bemerkung': row.remark,
            'betreiberref': get_tid(row.fk_operator__REL),
            'bezeichnung': row.identifier,
            'bruttokosten': row.gross_costs,
            'detailgeometrie': ST_Force2D(row.detail_geometry_geometry),
            'eigentuemerref': get_tid(row.fk_owner__REL),
            'ersatzjahr': row.year_of_replacement,
            'finanzierung': row.financing,
            'inspektionsintervall': row.inspection_interval,
            'sanierungsbedarf': row.renovation_necessity,
            'standortname': row.location_name,
            'subventionen': row.subsidies,
            'wbw_basisjahr': row.rv_base_year,
            'wbw_bauart': get_vl(row.rv_construction_type__REL),
            'wiederbeschaffungswert': row.replacement_value,
            'zugaenglichkeit': get_vl(row.accessibility__REL),
        }

    def wastewater_network_element_common(row):
        """
        Returns common attributes for network_element
        """

        return {
            'abwasserbauwerkref': get_tid(row.fk_wastewater_structure__REL),
            'bemerkung': row.remark,
            'bezeichnung': row.identifier,
        }

    def structure_part_common(row):
        """
        Returns common attributes for structure_part
        """
        return {
            'abwasserbauwerkref': get_tid(row.fk_wastewater_structure__REL),
            'bemerkung': row.remark,
            'bezeichnung': row.identifier,
            'instandstellung': get_vl(row.renovation_demand__REL),
        }

    # ADAPTED FROM 052a_sia405_abwasser_2015_2_d_interlisexport2.sql
    logger.info("Exporting QGEP.organisation -> ABWASSER.organisation, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.organisation):

        # AVAILABLE FIELDS IN QGEP.organisation

        # --- organisation ---
        # fk_dataowner, fk_provider, identifier, last_modification, obj_id, remark, uid

        # --- _bwrel_ ---
        # accident__BWREL_fk_dataowner, accident__BWREL_fk_provider, administrative_office__BWREL_obj_id, aquifier__BWREL_fk_dataowner, aquifier__BWREL_fk_provider, bathing_area__BWREL_fk_dataowner, bathing_area__BWREL_fk_provider, canton__BWREL_obj_id, catchment_area__BWREL_fk_dataowner, catchment_area__BWREL_fk_provider, connection_object__BWREL_fk_dataowner, connection_object__BWREL_fk_operator, connection_object__BWREL_fk_owner, connection_object__BWREL_fk_provider, control_center__BWREL_fk_dataowner, control_center__BWREL_fk_provider, cooperative__BWREL_obj_id, damage__BWREL_fk_dataowner, damage__BWREL_fk_provider, data_media__BWREL_fk_dataowner, data_media__BWREL_fk_provider, file__BWREL_fk_dataowner, file__BWREL_fk_provider, fish_pass__BWREL_fk_dataowner, fish_pass__BWREL_fk_provider, hazard_source__BWREL_fk_dataowner, hazard_source__BWREL_fk_owner, hazard_source__BWREL_fk_provider, hq_relation__BWREL_fk_dataowner, hq_relation__BWREL_fk_provider, hydr_geom_relation__BWREL_fk_dataowner, hydr_geom_relation__BWREL_fk_provider, hydr_geometry__BWREL_fk_dataowner, hydr_geometry__BWREL_fk_provider, hydraulic_char_data__BWREL_fk_dataowner, hydraulic_char_data__BWREL_fk_provider, maintenance_event__BWREL_fk_dataowner, maintenance_event__BWREL_fk_operating_company, maintenance_event__BWREL_fk_provider, measurement_result__BWREL_fk_dataowner, measurement_result__BWREL_fk_provider, measurement_series__BWREL_fk_dataowner, measurement_series__BWREL_fk_provider, measuring_device__BWREL_fk_dataowner, measuring_device__BWREL_fk_provider, measuring_point__BWREL_fk_dataowner, measuring_point__BWREL_fk_operator, measuring_point__BWREL_fk_provider, mechanical_pretreatment__BWREL_fk_dataowner, mechanical_pretreatment__BWREL_fk_provider, municipality__BWREL_obj_id, mutation__BWREL_fk_dataowner, mutation__BWREL_fk_provider, organisation__BWREL_fk_dataowner, organisation__BWREL_fk_provider, overflow__BWREL_fk_dataowner, overflow__BWREL_fk_provider, overflow_char__BWREL_fk_dataowner, overflow_char__BWREL_fk_provider, pipe_profile__BWREL_fk_dataowner, pipe_profile__BWREL_fk_provider, private__BWREL_obj_id, profile_geometry__BWREL_fk_dataowner, profile_geometry__BWREL_fk_provider, reach_point__BWREL_fk_dataowner, reach_point__BWREL_fk_provider, retention_body__BWREL_fk_dataowner, retention_body__BWREL_fk_provider, river_bank__BWREL_fk_dataowner, river_bank__BWREL_fk_provider, river_bed__BWREL_fk_dataowner, river_bed__BWREL_fk_provider, sector_water_body__BWREL_fk_dataowner, sector_water_body__BWREL_fk_provider, sludge_treatment__BWREL_fk_dataowner, sludge_treatment__BWREL_fk_provider, structure_part__BWREL_fk_dataowner, structure_part__BWREL_fk_provider, substance__BWREL_fk_dataowner, substance__BWREL_fk_provider, surface_runoff_parameters__BWREL_fk_dataowner, surface_runoff_parameters__BWREL_fk_provider, surface_water_bodies__BWREL_fk_dataowner, surface_water_bodies__BWREL_fk_provider, throttle_shut_off_unit__BWREL_fk_dataowner, throttle_shut_off_unit__BWREL_fk_provider, txt_symbol__BWREL_fk_dataowner, txt_symbol__BWREL_fk_provider, waste_water_association__BWREL_obj_id, waste_water_treatment__BWREL_fk_dataowner, waste_water_treatment__BWREL_fk_provider, waste_water_treatment_plant__BWREL_obj_id, wastewater_networkelement__BWREL_fk_dataowner, wastewater_networkelement__BWREL_fk_provider, wastewater_structure__BWREL_fk_dataowner, wastewater_structure__BWREL_fk_operator, wastewater_structure__BWREL_fk_owner, wastewater_structure__BWREL_fk_provider, wastewater_structure_symbol__BWREL_fk_dataowner, wastewater_structure_symbol__BWREL_fk_provider, water_catchment__BWREL_fk_dataowner, water_catchment__BWREL_fk_provider, water_control_structure__BWREL_fk_dataowner, water_control_structure__BWREL_fk_provider, water_course_segment__BWREL_fk_dataowner, water_course_segment__BWREL_fk_provider, wwtp_energy_use__BWREL_fk_dataowner, wwtp_energy_use__BWREL_fk_provider, zone__BWREL_fk_dataowner, zone__BWREL_fk_provider

        # --- _rel_ ---
        # fk_dataowner__REL, fk_provider__REL

        organisation = ABWASSER.organisation(
            # FIELDS TO MAP TO ABWASSER.organisation

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "organisation"),

            # --- organisation ---
            auid=row.uid,
            bemerkung=row.remark,
            bezeichnung=row.identifier,
        )
        abwasser_session.add(organisation)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    """
    logger.info("Exporting QGEP.channel -> ABWASSER.kanal, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.channel):

        # AVAILABLE FIELDS IN QGEP.channel

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement


        # --- _bwrel_ ---
        # measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id

        # --- _rel_ ---
        # accessibility__REL, bedding_encasement__REL, connection_type__REL, financing__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, function_hierarchic__REL, function_hydraulic__REL, renovation_necessity__REL, rv_construction_type__REL, status__REL, structure_condition__REL, usage_current__REL, usage_planned__REL

        kanal = ABWASSER.kanal(
            # FIELDS TO MAP TO ABWASSER.kanal

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "kanal"),

            # --- abwasserbauwerk ---
            **wastewater_structure_common(row),

            # --- kanal ---
            bettung_umhuellung=get_vl(row.bedding_encasement__REL),
            funktionhierarchisch=get_vl(row.function_hierarchic__REL),
            funktionhydraulisch=get_vl(row.function_hydraulic__REL),
            nutzungsart_geplant=get_vl(row.usage_planned__REL),
            nutzungsart_ist=get_vl(row.usage_current__REL),
            rohrlaenge=row.pipe_length,
            spuelintervall=row.jetting_interval,
            verbindungsart=get_vl(row.connection_type__REL),
        )
        abwasser_session.add(kanal)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.manhole -> ABWASSER.normschacht, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.manhole):
        normschacht = ABWASSER.normschacht(
            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "normschacht"),

            # --- abwasserbauwerk ---
            **wastewater_structure_common(row),

            # --- normschacht ---
            dimension1=row.dimension1,
            dimension2=row.dimension2,
            funktion=get_vl(row.function__REL),
            material=get_vl(row.material__REL),
            oberflaechenzulauf=get_vl(row.surface_inflow__REL),
        )
        abwasser_session.add(normschacht)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.discharge_point -> ABWASSER.einleitstelle, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.discharge_point):
        einleitstelle = ABWASSER.einleitstelle(

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "einleitstelle"),

            # --- abwasserbauwerk ---
            **wastewater_structure_common(row),

            # --- einleitstelle ---
            hochwasserkote=row.highwater_level,
            relevanz=get_vl(row.relevance__REL),
            terrainkote=row.terrain_level,
            wasserspiegel_hydraulik=row.waterlevel_hydraulic,
        )
        abwasser_session.add(einleitstelle)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.special_structure -> ABWASSER.spezialbauwerk, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.special_structure):

        # AVAILABLE FIELDS IN QGEP.special_structure

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- special_structure ---
        # bypass, emergency_spillway, function, obj_id, stormwater_tank_arrangement, upper_elevation

        # --- _bwrel_ ---
        # measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id

        # --- _rel_ ---
        # accessibility__REL, bypass__REL, emergency_spillway__REL, financing__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, function__REL, renovation_necessity__REL, rv_construction_type__REL, status__REL, stormwater_tank_arrangement__REL, structure_condition__REL
        warnings.warn(f'QGEP field special_structure.upper_elevation has no equivalent in the interlis model. It will be ignored.')
        spezialbauwerk = ABWASSER.spezialbauwerk(
            # FIELDS TO MAP TO ABWASSER.spezialbauwerk

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "spezialbauwerk"),

            # --- abwasserbauwerk ---
            **wastewater_structure_common(row),

            # --- spezialbauwerk ---
            # TODO : WARNING : upper_elevation is not mapped
            bypass=get_vl(row.bypass__REL),
            funktion=get_vl(row.function__REL),
            notueberlauf=get_vl(row.emergency_spillway__REL),
            regenbecken_anordnung=get_vl(row.stormwater_tank_arrangement__REL),
        )
        abwasser_session.add(spezialbauwerk)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.infiltration_installation -> ABWASSER.versickerungsanlage, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.infiltration_installation):

        # AVAILABLE FIELDS IN QGEP.infiltration_installation

        # --- wastewater_structure ---
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement

        # --- infiltration_installation ---
        # absorption_capacity, defects, dimension1, dimension2, distance_to_aquifer, effective_area, emergency_spillway, fk_aquifier, kind, labeling, obj_id, seepage_utilization, upper_elevation, vehicle_access, watertightness

        # --- _bwrel_ ---
        # measuring_point__BWREL_fk_wastewater_structure, mechanical_pretreatment__BWREL_fk_infiltration_installation, mechanical_pretreatment__BWREL_fk_wastewater_structure, re_maintenance_event_wastewater_structure__BWREL_fk_wastewater_structure, retention_body__BWREL_fk_infiltration_installation, structure_part__BWREL_fk_wastewater_structure, txt_symbol__BWREL_fk_wastewater_structure, txt_text__BWREL_fk_wastewater_structure, wastewater_networkelement__BWREL_fk_wastewater_structure, wastewater_structure_symbol__BWREL_fk_wastewater_structure, wastewater_structure_text__BWREL_fk_wastewater_structure, wwtp_structure_kind__BWREL_obj_id

        # --- _rel_ ---
        # accessibility__REL, defects__REL, emergency_spillway__REL, financing__REL, fk_aquifier__REL, fk_dataowner__REL, fk_main_cover__REL, fk_main_wastewater_node__REL, fk_operator__REL, fk_owner__REL, fk_provider__REL, kind__REL, labeling__REL, renovation_necessity__REL, rv_construction_type__REL, seepage_utilization__REL, status__REL, structure_condition__REL, vehicle_access__REL, watertightness__REL

        warnings.warn(f'QGEP field infiltration_installation.upper_elevation has no equivalent in the interlis model. It will be ignored.')
        versickerungsanlage = ABWASSER.versickerungsanlage(
            # FIELDS TO MAP TO ABWASSER.versickerungsanlage

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "versickerungsanlage"),

            # --- abwasserbauwerk ---
            **wastewater_structure_common(row),

            # --- versickerungsanlage ---
            # TODO : NOT MAPPED : upper_elevation
            art=get_vl(row.kind__REL),
            beschriftung=get_vl(row.labeling__REL),
            dimension1=row.dimension1,
            dimension2=row.dimension2,
            gwdistanz=row.distance_to_aquifer,
            maengel=get_vl(row.defects__REL),
            notueberlauf=get_vl(row.emergency_spillway__REL),
            saugwagen=get_vl(row.vehicle_access__REL),  # TODO : check mapping
            schluckvermoegen=row.absorption_capacity,  # TODO : check mapping
            versickerungswasser=get_vl(row.seepage_utilization__REL),  # TODO : check mapping
            wasserdichtheit=get_vl(row.watertightness__REL),
            wirksameflaeche=row.effective_area,
        )
        abwasser_session.add(versickerungsanlage)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.pipe_profile -> ABWASSER.rohrprofil, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.pipe_profile):

        # AVAILABLE FIELDS IN QGEP.pipe_profile

        # --- pipe_profile ---
        # fk_dataowner, fk_provider, height_width_ratio, identifier, last_modification, obj_id, profile_type, remark

        # --- _bwrel_ ---
        # profile_geometry__BWREL_fk_pipe_profile, reach__BWREL_fk_pipe_profile

        # --- _rel_ ---
        # fk_dataowner__REL, fk_provider__REL, profile_type__REL

        rohrprofil = ABWASSER.rohrprofil(
            # FIELDS TO MAP TO ABWASSER.rohrprofil

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "rohrprofil"),

            # --- rohrprofil ---
            bemerkung=row.remark,
            bezeichnung=row.identifier,
            hoehenbreitenverhaeltnis=row.height_width_ratio,
            profiltyp=get_vl(row.profile_type__REL),
        )
        abwasser_session.add(rohrprofil)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.reach_point -> ABWASSER.haltungspunkt, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.reach_point):

        # AVAILABLE FIELDS IN QGEP.reach_point

        # --- reach_point ---
        # elevation_accuracy, fk_dataowner, fk_provider, fk_wastewater_networkelement, identifier, last_modification, level, obj_id, outlet_shape, position_of_connection, remark, situation_geometry

        # --- _bwrel_ ---
        # examination__BWREL_fk_reach_point, reach__BWREL_fk_reach_point_from, reach__BWREL_fk_reach_point_to

        # --- _rel_ ---
        # elevation_accuracy__REL, fk_dataowner__REL, fk_provider__REL, fk_wastewater_networkelement__REL, outlet_shape__REL

        haltungspunkt = ABWASSER.haltungspunkt(
            # FIELDS TO MAP TO ABWASSER.haltungspunkt

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "haltungspunkt"),

            # --- haltungspunkt ---
            abwassernetzelementref=get_tid(row.fk_wastewater_networkelement__REL),
            auslaufform=get_vl(row.outlet_shape__REL),
            bemerkung=row.remark,
            bezeichnung=row.identifier,
            hoehengenauigkeit=get_vl(row.elevation_accuracy__REL),
            kote=row.level,
            lage=ST_Force2D(row.situation_geometry),
            lage_anschluss=row.position_of_connection,
        )
        abwasser_session.add(haltungspunkt)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.wastewater_node -> ABWASSER.abwasserknoten, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.wastewater_node):

        # AVAILABLE FIELDS IN QGEP.wastewater_node

        # --- wastewater_networkelement ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark

        # --- wastewater_node ---

        # --- _bwrel_ ---
        # catchment_area__BWREL_fk_wastewater_networkelement_rw_current, catchment_area__BWREL_fk_wastewater_networkelement_rw_planned, catchment_area__BWREL_fk_wastewater_networkelement_ww_current, catchment_area__BWREL_fk_wastewater_networkelement_ww_planned, connection_object__BWREL_fk_wastewater_networkelement, hydraulic_char_data__BWREL_fk_wastewater_node, overflow__BWREL_fk_overflow_to, overflow__BWREL_fk_wastewater_node, reach_point__BWREL_fk_wastewater_networkelement, throttle_shut_off_unit__BWREL_fk_wastewater_node, wastewater_structure__BWREL_fk_main_wastewater_node

        # --- _rel_ ---
        # fk_dataowner__REL, fk_hydr_geometry__REL, fk_provider__REL, fk_wastewater_structure__REL

        warnings.warn(f'QGEP field wastewater_node.fk_hydr_geometry has no equivalent in the interlis model. It will be ignored.')
        abwasserknoten = ABWASSER.abwasserknoten(
            # FIELDS TO MAP TO ABWASSER.abwasserknoten

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "abwasserknoten"),

            # --- abwassernetzelement ---
            **wastewater_network_element_common(row),

            # --- abwasserknoten ---
            # TODO : WARNING : fk_hydr_geometry is not mapped
            lage=ST_Force2D(row.situation_geometry),
            rueckstaukote=row.backflow_level,
            sohlenkote=row.bottom_level,
        )
        abwasser_session.add(abwasserknoten)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.reach -> ABWASSER.haltung, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.reach):

        # AVAILABLE FIELDS IN QGEP.reach

        # --- wastewater_networkelement ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark

        # --- reach ---
        # clear_height, coefficient_of_friction, elevation_determination, fk_pipe_profile, fk_reach_point_from, fk_reach_point_to, horizontal_positioning, inside_coating, length_effective, material, obj_id, progression_geometry, reliner_material, reliner_nominal_size, relining_construction, relining_kind, ring_stiffness, slope_building_plan, wall_roughness

        # --- _bwrel_ ---
        # catchment_area__BWREL_fk_wastewater_networkelement_rw_current, catchment_area__BWREL_fk_wastewater_networkelement_rw_planned, catchment_area__BWREL_fk_wastewater_networkelement_ww_current, catchment_area__BWREL_fk_wastewater_networkelement_ww_planned, connection_object__BWREL_fk_wastewater_networkelement, reach_point__BWREL_fk_wastewater_networkelement, reach_text__BWREL_fk_reach, txt_text__BWREL_fk_reach

        # --- _rel_ ---
        # elevation_determination__REL, fk_dataowner__REL, fk_pipe_profile__REL, fk_provider__REL, fk_reach_point_from__REL, fk_reach_point_to__REL, fk_wastewater_structure__REL, horizontal_positioning__REL, inside_coating__REL, material__REL, reliner_material__REL, relining_construction__REL, relining_kind__REL

        warnings.warn(f'QGEP field reach.elevation_determination has no equivalent in the interlis model. It will be ignored.')
        haltung = ABWASSER.haltung(
            # FIELDS TO MAP TO ABWASSER.haltung

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "haltung"),
            # --- abwassernetzelement ---
            **wastewater_network_element_common(row),

            # --- haltung ---
            # NOT MAPPED : elevation_determination
            innenschutz=get_vl(row.inside_coating__REL),
            laengeeffektiv=row.length_effective,
            lagebestimmung=get_vl(row.horizontal_positioning__REL),
            lichte_hoehe=row.clear_height,
            material=row.material,
            nachhaltungspunktref=get_tid(row.fk_reach_point_to__REL),
            plangefaelle=row.slope_building_plan,  # TODO : check, does this need conversion ?
            reibungsbeiwert=row.coefficient_of_friction,
            reliner_art=row.relining_kind,
            reliner_bautechnik=row.relining_construction,
            reliner_material=get_vl(row.reliner_material__REL),
            reliner_nennweite=row.reliner_nominal_size,
            ringsteifigkeit=row.ring_stiffness,
            rohrprofilref=get_tid(row.fk_pipe_profile__REL),
            verlauf=ST_Force2D(row.progression_geometry),
            vonhaltungspunktref=get_tid(row.fk_reach_point_from__REL),
            wandrauhigkeit=row.wall_roughness,
        )
        abwasser_session.add(haltung)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.dryweather_downspout -> ABWASSER.trockenwetterfallrohr, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.dryweather_downspout):

        # AVAILABLE FIELDS IN QGEP.dryweather_downspout

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- dryweather_downspout ---
        # diameter, obj_id

        # --- _bwrel_ ---
        # access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id

        # --- _rel_ ---
        # fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, renovation_demand__REL

        trockenwetterfallrohr = ABWASSER.trockenwetterfallrohr(
            # FIELDS TO MAP TO ABWASSER.trockenwetterfallrohr

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "trockenwetterfallrohr"),

            # --- bauwerksteil ---
            **structure_part_common(row),

            # --- trockenwetterfallrohr ---
            durchmesser=row.diameter,
        )
        abwasser_session.add(trockenwetterfallrohr)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.access_aid -> ABWASSER.einstiegshilfe, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.access_aid):

        # AVAILABLE FIELDS IN QGEP.access_aid

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- access_aid ---
        # kind, obj_id

        # --- _bwrel_ ---
        # access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id

        # --- _rel_ ---
        # fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, kind__REL, renovation_demand__REL

        einstiegshilfe = ABWASSER.einstiegshilfe(
            # FIELDS TO MAP TO ABWASSER.einstiegshilfe

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "einstiegshilfe"),

            # --- bauwerksteil ---
            **structure_part_common(row),

            # --- einstiegshilfe ---
            art=get_vl(row.kind__REL),
        )
        abwasser_session.add(einstiegshilfe)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.dryweather_flume -> ABWASSER.trockenwetterrinne, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.dryweather_flume):

        # AVAILABLE FIELDS IN QGEP.dryweather_flume

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- dryweather_flume ---
        # material, obj_id

        # --- _bwrel_ ---
        # access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id

        # --- _rel_ ---
        # fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, material__REL, renovation_demand__REL

        trockenwetterrinne = ABWASSER.trockenwetterrinne(
            # FIELDS TO MAP TO ABWASSER.trockenwetterrinne

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "trockenwetterrinne"),

            # --- bauwerksteil ---
            **structure_part_common(row),

            # --- trockenwetterrinne ---
            material=get_vl(row.material__REL),
        )
        abwasser_session.add(trockenwetterrinne)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.cover -> ABWASSER.deckel, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.cover):

        # AVAILABLE FIELDS IN QGEP.cover

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- cover ---
        # brand, cover_shape, diameter, fastening, level, material, obj_id, positional_accuracy, situation_geometry, sludge_bucket, venting

        # --- _bwrel_ ---
        # access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id, wastewater_structure__BWREL_fk_main_cover

        # --- _rel_ ---
        # cover_shape__REL, fastening__REL, fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, material__REL, positional_accuracy__REL, renovation_demand__REL, sludge_bucket__REL, venting__REL

        deckel = ABWASSER.deckel(
            # FIELDS TO MAP TO ABWASSER.deckel

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "deckel"),

            # --- bauwerksteil ---
            **structure_part_common(row),

            # --- deckel ---
            deckelform=get_vl(row.cover_shape__REL),
            durchmesser=row.diameter,
            entlueftung=get_vl(row.venting__REL),
            fabrikat=row.brand,
            kote=row.level,
            lage=ST_Force2D(row.situation_geometry),
            lagegenauigkeit=get_vl(row.positional_accuracy__REL),
            material=get_vl(row.material__REL),
            schlammeimer=get_vl(row.sludge_bucket__REL),
            verschluss=get_vl(row.fastening__REL),
        )
        abwasser_session.add(deckel)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.benching -> ABWASSER.bankett, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.benching):

        # AVAILABLE FIELDS IN QGEP.benching

        # --- structure_part ---
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark, renovation_demand

        # --- benching ---
        # kind, obj_id

        # --- _bwrel_ ---
        # access_aid_kind__BWREL_obj_id, backflow_prevention__BWREL_obj_id, benching_kind__BWREL_obj_id, dryweather_flume_material__BWREL_obj_id, electric_equipment__BWREL_obj_id, electromechanical_equipment__BWREL_obj_id, solids_retention__BWREL_obj_id, tank_cleaning__BWREL_obj_id, tank_emptying__BWREL_obj_id

        # --- _rel_ ---
        # fk_dataowner__REL, fk_provider__REL, fk_wastewater_structure__REL, kind__REL, renovation_demand__REL

        bankett = ABWASSER.bankett(
            # FIELDS TO MAP TO ABWASSER.bankett

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "bankett"),

            # --- sia405_baseclass ---
            obj_id=row.obj_id,

            # --- bauwerksteil ---
            **structure_part_common(row),

            # --- bankett ---
            art=get_vl(row.kind__REL),
        )
        abwasser_session.add(bankett)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.examination -> ABWASSER.untersuchung, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.examination):

        # AVAILABLE FIELDS IN QGEP.examination

        # --- maintenance_event ---
        # --- examination ---
        # equipment, fk_reach_point, from_point_identifier, inspected_length, obj_id, recording_type, to_point_identifier, vehicle, videonumber, weather

        # --- _bwrel_ ---
        # damage__BWREL_fk_examination, re_maintenance_event_wastewater_structure__BWREL_fk_maintenance_event

        # --- _rel_ ---
        # fk_dataowner__REL, fk_operating_company__REL, fk_provider__REL, fk_reach_point__REL, kind__REL, recording_type__REL, status__REL, weather__REL
        warnings.warn(f'QGEP field maintenance_event.active_zone has no equivalent in the interlis model. It will be ignored.')

        untersuchung = ABWASSER.untersuchung(
            # FIELDS TO MAP TO ABWASSER.untersuchung

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "untersuchung"),

            # --- erhaltungsereignis ---
            # abwasserbauwerkref=row.REPLACE_ME,  # TODO : convert this to M2N relation through re_maintenance_event_wastewater_structure
            art=row.kind,
            astatus=row.status,
            ausfuehrende_firmaref=get_tid(row.fk_operating_company__REL),
            ausfuehrender=row.operator,
            bemerkung=row.remark,
            bezeichnung=row.identifier,
            datengrundlage=row.base_data,
            dauer=row.duration,
            detaildaten=row.data_details,
            ergebnis=row.result,
            grund=row.reason,
            kosten=row.cost,
            zeitpunkt=row.time_point,

            # --- untersuchung ---
            bispunktbezeichnung=row.to_point_identifier,
            erfassungsart=row.recording_type,
            fahrzeug=row.vehicle,
            geraet=row.equipment,
            haltungspunktref=get_tid(row.fk_reach_point__REL),
            inspizierte_laenge=row.inspected_length,
            videonummer=row.videonumber,
            vonpunktbezeichnung=row.from_point_identifier,
            witterung=row.weather,
        )
        abwasser_session.add(untersuchung)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.damage_manhole -> ABWASSER.normschachtschaden, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.damage_manhole):

        # AVAILABLE FIELDS IN QGEP.damage_manhole

        # --- damage ---

        # --- damage_manhole ---
        # manhole_damage_code, manhole_shaft_area, obj_id

        # --- _bwrel_ ---
        # damage_channel_channel_damage_code__BWREL_obj_id

        # --- _rel_ ---
        # connection__REL, fk_dataowner__REL, fk_examination__REL, fk_provider__REL, manhole_damage_code__REL, manhole_shaft_area__REL, single_damage_class__REL

        normschachtschaden = ABWASSER.normschachtschaden(
            # FIELDS TO MAP TO ABWASSER.normschachtschaden

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "normschachtschaden"),

            # --- schaden ---
            anmerkung=row.comments,
            ansichtsparameter=row.view_parameters,
            einzelschadenklasse=get_vl(row.single_damage_class__REL),
            streckenschaden=row.damage_reach,
            untersuchungref=get_tid(row.fk_examination__REL),
            verbindung=get_vl(row.connection__REL),
            videozaehlerstand=row.video_counter,

            # --- normschachtschaden ---
            distanz=row.distance,
            quantifizierung1=row.quantification1,
            quantifizierung2=row.quantification2,
            schachtbereich=get_vl(row.manhole_shaft_area__REL),
            schachtschadencode=get_vl(row.manhole_damage_code__REL),
            schadenlageanfang=row.damage_begin,
            schadenlageende=row.damage_end,
        )
        abwasser_session.add(normschachtschaden)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.damage_channel -> ABWASSER.kanalschaden, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.damage_channel):

        # AVAILABLE FIELDS IN QGEP.damage_channel

        # --- damage ---
        # comments, connection, damage_begin, damage_end, damage_reach, distance, fk_dataowner, fk_examination, fk_provider, last_modification, quantification1, quantification2, single_damage_class, video_counter, view_parameters

        # --- damage_channel ---
        # , obj_id

        # --- _bwrel_ ---
        # damage_channel_channel_damage_code__BWREL_obj_id

        # --- _rel_ ---
        # channel_damage_code__REL, connection__REL, fk_dataowner__REL, fk_examination__REL, fk_provider__REL, single_damage_class__REL

        kanalschaden = ABWASSER.kanalschaden(
            # FIELDS TO MAP TO ABWASSER.kanalschaden

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "kanalschaden"),

            # --- schaden ---
            anmerkung=row.comments,
            ansichtsparameter=row.view_parameters,
            einzelschadenklasse=get_vl(row.single_damage_class__REL),
            streckenschaden=row.damage_reach,
            untersuchungref=get_tid(row.fk_examination__REL),
            verbindung=get_vl(row.connection__REL),
            videozaehlerstand=row.video_counter,

            # --- kanalschaden ---
            distanz=row.distance,
            kanalschadencode=get_vl(row.channel_damage_code__REL),
            quantifizierung1=row.quantification1,
            quantifizierung2=row.quantification2,
            schadenlageanfang=row.damage_begin,
            schadenlageende=row.damage_end,
        )
        abwasser_session.add(kanalschaden)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.data_media -> ABWASSER.datentraeger, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.data_media):

        # AVAILABLE FIELDS IN QGEP.data_media

        # --- data_media ---
        # fk_dataowner, fk_provider, identifier, kind, last_modification, location, obj_id, path, remark

        # --- _rel_ ---
        # fk_dataowner__REL, fk_provider__REL, kind__REL

        datentraeger = ABWASSER.datentraeger(
            # FIELDS TO MAP TO ABWASSER.datentraeger

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "datentraeger"),

            # --- datentraeger ---
            art=row.kind,
            bemerkung=row.remark,
            bezeichnung=row.identifier,
            pfad=row.path,
            standort=row.location,
        )
        abwasser_session.add(datentraeger)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()

    logger.info("Exporting QGEP.file -> ABWASSER.datei, ABWASSER.metaattribute")
    for row in qgep_session.query(QGEP.file):

        # AVAILABLE FIELDS IN QGEP.file

        # --- file ---
        # class, fk_data_media, fk_dataowner, fk_provider, identifier, kind, last_modification, obj_id, object, path_relative, remark

        # --- _rel_ ---
        # class__REL, fk_dataowner__REL, fk_provider__REL, kind__REL

        # NOTE: QGEP misses a FK to data_media, so we inject it manually here
        row.data_media__REL = qgep_session.query(QGEP.data_media).get(row.fk_data_media)

        datei = ABWASSER.datei(
            # FIELDS TO MAP TO ABWASSER.datei

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "datei"),

            # --- datei ---
            art=get_vl(row.kind__REL) or '???',
            bemerkung=row.remark,
            bezeichnung=row.identifier,
            datentraegerref=get_tid(row.data_media__REL),
            klasse=getattr(row, "class"),  # class is a python keyword, this is equivalent to `klasse=row.class`,
            objekt=row.object,
            relativpfad=row.path_relative,
        )
        abwasser_session.add(datei)
        create_metaattributes(row)
        print(".", end="")
    logger.info("done")
    abwasser_session.flush()
    """

    abwasser_session.commit()

    qgep_session.close()
    abwasser_session.close()
