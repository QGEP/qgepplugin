from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from .. import utils

from .model_qwat import QWAT
from .model_wasser import WASSER


def export():

    qwat_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    wasser_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    tid_maker = utils.ili2db.TidMaker(id_attribute='obj_id')

    def create_metaattributes(row, session):
        metaattribute = WASSER.metaattribute(
            # FIELDS TO MAP TO WASSER.metaattribute
            # --- metaattribute ---
            # datenherr=row.REPLACE_ME,
            # datenlieferant=row.REPLACE_ME,
            # letzte_aenderung=row.REPLACE_ME,
            # sia405_baseclass_metaattribute=row.REPLACE_ME,
            # t_id=row.REPLACE_ME
            # t_seq=row.REPLACE_ME,
        )
        session.add(metaattribute)

    print("Exporting QWAT.node -> WASSER.hydraulischer_knoten")
    for row in qwat_session.query(QWAT.node):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, id, update_geometry_alt1, update_geometry_alt2
        # _bwrel_ --- pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b
        # _rel_ --- fk_district__REL, fk_pressurezone__REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- hydraulischer_knoten ---
            # bemerkung=row.REPLACE_ME,
            # druck=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # knotentyp=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # verbrauch=row.REPLACE_ME,
        )
        wasser_session.add(hydraulischer_knoten)
        print(".", end="")
    print("done")

    print("Exporting QWAT.hydrant -> WASSER.hydrant")
    for row in qwat_session.query(QWAT.hydrant):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2
        # network_element --- altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end
        # hydrant --- fk_material, fk_model_inf, fk_model_sup, fk_output, fk_provider, flow, id, marked, observation_date, observation_source, pressure_dynamic, pressure_static, underground
        # _bwrel_ --- meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, samplingpoint__BWREL_id
        # _rel_ --- fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_material__REL, fk_model_inf__REL, fk_model_sup__REL, fk_object_reference__REL, fk_output__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_provider__REL, fk_status__REL, label_1_visible__REL, label_2_visible__REL

        hydrant = WASSER.hydrant(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- hydrant ---
            # art=row.REPLACE_ME,
            # dimension=row.REPLACE_ME,
            # entnahme=row.REPLACE_ME,
            # fliessdruck=row.REPLACE_ME,
            # hersteller=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # typ=row.REPLACE_ME,
            # versorgungsdruck=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(hydrant)
        print(".", end="")
    print("done")

    print("Exporting QWAT.tank -> WASSER.wasserbehaelter")
    for row in qwat_session.query(QWAT.tank):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2
        # network_element --- altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end
        # installation --- eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel
        # tank --- _cistern1_litrepercm, _cistern2_litrepercm, _litrepercm, altitude_apron, altitude_overflow, cistern1_dimension_1, cistern1_dimension_2, cistern1_fk_type, cistern1_storage, cistern2_dimension_1, cistern2_dimension_2, cistern2_fk_type, cistern2_storage, fire_remote, fire_valve, fk_overflow, fk_tank_firestorage, height_max, id, storage_fire, storage_supply, storage_total
        # _bwrel_ --- cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id
        # _rel_ --- cistern1_fk_type__REL, cistern2_fk_type__REL, fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_overflow__REL, fk_parent__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_remote__REL, fk_status__REL, fk_tank_firestorage__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        wasserbehaelter = WASSER.wasserbehaelter(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- wasserbehaelter ---
            # art=row.REPLACE_ME,
            # beschichtung=row.REPLACE_ME,
            # brauchwasserreserve=row.REPLACE_ME,
            # fassungsvermoegen=row.REPLACE_ME,
            # leistung=row.REPLACE_ME,
            # loeschwasserreserve=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # ueberlaufhoehe=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(wasserbehaelter)
        print(".", end="")
    print("done")

    print("Exporting QWAT.pump -> WASSER.foerderanlage")
    for row in qwat_session.query(QWAT.pump):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2
        # network_element --- altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end
        # installation --- eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel
        # pump --- fk_pipe_in, fk_pipe_out, fk_pump_operating, fk_pump_type, id, manometric_height, no_pumps, rejected_flow
        # _bwrel_ --- cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id
        # _rel_ --- fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_parent__REL, fk_pipe_in__REL, fk_pipe_out__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_pump_operating__REL, fk_pump_type__REL, fk_remote__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        foerderanlage = WASSER.foerderanlage(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- foerderanlage ---
            # art=row.REPLACE_ME,
            # leistung=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(foerderanlage)
        print(".", end="")
    print("done")

    print("Exporting QWAT.treatment -> WASSER.anlage")
    for row in qwat_session.query(QWAT.treatment):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2
        # network_element --- altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end
        # installation --- eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel
        # treatment --- activatedcharcoal, filtration_membrane, filtration_sandorgravel, flocculation, id, sanitization_chlorine_gas, sanitization_chlorine_liquid, sanitization_ozone, sanitization_uv, settling, treatment_capacity
        # _bwrel_ --- cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id
        # _rel_ --- fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_parent__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_remote__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        anlage = WASSER.anlage(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- anlage ---
            # art=row.REPLACE_ME,
            # betreiber=row.REPLACE_ME,
            # dimension1=row.REPLACE_ME,
            # konzessionaer=row.REPLACE_ME,
            # leistung=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # unterhaltspflichtiger=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(anlage)
        print(".", end="")
    print("done")

    print("Exporting QWAT.subscriber -> WASSER.hausanschluss")
    for row in qwat_session.query(QWAT.subscriber):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2
        # network_element --- altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end
        # subscriber --- fk_pipe, fk_subscriber_type, flow_current, flow_planned, id, parcel
        # _bwrel_ --- meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, samplingpoint__BWREL_id, subscriber_reference__BWREL_fk_subscriber
        # _rel_ --- fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_pipe__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_status__REL, fk_subscriber_type__REL, label_1_visible__REL, label_2_visible__REL

        hausanschluss = WASSER.hausanschluss(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- hausanschluss ---
            # art=row.REPLACE_ME,
            # dimension=row.REPLACE_ME,
            # gebaeudeanschluss=row.REPLACE_ME,
            # isolierstueck=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # standort=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # typ=row.REPLACE_ME,
            # verbrauch=row.REPLACE_ME,
            # zuordnung_hydraulischer_knoten=row.REPLACE_ME,
            # zuordnung_hydraulischer_strang=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(hausanschluss)
        print(".", end="")
    print("done")

    print("Exporting QWAT.source -> WASSER.wassergewinnungsanlage")
    for row in qwat_session.query(QWAT.source):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2
        # network_element --- altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end
        # installation --- eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel
        # source --- contract_end, fk_source_quality, fk_source_type, flow_average, flow_concession, flow_lowest, gathering_chamber, id
        # _bwrel_ --- cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id
        # _rel_ --- fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_parent__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_remote__REL, fk_source_quality__REL, fk_source_type__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        wassergewinnungsanlage = WASSER.wassergewinnungsanlage(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- wassergewinnungsanlage ---
            # art=row.REPLACE_ME,
            # betreiber=row.REPLACE_ME,
            # konzessionaer=row.REPLACE_ME,
            # leistung=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # unterhaltspflichtiger=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(wassergewinnungsanlage)
        print(".", end="")
    print("done")

    print("Exporting QWAT.chamber -> WASSER.absperrorgan")
    for row in qwat_session.query(QWAT.chamber):

        # node --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2
        # network_element --- altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end
        # installation --- eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel
        # chamber --- depth, flow_meter, id, manometer, networkseparation, no_valves, water_meter
        # _bwrel_ --- cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id
        # _rel_ --- fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_parent__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_remote__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        absperrorgan = WASSER.absperrorgan(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- absperrorgan ---
            # art=row.REPLACE_ME,
            # hersteller=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # nennweite=row.REPLACE_ME,
            # schaltantrieb=row.REPLACE_ME,
            # schaltzustand=row.REPLACE_ME,
            # schliessrichtung=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # typ=row.REPLACE_ME,
            # zulaessiger_bauteil_betriebsdruck=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(absperrorgan)
        print(".", end="")
    print("done")

    print("Exporting QWAT.valve -> WASSER.absperrorgan")
    for row in qwat_session.query(QWAT.valve):

        # valve --- _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, _schema_visible, altitude, closed, fk_distributor, fk_district, fk_folder, fk_handle_precision, fk_handle_precisionalti, fk_locationtype, fk_maintenance, fk_nominal_diameter, fk_object_reference, fk_pipe, fk_precision, fk_precisionalti, fk_pressurezone, fk_printmap, fk_status, fk_valve_actuation, fk_valve_function, fk_valve_type, geometry, geometry_alt1, geometry_alt2, handle_altitude, handle_geometry, id, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, networkseparation, orientation, remark, schema_force_visible, update_geometry_alt1, update_geometry_alt2, year, year_end
        # _rel_ --- fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_handle_precision__REL, fk_handle_precisionalti__REL, fk_nominal_diameter__REL, fk_object_reference__REL, fk_pipe__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_status__REL, fk_valve_actuation__REL, fk_valve_function__REL, fk_valve_type__REL, label_1_visible__REL, label_2_visible__REL, schema_force_visible__REL

        absperrorgan = WASSER.absperrorgan(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            # knotenref=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # symbolori=row.REPLACE_ME,

            # --- absperrorgan ---
            # art=row.REPLACE_ME,
            # hersteller=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # nennweite=row.REPLACE_ME,
            # schaltantrieb=row.REPLACE_ME,
            # schaltzustand=row.REPLACE_ME,
            # schliessrichtung=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # typ=row.REPLACE_ME,
            # zulaessiger_bauteil_betriebsdruck=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(absperrorgan)
        print(".", end="")
    print("done")

    print("Exporting QWAT.pipe -> WASSER.hydraulischer_strang, WASSER.leitung")
    for row in qwat_session.query(QWAT.pipe):

        # pipe --- _diff_elevation, _geometry_alt1_used, _geometry_alt2_used, _length2d, _length3d, _printmaps, _schema_visible, _valve_closed, _valve_count, fk_bedding, fk_distributor, fk_district, fk_folder, fk_function, fk_installmethod, fk_locationtype, fk_material, fk_node_a, fk_node_b, fk_parent, fk_precision, fk_pressurezone, fk_printmap, fk_protection, fk_status, fk_watertype, geometry, geometry_alt1, geometry_alt2, id, label_1_text, label_1_visible, label_2_text, label_2_visible, pressure_nominal, remark, schema_force_visible, tunnel_or_bridge, update_geometry_alt1, update_geometry_alt2, year, year_end, year_rehabilitation
        # _bwrel_ --- crossing__BWREL__pipe1_id, crossing__BWREL__pipe2_id, leak__BWREL_fk_pipe, meter__BWREL_fk_pipe, part__BWREL_fk_pipe, pipe__BWREL_fk_parent, pump__BWREL_fk_pipe_in, pump__BWREL_fk_pipe_out, subscriber__BWREL_fk_pipe, valve__BWREL_fk_pipe
        # _rel_ --- fk_bedding__REL, fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_function__REL, fk_installmethod__REL, fk_material__REL, fk_node_a__REL, fk_node_b__REL, fk_parent__REL, fk_precision__REL, fk_pressurezone__REL, fk_protection__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL, schema_force_visible__REL

        hydraulischer_strang = WASSER.hydraulischer_strang(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- hydraulischer_strang ---
            # bemerkung=row.REPLACE_ME,
            # bisknotenref=row.REPLACE_ME,
            # durchfluss=row.REPLACE_ME,
            # fliessgeschwindigkeit=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # referenz_durchmesser=row.REPLACE_ME,
            # referenz_laenge=row.REPLACE_ME,
            # referenz_rauheit=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # verbrauch=row.REPLACE_ME,
            # vonknotenref=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(hydraulischer_strang)
        leitung = WASSER.leitung(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- leitung ---
            # astatus=row.REPLACE_ME,
            # aussenbeschichtung=row.REPLACE_ME,
            # baujahr=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # betreiber=row.REPLACE_ME,
            # betriebsdruck=row.REPLACE_ME,
            # bettung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # durchmesser=row.REPLACE_ME,
            # durchmesseraussen=row.REPLACE_ME,
            # durchmesserinnen=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # funktion=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hydraulische_rauheit=row.REPLACE_ME,
            # innenbeschichtung=row.REPLACE_ME,
            # kathodischer_schutz=row.REPLACE_ME,
            # konzessionaer=row.REPLACE_ME,
            # laenge=row.REPLACE_ME,
            # lagebestimmung=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # nennweite=row.REPLACE_ME,
            # sanierung_erneuerung=row.REPLACE_ME,
            # schubsicherung=row.REPLACE_ME,
            # strangref=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # ueberdeckung=row.REPLACE_ME,
            # unterhalt=row.REPLACE_ME,
            # unterhaltspflichtiger=row.REPLACE_ME,
            # verbindungsart=row.REPLACE_ME,
            # verlegeart=row.REPLACE_ME,
            # wasserqualitaet=row.REPLACE_ME,
            # zulaessiger_bauteil_betriebsdruck=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(leitung)
        print(".", end="")
    print("done")

    print("Exporting QWAT.leak -> WASSER.schadenstelle")
    for row in qwat_session.query(QWAT.leak):

        # leak --- _repaired, address, description, detection_date, fk_cause, fk_pipe, geometry, id, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, pipe_replaced, repair, repair_date, widespread_damage
        # _rel_ --- fk_cause__REL, fk_pipe__REL, label_1_visible__REL, label_2_visible__REL

        schadenstelle = WASSER.schadenstelle(

            # --- baseclass ---
            # t_ili_tid=row.REPLACE_ME,
            # t_type=row.REPLACE_ME,

            # --- sia405_baseclass ---
            # obj_id=row.REPLACE_ME,

            # --- schadenstelle ---
            # art=row.REPLACE_ME,
            # ausloeser=row.REPLACE_ME,
            # behebungsdatum=row.REPLACE_ME,
            # bemerkung=row.REPLACE_ME,
            # erhebungsdatum=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # leitungref=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # ursache=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(schadenstelle)
        print(".", end="")
    print("done")

    wasser_session.commit()

    qwat_session.close()
    wasser_session.close()