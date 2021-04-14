import datetime
import warnings

from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D, ST_Z, ST_ForceCurve

from .. import utils

from .model_qwat import get_qwat_model
from .model_wasser import get_wasser_model

from ..utils.various import logger

def qwat_export():

    QWAT = get_qwat_model()
    WASSER = get_wasser_model()

    qwat_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    wasser_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    tid_maker = utils.ili2db.TidMaker(id_attribute='id')

    def get_tid(relation, for_class=None):
        """
        Makes a tid for a relation
        """
        if relation is None:
            return None
        return tid_maker.tid_for_row(relation, for_class=for_class)

    def create_metaattributes(row, for_class=None):
        warnings.warn(f'QWAT doesn\'t define meta attributes. Dummy metaattributes will be created with an arbitrary date.')

        # NOTE : QWAT doesn't define meta attributes, so we create a dummy metattribute
        metaattribute = WASSER.metaattribute(
            # FIELDS TO MAP TO WASSER.metaattribute
            # --- metaattribute ---
            datenherr='unknown',
            datenlieferant='unknown',
            letzte_aenderung=datetime.datetime.min,
            sia405_baseclass_metaattribute=get_tid(row, for_class=for_class),
            # OD : is this OK ? Don't we need a different t_id from what inserted above in organisation ? if so, consider adding a "for_class" arg to tid_for_row
            t_id=get_tid(row, for_class=for_class),
            t_seq=0,
        )
        wasser_session.add(metaattribute)

    def base_common(row, type_name, tid_for_class=None):
        """
        Returns common attributes for base
        """
        return {
            "t_ili_tid": row.id,
            "t_type": type_name,
            "obj_id": row.id,
            "t_id": get_tid(row, tid_for_class),
        }

    def leitungsknoten_common(row):
        """
        Returns common attributes for leitungsknoten
        """
        return {
            # --- leitungsknoten ---
            # "bemerkung": row.REPLACE_ME,
            # "druckzone": row.REPLACE_ME,
            # "eigentuemer": row.REPLACE_ME,
            # "einbaujahr": row.REPLACE_ME,
            "geometrie": ST_Force2D(ST_Transform(row.geometry, 2056)),
            "hoehe": ST_Z(row.geometry),
            # "hoehenbestimmung": row.REPLACE_ME,
            "knotenref": tid_maker.tid_for_row(row, QWAT.node),  # we use the generated hydraulischer_knoten t_id
            "lagebestimmung": "undefined",
            "symbolori": 0,
        }

    print("Exporting QWAT.node -> WASSER.hydraulischer_knoten")
    for row in qwat_session.query(QWAT.node):

        # AVAILABLE FIELDS IN QWAT.node

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, id, update_geometry_alt1, update_geometry_alt2

        # --- _bwrel_ ---
        # pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b

        # --- _rel_ ---
        # fk_district__REL, fk_pressurezone__REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten

            **base_common(row, "hydraulischer_knoten", QWAT.node),

            # --- hydraulischer_knoten ---
            # bemerkung=row.REPLACE_ME,
            # druck=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            knotentyp="Normalknoten",
            name_nummer=str(row.id),
            # verbrauch=row.REPLACE_ME,
        )
        wasser_session.add(hydraulischer_knoten)
        create_metaattributes(row, QWAT.node)
        print(".", end="")
    print("done")
    wasser_session.commit()

    print("Exporting QWAT.hydrant -> WASSER.hydraulischer_knoten, WASSER.hydrant")
    for row in qwat_session.query(QWAT.hydrant):

        # AVAILABLE FIELDS IN QWAT.hydrant

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- hydrant ---
        # fk_material, fk_model_inf, fk_model_sup, fk_output, fk_provider, flow, id, marked, observation_date, observation_source, pressure_dynamic, pressure_static, underground

        # --- _bwrel_ ---
        # meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, samplingpoint__BWREL_id, subscriber__BWREL_id

        # --- _rel_ ---
        # fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_material__REL, fk_model_inf__REL, fk_model_sup__REL, fk_object_reference__REL, fk_output__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_provider__REL, fk_status__REL, label_1_visible__REL, label_2_visible__REL

        hydrant = WASSER.hydrant(
            # FIELDS TO MAP TO WASSER.hydrant

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "hydrant"),

            # --- leitungsknoten ---
            **leitungsknoten_common(row),

            # --- hydrant ---
            # art=row.REPLACE_ME,
            # dimension=row.REPLACE_ME,
            # entnahme=row.REPLACE_ME,
            # fliessdruck=row.REPLACE_ME,
            # hersteller=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # typ=row.REPLACE_ME,
            # versorgungsdruck=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(hydrant)
        create_metaattributes(row)
        print(".", end="")
    print("done")
    wasser_session.commit()

    print("Exporting QWAT.tank -> WASSER.wasserbehaelter")
    for row in qwat_session.query(QWAT.tank):

        # AVAILABLE FIELDS IN QWAT.tank

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- installation ---
        # eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel

        # --- tank ---
        # _cistern1_litrepercm, _cistern2_litrepercm, _litrepercm, altitude_apron, altitude_overflow, cistern1_dimension_1, cistern1_dimension_2, cistern1_fk_type, cistern1_storage, cistern2_dimension_1, cistern2_dimension_2, cistern2_fk_type, cistern2_storage, fire_remote, fire_valve, fk_overflow, fk_tank_firestorage, height_max, id, storage_fire, storage_supply, storage_total

        # --- _bwrel_ ---
        # cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id, source__BWREL_id, subscriber__BWREL_id

        # --- _rel_ ---
        # cistern1_fk_type__REL, cistern2_fk_type__REL, fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_overflow__REL, fk_parent__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_remote__REL, fk_status__REL, fk_tank_firestorage__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        wasserbehaelter = WASSER.wasserbehaelter(
            # FIELDS TO MAP TO WASSER.wasserbehaelter

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "hydrant"),

            # --- leitungsknoten ---
            **leitungsknoten_common(row),

            # --- wasserbehaelter ---
            # art=row.REPLACE_ME,
            # beschichtung=row.REPLACE_ME,
            brauchwasserreserve=0,
            fassungsvermoegen=0,
            # leistung=row.REPLACE_ME,
            loeschwasserreserve=0,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            ueberlaufhoehe=0,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(wasserbehaelter)
        print(".", end="")
    print("done")
    wasser_session.commit()

    print("Exporting QWAT.pump -> WASSER.foerderanlage")
    for row in qwat_session.query(QWAT.pump):

        # AVAILABLE FIELDS IN QWAT.pump

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- installation ---
        # eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel

        # --- pump ---
        # fk_pipe_in, fk_pipe_out, fk_pump_operating, fk_pump_type, id, manometric_height, no_pumps, rejected_flow

        # --- _bwrel_ ---
        # cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id, source__BWREL_id, subscriber__BWREL_id

        # --- _rel_ ---
        # fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_parent__REL, fk_pipe_in__REL, fk_pipe_out__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_pump_operating__REL, fk_pump_type__REL, fk_remote__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        foerderanlage = WASSER.foerderanlage(
            # FIELDS TO MAP TO WASSER.foerderanlage

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "hydrant"),

            # --- leitungsknoten ---
            **leitungsknoten_common(row),

            # --- foerderanlage ---
            # art=row.REPLACE_ME,
            leistung="undefined",
            # name_nummer=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(foerderanlage)
        print(".", end="")
    print("done")
    wasser_session.commit()

    print("Exporting QWAT.treatment -> WASSER.anlage")
    for row in qwat_session.query(QWAT.treatment):

        # AVAILABLE FIELDS IN QWAT.treatment

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- installation ---
        # eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel

        # --- treatment ---
        # activatedcharcoal, filtration_membrane, filtration_sandorgravel, flocculation, id, sanitization_chlorine_gas, sanitization_chlorine_liquid, sanitization_ozone, sanitization_uv, settling, treatment_capacity

        # --- _bwrel_ ---
        # cover__BWREL_fk_installation, installation__BWREL_fk_parent, meter__BWREL_id, pipe__BWREL_fk_node_a, pipe__BWREL_fk_node_b, pressurecontrol_type__BWREL_id, samplingpoint__BWREL_id, source__BWREL_id, subscriber__BWREL_id

        # --- _rel_ ---
        # fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_object_reference__REL, fk_parent__REL, fk_precision__REL, fk_precisionalti__REL, fk_pressurezone__REL, fk_remote__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL

        anlage = WASSER.anlage(
            # FIELDS TO MAP TO WASSER.anlage

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "hydrant"),

            # --- leitungsknoten ---
            **leitungsknoten_common(row),

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
    wasser_session.commit()

    print("Exporting QWAT.subscriber -> WASSER.hausanschluss")
    for row in qwat_session.query(QWAT.subscriber):

        # AVAILABLE FIELDS IN QWAT.subscriber

        # --- subscriber ---
        # fk_pipe, fk_subscriber_type, flow_current, flow_planned, id, parcel

        # --- _bwrel_ ---
        # subscriber_reference__BWREL_fk_subscriber

        # --- _rel_ ---
        # fk_pipe__REL, fk_subscriber_type__REL, id__REL

        hausanschluss = WASSER.hausanschluss(
            # FIELDS TO MAP TO WASSER.hausanschluss

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "hydrant"),

            # --- leitungsknoten ---
            **leitungsknoten_common(row),

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
            zuordnung_hydraulischer_knoten="undefined",
            zuordnung_hydraulischer_strang="undefined",
            # zustand=row.REPLACE_ME,
        )
        wasser_session.add(hausanschluss)
        print(".", end="")
    print("done")
    wasser_session.commit()


    print("Exporting QWAT.pipe -> WASSER.leitung")
    for row in qwat_session.query(QWAT.pipe):

        # AVAILABLE FIELDS IN QWAT.pipe

        # --- pipe ---
        # _diff_elevation, _geometry_alt1_used, _geometry_alt2_used, _length2d, _length3d, _printmaps, _schema_visible, _valve_closed, _valve_count, fk_bedding, fk_distributor, fk_district, fk_folder, fk_function, fk_installmethod, fk_locationtype, fk_material, fk_node_a, fk_node_b, fk_parent, fk_precision, fk_pressurezone, fk_printmap, fk_protection, fk_status, fk_watertype, geometry, geometry_alt1, geometry_alt2, id, label_1_text, label_1_visible, label_2_text, label_2_visible, pressure_nominal, remark, schema_force_visible, tunnel_or_bridge, update_geometry_alt1, update_geometry_alt2, year, year_end, year_rehabilitation

        # --- _bwrel_ ---
        # crossing__BWREL__pipe1_id, crossing__BWREL__pipe2_id, leak__BWREL_fk_pipe, meter__BWREL_fk_pipe, part__BWREL_fk_pipe, pipe__BWREL_fk_parent, pump__BWREL_fk_pipe_in, pump__BWREL_fk_pipe_out, subscriber__BWREL_fk_pipe, valve__BWREL_fk_pipe

        # --- _rel_ ---
        # fk_bedding__REL, fk_distributor__REL, fk_district__REL, fk_folder__REL, fk_function__REL, fk_installmethod__REL, fk_material__REL, fk_node_a__REL, fk_node_b__REL, fk_parent__REL, fk_precision__REL, fk_pressurezone__REL, fk_protection__REL, fk_status__REL, fk_watertype__REL, label_1_visible__REL, label_2_visible__REL, schema_force_visible__REL

        leitung = WASSER.leitung(
            # FIELDS TO MAP TO WASSER.leitung

            # --- baseclass ---
            # --- sia405_baseclass ---
            **base_common(row, "hydrant"),

            # --- leitung ---
            astatus="undefined",
            # aussenbeschichtung=row.REPLACE_ME,
            baujahr=0,
            # bemerkung=row.REPLACE_ME,
            # betreiber=row.REPLACE_ME,
            # betriebsdruck=row.REPLACE_ME,
            # bettung=row.REPLACE_ME,
            druckzone="undefined",
            # durchmesser=row.REPLACE_ME,
            # durchmesseraussen=row.REPLACE_ME,
            # durchmesserinnen=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # funktion=row.REPLACE_ME,
            geometrie=ST_ForceCurve(ST_Force2D(ST_Transform(row.geometry, 2056))),
            # hydraulische_rauheit=row.REPLACE_ME,
            # innenbeschichtung=row.REPLACE_ME,
            # kathodischer_schutz=row.REPLACE_ME,
            # konzessionaer=row.REPLACE_ME,
            laenge=0,
            # lagebestimmung=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # name_nummer=row.REPLACE_ME,
            # nennweite=row.REPLACE_ME,
            # sanierung_erneuerung=row.REPLACE_ME,
            # schubsicherung=row.REPLACE_ME,
            # strangref=row.REPLACE_ME,
            # ueberdeckung=row.REPLACE_ME,
            # unterhalt=row.REPLACE_ME,
            # unterhaltspflichtiger=row.REPLACE_ME,
            # verbindungsart=row.REPLACE_ME,
            # verlegeart=row.REPLACE_ME,
            # wasserqualitaet=row.REPLACE_ME,
            # zulaessiger_bauteil_betriebsdruck=row.REPLACE_ME,
            zustand="undefined",
        )
        wasser_session.add(leitung)
        print(".", end="")
    print("done")
    wasser_session.commit()
