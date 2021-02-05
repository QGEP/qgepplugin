from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from .. import utils

from .model_qwat import QWAT
from .model_wasser import WASSER


def import_():

    wasser_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    qwat_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)

    print("Importing WASSER.hydraulischer_knoten -> QWAT.node")
    for row in wasser_session.query(WASSER.hydraulischer_knoten):

        # AVAILABLE FIELDS IN hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

        # --- _bwrel_ ---
        # hydraulischer_strang__BWREL_bisknotenref, hydraulischer_strang__BWREL_vonknotenref, leitungsknoten__BWREL_knotenref, metaattribute__BWREL_sia405_baseclass_metaattribute, schadenstelle__BWREL_t_id, sia405_textpos__BWREL_hydraulischer_knotenref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        node = QWAT.node(
            # FIELDS TO MAP TO QWAT.node

            # --- node ---
            # _geometry_alt1_used=row.REPLACE_ME,
            # _geometry_alt2_used=row.REPLACE_ME,
            # _pipe_node_type=row.REPLACE_ME,
            # _pipe_orientation=row.REPLACE_ME,
            # _pipe_schema_visible=row.REPLACE_ME,
            # _printmaps=row.REPLACE_ME,
            # fk_district=row.REPLACE_ME,
            # fk_pressurezone=row.REPLACE_ME,
            # fk_printmap=row.REPLACE_ME,
            # geometry=row.REPLACE_ME,
            # geometry_alt1=row.REPLACE_ME,
            # geometry_alt2=row.REPLACE_ME,
            # id=row.REPLACE_ME,
            # update_geometry_alt1=row.REPLACE_ME,
            # update_geometry_alt2=row.REPLACE_ME,
        )
        qwat_session.add(node)
        print(".", end="")
    print("done")

    print("Importing WASSER.hydraulischer_knoten, WASSER.hydrant -> QWAT.hydrant")
    for row, hydrant in wasser_session.query(WASSER.hydraulischer_knoten, WASSER.hydrant).join(WASSER.hydrant):

        # AVAILABLE FIELDS IN hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

        # --- _bwrel_ ---
        # hydraulischer_strang__BWREL_bisknotenref, hydraulischer_strang__BWREL_vonknotenref, leitungsknoten__BWREL_knotenref, metaattribute__BWREL_sia405_baseclass_metaattribute, schadenstelle__BWREL_t_id, sia405_textpos__BWREL_hydraulischer_knotenref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # AVAILABLE FIELDS IN hydrant

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- leitungsknoten ---
        # bemerkung, druckzone, eigentuemer, einbaujahr, geometrie, hoehe, hoehenbestimmung, knotenref, lagebestimmung, symbolori

        # --- hydrant ---
        # art, dimension, entnahme, fliessdruck, hersteller, material, name_nummer, t_id, typ, versorgungsdruck, zustand

        # --- _bwrel_ ---
        # absperrorgan__BWREL_t_id, anlage__BWREL_t_id, hausanschluss__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, muffen__BWREL_t_id, rohrleitungsteil__BWREL_t_id, schadenstelle__BWREL_t_id, sia405_symbolpos__BWREL_objekt, sia405_textpos__BWREL_leitungsknotenref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id, uebrige__BWREL_t_id, wassergewinnungsanlage__BWREL_t_id

        # --- _rel_ ---
        # knotenref__REL

        hydrant = QWAT.hydrant(
            # FIELDS TO MAP TO QWAT.hydrant

            # --- node ---
            # _geometry_alt1_used=row.REPLACE_ME,
            # _geometry_alt2_used=row.REPLACE_ME,
            # _pipe_node_type=row.REPLACE_ME,
            # _pipe_orientation=row.REPLACE_ME,
            # _pipe_schema_visible=row.REPLACE_ME,
            # _printmaps=row.REPLACE_ME,
            # fk_district=row.REPLACE_ME,
            # fk_pressurezone=row.REPLACE_ME,
            # fk_printmap=row.REPLACE_ME,
            # geometry=row.REPLACE_ME,
            # geometry_alt1=row.REPLACE_ME,
            # geometry_alt2=row.REPLACE_ME,
            # update_geometry_alt1=row.REPLACE_ME,
            # update_geometry_alt2=row.REPLACE_ME,

            # --- network_element ---
            # altitude=row.REPLACE_ME,
            # fk_distributor=row.REPLACE_ME,
            # fk_folder=row.REPLACE_ME,
            # fk_locationtype=row.REPLACE_ME,
            # fk_object_reference=row.REPLACE_ME,
            # fk_precision=row.REPLACE_ME,
            # fk_precisionalti=row.REPLACE_ME,
            # fk_status=row.REPLACE_ME,
            # identification=row.REPLACE_ME,
            # label_1_rotation=row.REPLACE_ME,
            # label_1_text=row.REPLACE_ME,
            # label_1_visible=row.REPLACE_ME,
            # label_1_x=row.REPLACE_ME,
            # label_1_y=row.REPLACE_ME,
            # label_2_rotation=row.REPLACE_ME,
            # label_2_text=row.REPLACE_ME,
            # label_2_visible=row.REPLACE_ME,
            # label_2_x=row.REPLACE_ME,
            # label_2_y=row.REPLACE_ME,
            # orientation=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # year=row.REPLACE_ME,
            # year_end=row.REPLACE_ME,

            # --- hydrant ---
            # fk_material=row.REPLACE_ME,
            # fk_model_inf=row.REPLACE_ME,
            # fk_model_sup=row.REPLACE_ME,
            # fk_output=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # flow=row.REPLACE_ME,
            # id=row.REPLACE_ME,
            # marked=row.REPLACE_ME,
            # observation_date=row.REPLACE_ME,
            # observation_source=row.REPLACE_ME,
            # pressure_dynamic=row.REPLACE_ME,
            # pressure_static=row.REPLACE_ME,
            # underground=row.REPLACE_ME,
        )
        qwat_session.add(hydrant)
        print(".", end="")
    print("done")

    print("Importing WASSER.hydraulischer_knoten, WASSER.wasserbehaelter -> QWAT.tank")
    for row, wasserbehaelter in wasser_session.query(WASSER.hydraulischer_knoten, WASSER.wasserbehaelter).join(WASSER.wasserbehaelter):

        # AVAILABLE FIELDS IN hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

        # --- _bwrel_ ---
        # hydraulischer_strang__BWREL_bisknotenref, hydraulischer_strang__BWREL_vonknotenref, leitungsknoten__BWREL_knotenref, metaattribute__BWREL_sia405_baseclass_metaattribute, schadenstelle__BWREL_t_id, sia405_textpos__BWREL_hydraulischer_knotenref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # AVAILABLE FIELDS IN wasserbehaelter

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- leitungsknoten ---
        # bemerkung, druckzone, eigentuemer, einbaujahr, geometrie, hoehe, hoehenbestimmung, knotenref, lagebestimmung, symbolori

        # --- wasserbehaelter ---
        # art, beschichtung, brauchwasserreserve, fassungsvermoegen, leistung, loeschwasserreserve, material, name_nummer, t_id, ueberlaufhoehe, zustand

        # --- _bwrel_ ---
        # absperrorgan__BWREL_t_id, anlage__BWREL_t_id, hausanschluss__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, muffen__BWREL_t_id, rohrleitungsteil__BWREL_t_id, schadenstelle__BWREL_t_id, sia405_symbolpos__BWREL_objekt, sia405_textpos__BWREL_leitungsknotenref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id, uebrige__BWREL_t_id, wassergewinnungsanlage__BWREL_t_id

        # --- _rel_ ---
        # knotenref__REL

        tank = QWAT.tank(
            # FIELDS TO MAP TO QWAT.tank

            # --- node ---
            # _geometry_alt1_used=row.REPLACE_ME,
            # _geometry_alt2_used=row.REPLACE_ME,
            # _pipe_node_type=row.REPLACE_ME,
            # _pipe_orientation=row.REPLACE_ME,
            # _pipe_schema_visible=row.REPLACE_ME,
            # _printmaps=row.REPLACE_ME,
            # fk_district=row.REPLACE_ME,
            # fk_pressurezone=row.REPLACE_ME,
            # fk_printmap=row.REPLACE_ME,
            # geometry=row.REPLACE_ME,
            # geometry_alt1=row.REPLACE_ME,
            # geometry_alt2=row.REPLACE_ME,
            # update_geometry_alt1=row.REPLACE_ME,
            # update_geometry_alt2=row.REPLACE_ME,

            # --- network_element ---
            # altitude=row.REPLACE_ME,
            # fk_distributor=row.REPLACE_ME,
            # fk_folder=row.REPLACE_ME,
            # fk_locationtype=row.REPLACE_ME,
            # fk_object_reference=row.REPLACE_ME,
            # fk_precision=row.REPLACE_ME,
            # fk_precisionalti=row.REPLACE_ME,
            # fk_status=row.REPLACE_ME,
            # identification=row.REPLACE_ME,
            # label_1_rotation=row.REPLACE_ME,
            # label_1_text=row.REPLACE_ME,
            # label_1_visible=row.REPLACE_ME,
            # label_1_x=row.REPLACE_ME,
            # label_1_y=row.REPLACE_ME,
            # label_2_rotation=row.REPLACE_ME,
            # label_2_text=row.REPLACE_ME,
            # label_2_visible=row.REPLACE_ME,
            # label_2_x=row.REPLACE_ME,
            # label_2_y=row.REPLACE_ME,
            # orientation=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # year=row.REPLACE_ME,
            # year_end=row.REPLACE_ME,

            # --- installation ---
            # eca=row.REPLACE_ME,
            # fk_parent=row.REPLACE_ME,
            # fk_remote=row.REPLACE_ME,
            # fk_watertype=row.REPLACE_ME,
            # geometry_polygon=row.REPLACE_ME,
            # name=row.REPLACE_ME,
            # open_water_surface=row.REPLACE_ME,
            # parcel=row.REPLACE_ME,

            # --- tank ---
            # _cistern1_litrepercm=row.REPLACE_ME,
            # _cistern2_litrepercm=row.REPLACE_ME,
            # _litrepercm=row.REPLACE_ME,
            # altitude_apron=row.REPLACE_ME,
            # altitude_overflow=row.REPLACE_ME,
            # cistern1_dimension_1=row.REPLACE_ME,
            # cistern1_dimension_2=row.REPLACE_ME,
            # cistern1_fk_type=row.REPLACE_ME,
            # cistern1_storage=row.REPLACE_ME,
            # cistern2_dimension_1=row.REPLACE_ME,
            # cistern2_dimension_2=row.REPLACE_ME,
            # cistern2_fk_type=row.REPLACE_ME,
            # cistern2_storage=row.REPLACE_ME,
            # fire_remote=row.REPLACE_ME,
            # fire_valve=row.REPLACE_ME,
            # fk_overflow=row.REPLACE_ME,
            # fk_tank_firestorage=row.REPLACE_ME,
            # height_max=row.REPLACE_ME,
            # id=row.REPLACE_ME,
            # storage_fire=row.REPLACE_ME,
            # storage_supply=row.REPLACE_ME,
            # storage_total=row.REPLACE_ME,
        )
        qwat_session.add(tank)
        print(".", end="")
    print("done")

    print("Importing WASSER.hydraulischer_knoten, WASSER.foerderanlage -> QWAT.pump")
    for row, foerderanlage in wasser_session.query(WASSER.hydraulischer_knoten, WASSER.foerderanlage).join(WASSER.foerderanlage):

        # AVAILABLE FIELDS IN hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

        # --- _bwrel_ ---
        # hydraulischer_strang__BWREL_bisknotenref, hydraulischer_strang__BWREL_vonknotenref, leitungsknoten__BWREL_knotenref, metaattribute__BWREL_sia405_baseclass_metaattribute, schadenstelle__BWREL_t_id, sia405_textpos__BWREL_hydraulischer_knotenref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # AVAILABLE FIELDS IN foerderanlage

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- leitungsknoten ---
        # bemerkung, druckzone, eigentuemer, einbaujahr, geometrie, hoehe, hoehenbestimmung, knotenref, lagebestimmung, symbolori

        # --- foerderanlage ---
        # art, leistung, name_nummer, t_id, zustand

        # --- _bwrel_ ---
        # absperrorgan__BWREL_t_id, anlage__BWREL_t_id, hausanschluss__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, muffen__BWREL_t_id, rohrleitungsteil__BWREL_t_id, schadenstelle__BWREL_t_id, sia405_symbolpos__BWREL_objekt, sia405_textpos__BWREL_leitungsknotenref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id, uebrige__BWREL_t_id, wassergewinnungsanlage__BWREL_t_id

        # --- _rel_ ---
        # knotenref__REL

        pump = QWAT.pump(
            # FIELDS TO MAP TO QWAT.pump

            # --- node ---
            # _geometry_alt1_used=row.REPLACE_ME,
            # _geometry_alt2_used=row.REPLACE_ME,
            # _pipe_node_type=row.REPLACE_ME,
            # _pipe_orientation=row.REPLACE_ME,
            # _pipe_schema_visible=row.REPLACE_ME,
            # _printmaps=row.REPLACE_ME,
            # fk_district=row.REPLACE_ME,
            # fk_pressurezone=row.REPLACE_ME,
            # fk_printmap=row.REPLACE_ME,
            # geometry=row.REPLACE_ME,
            # geometry_alt1=row.REPLACE_ME,
            # geometry_alt2=row.REPLACE_ME,
            # update_geometry_alt1=row.REPLACE_ME,
            # update_geometry_alt2=row.REPLACE_ME,

            # --- network_element ---
            # altitude=row.REPLACE_ME,
            # fk_distributor=row.REPLACE_ME,
            # fk_folder=row.REPLACE_ME,
            # fk_locationtype=row.REPLACE_ME,
            # fk_object_reference=row.REPLACE_ME,
            # fk_precision=row.REPLACE_ME,
            # fk_precisionalti=row.REPLACE_ME,
            # fk_status=row.REPLACE_ME,
            # identification=row.REPLACE_ME,
            # label_1_rotation=row.REPLACE_ME,
            # label_1_text=row.REPLACE_ME,
            # label_1_visible=row.REPLACE_ME,
            # label_1_x=row.REPLACE_ME,
            # label_1_y=row.REPLACE_ME,
            # label_2_rotation=row.REPLACE_ME,
            # label_2_text=row.REPLACE_ME,
            # label_2_visible=row.REPLACE_ME,
            # label_2_x=row.REPLACE_ME,
            # label_2_y=row.REPLACE_ME,
            # orientation=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # year=row.REPLACE_ME,
            # year_end=row.REPLACE_ME,

            # --- installation ---
            # eca=row.REPLACE_ME,
            # fk_parent=row.REPLACE_ME,
            # fk_remote=row.REPLACE_ME,
            # fk_watertype=row.REPLACE_ME,
            # geometry_polygon=row.REPLACE_ME,
            # name=row.REPLACE_ME,
            # open_water_surface=row.REPLACE_ME,
            # parcel=row.REPLACE_ME,

            # --- pump ---
            # fk_pipe_in=row.REPLACE_ME,
            # fk_pipe_out=row.REPLACE_ME,
            # fk_pump_operating=row.REPLACE_ME,
            # fk_pump_type=row.REPLACE_ME,
            # id=row.REPLACE_ME,
            # manometric_height=row.REPLACE_ME,
            # no_pumps=row.REPLACE_ME,
            # rejected_flow=row.REPLACE_ME,
        )
        qwat_session.add(pump)
        print(".", end="")
    print("done")

    print("Importing WASSER.hydraulischer_strang, WASSER.leitung -> QWAT.pipe")
    for row, leitung in wasser_session.query(WASSER.hydraulischer_strang, WASSER.leitung).join(WASSER.leitung):

        # AVAILABLE FIELDS IN hydraulischer_strang

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_strang ---
        # bemerkung, bisknotenref, durchfluss, fliessgeschwindigkeit, name_nummer, referenz_durchmesser, referenz_laenge, referenz_rauheit, t_id, verbrauch, vonknotenref, zustand

        # --- _bwrel_ ---
        # leitung__BWREL_strangref, metaattribute__BWREL_sia405_baseclass_metaattribute, schadenstelle__BWREL_t_id, sia405_textpos__BWREL_hydraulischer_strangref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # bisknotenref__REL, vonknotenref__REL

        # AVAILABLE FIELDS IN leitung

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- leitung ---
        # astatus, aussenbeschichtung, baujahr, bemerkung, betreiber, betriebsdruck, bettung, druckzone, durchmesser, durchmesseraussen, durchmesserinnen, eigentuemer, funktion, geometrie, hydraulische_rauheit, innenbeschichtung, kathodischer_schutz, konzessionaer, laenge, lagebestimmung, material, name_nummer, nennweite, sanierung_erneuerung, schubsicherung, strangref, t_id, ueberdeckung, unterhalt, unterhaltspflichtiger, verbindungsart, verlegeart, wasserqualitaet, zulaessiger_bauteil_betriebsdruck, zustand

        # --- _bwrel_ ---
        # metaattribute__BWREL_sia405_baseclass_metaattribute, schadenstelle__BWREL_leitungref, schadenstelle__BWREL_t_id, sia405_textpos__BWREL_leitungref, spezialbauwerk__BWREL_t_id, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # strangref__REL

        pipe = QWAT.pipe(
            # FIELDS TO MAP TO QWAT.pipe

            # --- pipe ---
            # _diff_elevation=row.REPLACE_ME,
            # _geometry_alt1_used=row.REPLACE_ME,
            # _geometry_alt2_used=row.REPLACE_ME,
            # _length2d=row.REPLACE_ME,
            # _length3d=row.REPLACE_ME,
            # _printmaps=row.REPLACE_ME,
            # _schema_visible=row.REPLACE_ME,
            # _valve_closed=row.REPLACE_ME,
            # _valve_count=row.REPLACE_ME,
            # fk_bedding=row.REPLACE_ME,
            # fk_distributor=row.REPLACE_ME,
            # fk_district=row.REPLACE_ME,
            # fk_folder=row.REPLACE_ME,
            # fk_function=row.REPLACE_ME,
            # fk_installmethod=row.REPLACE_ME,
            # fk_locationtype=row.REPLACE_ME,
            # fk_material=row.REPLACE_ME,
            # fk_node_a=row.REPLACE_ME,
            # fk_node_b=row.REPLACE_ME,
            # fk_parent=row.REPLACE_ME,
            # fk_precision=row.REPLACE_ME,
            # fk_pressurezone=row.REPLACE_ME,
            # fk_printmap=row.REPLACE_ME,
            # fk_protection=row.REPLACE_ME,
            # fk_status=row.REPLACE_ME,
            # fk_watertype=row.REPLACE_ME,
            # geometry=row.REPLACE_ME,
            # geometry_alt1=row.REPLACE_ME,
            # geometry_alt2=row.REPLACE_ME,
            # id=row.REPLACE_ME,
            # label_1_text=row.REPLACE_ME,
            # label_1_visible=row.REPLACE_ME,
            # label_2_text=row.REPLACE_ME,
            # label_2_visible=row.REPLACE_ME,
            # pressure_nominal=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # schema_force_visible=row.REPLACE_ME,
            # tunnel_or_bridge=row.REPLACE_ME,
            # update_geometry_alt1=row.REPLACE_ME,
            # update_geometry_alt2=row.REPLACE_ME,
            # year=row.REPLACE_ME,
            # year_end=row.REPLACE_ME,
            # year_rehabilitation=row.REPLACE_ME,
        )
        qwat_session.add(pipe)
        print(".", end="")
    print("done")

    qwat_session.commit()

    qwat_session.close()
    wasser_session.close()
