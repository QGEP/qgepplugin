from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from . import utils

from .datamodels.qwat import Classes as QWAT
from .datamodels.wasser import Classes as WASSER


###############################################
# Export                                      #
###############################################

def export():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

    print("Exporting QWAT.node -> WASSER.hydraulischer_knoten")
    # Some QWAT.node are abstract (have entries for subclasses, such as hydrant) and some are concrete (no subclass entry).
    # Here's we just insert the concrete ones, the abstract ones will be inserted later.
    # TODO : can't sqlalchemy manage this ? tried with session.merge instead of session.add, but it doesn't work
    # alternatively we could delete the abstract nodes just before adding the subclasses below
    network_elements_ids = set()
    network_elements_ids.update(o[0] for o in session.query(QWAT.hydrant.id).all())
    network_elements_ids.update(o[0] for o in session.query(QWAT.tank.id).all())
    network_elements_ids.update(o[0] for o in session.query(QWAT.pump.id).all())
    # SELECT * FROM "qwat_od"."node" WHERE id=8102;
    # SELECT * FROM "qwat_od"."network_element" WHERE id=8102;
    # SELECT * FROM "qwat_od"."hydrant" WHERE id=8102;
    # SELECT * FROM "qwat_od"."installation" WHERE id=8102;
    # SELECT * FROM "qwat_od"."part" WHERE id=8102;
    # SELECT * FROM "qwat_od"."subscriber" WHERE id=8102;
    # SELECT * FROM "qwat_od"."meter" WHERE id=8102;
    # SELECT * FROM "qwat_od"."valve" WHERE id=8102;
    for row in session.query(QWAT.node):
        # We skip abstract entries element (those that have entries for subclasses)
        if row.id in network_elements_ids:
            continue

        # AVAILABLE FIELDS IN QWAT.node

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, id, update_geometry_alt1, update_geometry_alt2

        # --- _relations_ ---
        # fk_district_REL, fk_pressurezone_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='hydraulischer_knoten',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- hydraulischer_knoten ---
            # bemerkung=row.REPLACE_ME,
            # druck=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # type_de_noeud=row.REPLACE_ME,
            name_nummer="???",
            t_id=QWAT.node.make_tid(row.id),
            # verbrauch=row.REPLACE_ME,

        )
        session.add(hydraulischer_knoten)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QWAT.hydrant -> WASSER.hydraulischer_knoten, WASSER.hydrant")
    for row in session.query(QWAT.hydrant):
        # AVAILABLE FIELDS IN QWAT.hydrant

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- hydrant ---
        # fk_material, fk_model_inf, fk_model_sup, fk_output, fk_provider, flow, id, marked, observation_date, observation_source, pressure_dynamic, pressure_static, underground

        # --- _relations_ ---
        # fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_material_REL, fk_model_inf_REL, fk_model_sup_REL, fk_object_reference_REL, fk_output_REL, fk_precision_REL, fk_precisionalti_REL, fk_pressurezone_REL, fk_provider_REL, fk_status_REL, label_1_visible_REL, label_2_visible_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='hydraulischer_knoten',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- hydraulischer_knoten ---
            # bemerkung=row.REPLACE_ME,
            # druck=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # knotentyp=row.REPLACE_ME,
            name_nummer='???',
            t_id=QWAT.hydrant.make_tid(row.id),
            # verbrauch=row.REPLACE_ME,

        )
        session.add(hydraulischer_knoten)
        hydrant = WASSER.hydrant(
            # FIELDS TO MAP TO WASSER.hydrant
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='hydrant',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- noeud_de_leitung ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            knotenref=hydraulischer_knoten.t_id,
            lagebestimmung='???',
            symbolori=0,  # ???

            # --- hydrant ---
            # art=row.REPLACE_ME,
            # dimension=row.REPLACE_ME,
            # entnahme=row.REPLACE_ME,
            # fliessdruck=row.REPLACE_ME,
            # hersteller=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            name_nummer="???",
            t_id=QWAT.hydrant.make_tid(row.id+10000000),  # TODO : not too clean...
            # typ=row.REPLACE_ME,
            # versorgungsdruck=row.REPLACE_ME,
            # zustand=row.REPLACE_ME,

        )
        session.add(hydrant)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QWAT.tank -> WASSER.hydraulischer_knoten, WASSER.wasserbehaelter")
    for row in session.query(QWAT.tank):
        # AVAILABLE FIELDS IN QWAT.tank

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- installation ---
        # eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel

        # --- tank ---
        # _cistern1_litrepercm, _cistern2_litrepercm, _litrepercm, altitude_apron, altitude_overflow, cistern1_dimension_1, cistern1_dimension_2, cistern1_fk_type, cistern1_storage, cistern2_dimension_1, cistern2_dimension_2, cistern2_fk_type, cistern2_storage, fire_remote, fire_valve, fk_overflow, fk_tank_firestorage, height_max, id, storage_fire, storage_supply, storage_total

        # --- _relations_ ---
        # cistern1_fk_type_REL, cistern2_fk_type_REL, fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_object_reference_REL, fk_overflow_REL, fk_parent_REL, fk_precision_REL, fk_precisionalti_REL, fk_pressurezone_REL, fk_remote_REL, fk_status_REL, fk_tank_firestorage_REL, fk_watertype_REL, label_1_visible_REL, label_2_visible_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='hydraulischer_knoten',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- hydraulischer_knoten ---
            # bemerkung=row.REPLACE_ME,
            # druck=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # knotentyp=row.REPLACE_ME,
            name_nummer='???',
            t_id=QWAT.tank.make_tid(row.id),
            # verbrauch=row.REPLACE_ME,

        )
        session.add(hydraulischer_knoten)
        wasserbehaelter = WASSER.wasserbehaelter(
            # FIELDS TO MAP TO WASSER.wasserbehaelter
            # --- baseclass ---
            # t_ili_tid=QWAT.tank.make_tid(row.id),
            t_type='wasserbehaelter',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- leitungsknoten ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            knotenref=hydraulischer_knoten.t_id,
            lagebestimmung='???',
            symbolori=0,  # ???

            # --- wasserbehaelter ---
            # art=row.REPLACE_ME,
            # beschichtung=row.REPLACE_ME,
            brauchwasserreserve=row.storage_supply or 0,
            fassungsvermoegen=0,  # ???
            # leistung=row.REPLACE_ME,
            loeschwasserreserve=row.storage_fire or 0,
            # material=row.REPLACE_ME,
            name_nummer="???",
            t_id=QWAT.tank.make_tid(row.id+10000000),  # TODO : not too clean...
            ueberlaufhoehe=row.altitude_overflow or 0,
            # zustand=row.REPLACE_ME,

        )
        session.add(wasserbehaelter)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QWAT.pump -> WASSER.hydraulischer_knoten, WASSER.foerderanlage")
    for row in session.query(QWAT.pump):
        # AVAILABLE FIELDS IN QWAT.pump

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- installation ---
        # eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel

        # --- pump ---
        # fk_pipe_in, fk_pipe_out, fk_pump_operating, fk_pump_type, id, manometric_height, no_pumps, rejected_flow

        # --- _relations_ ---
        # fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_object_reference_REL, fk_parent_REL, fk_pipe_in_REL, fk_pipe_out_REL, fk_precision_REL, fk_precisionalti_REL, fk_pressurezone_REL, fk_pump_operating_REL, fk_pump_type_REL, fk_remote_REL, fk_status_REL, fk_watertype_REL, label_1_visible_REL, label_2_visible_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='hydraulischer_knoten',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- hydraulischer_knoten ---
            # bemerkung=row.REPLACE_ME,
            # druck=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # knotentyp=row.REPLACE_ME,
            name_nummer='???',
            t_id=QWAT.pump.make_tid(row.id),
            # verbrauch=row.REPLACE_ME,

        )
        session.add(hydraulischer_knoten)
        foerderanlage = WASSER.foerderanlage(
            # FIELDS TO MAP TO WASSER.foerderanlage
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='foerderanlage',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- noeud_de_leitung ---
            # bemerkung=row.REPLACE_ME,
            # druckzone=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # einbaujahr=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # hoehe=row.REPLACE_ME,
            # hoehenbestimmung=row.REPLACE_ME,
            knotenref=hydraulischer_knoten.t_id,
            lagebestimmung='???',
            symbolori=0,  # ???

            # --- foerderanlage ---
            # art=row.REPLACE_ME,
            leistung=0,  # ???
            # name_nummer=row.REPLACE_ME,
            t_id=QWAT.pump.make_tid(row.id+10000000),  # TODO : not too clean...
            # zustand=row.REPLACE_ME,

        )
        session.add(foerderanlage)
        print(".", end="")
    print("done")
    session.commit()

    print("Exporting QWAT.pipe -> WASSER.hydraulischer_strang, WASSER.leitung")
    for row in session.query(QWAT.pipe):
        # AVAILABLE FIELDS IN QWAT.pipe

        # --- pipe ---
        # _diff_elevation, _geometry_alt1_used, _geometry_alt2_used, _length2d, _length3d, _printmaps, _schema_visible, _valve_closed, _valve_count, fk_bedding, fk_distributor, fk_district, fk_folder, fk_function, fk_installmethod, fk_locationtype, fk_material, fk_node_a, fk_node_b, fk_parent, fk_precision, fk_pressurezone, fk_printmap, fk_protection, fk_status, fk_watertype, geometry, geometry_alt1, geometry_alt2, id, label_1_text, label_1_visible, label_2_text, label_2_visible, pressure_nominal, remark, schema_force_visible, tunnel_or_bridge, update_geometry_alt1, update_geometry_alt2, year, year_end, year_rehabilitation

        # --- _relations_ ---
        # fk_bedding_REL, fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_function_REL, fk_installmethod_REL, fk_material_REL, fk_node_a_REL, fk_node_b_REL, fk_parent_REL, fk_precision_REL, fk_pressurezone_REL, fk_protection_REL, fk_status_REL, fk_watertype_REL, label_1_visible_REL, label_2_visible_REL, schema_force_visible_REL

        hydraulischer_strang = WASSER.hydraulischer_strang(
            # FIELDS TO MAP TO WASSER.hydraulischer_strang
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='troncon_hydraulique',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- hydraulischer_strang ---
            # bemerkung=row.REPLACE_ME,
            bisknotenref=QWAT.node.make_tid(row.fk_node_b),
            # durchfluss=row.REPLACE_ME,
            # fliessgeschwindigkeit=row.REPLACE_ME,
            name_nummer="???",
            referenz_durchmesser=0,  # ???,
            referenz_laenge=0,  # ???
            referenz_rauheit=0,  # ???,
            t_id=QWAT.pipe.make_tid(row.id),
            # verbrauch=row.REPLACE_ME,
            vonknotenref=QWAT.node.make_tid(row.fk_node_a),
            # zustand=row.REPLACE_ME,

        )
        session.add(hydraulischer_strang)
        leitung = WASSER.leitung(
            # FIELDS TO MAP TO WASSER.leitung
            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='leitung',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- leitung ---
            astatus="?",  # ???
            # aussenbeschichtung=row.REPLACE_ME,
            baujahr=max(1800, row.year or 0),
            # betreiber=row.REPLACE_ME,
            # betriebsdruck=row.REPLACE_ME,
            # bettung=row.REPLACE_ME,
            druckzone=row.fk_pressurezone_REL.name,
            # durchmesser=row.REPLACE_ME,
            # durchmesseraussen=row.REPLACE_ME,
            # durchmesserinnen=row.REPLACE_ME,
            # eigentuemer=row.REPLACE_ME,
            # funktion=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # hydraulische_rauheit=row.REPLACE_ME,
            # innenbeschichtung=row.REPLACE_ME,
            # kathodischer_schutz=row.REPLACE_ME,
            # konzessionaer=row.REPLACE_ME,
            laenge=row._length2d,
            # lagebestimmung=row.REPLACE_ME,
            material=row.fk_material_REL.sia_fr,
            name_nummer="???",
            # nennweite=row.REPLACE_ME,
            # sanierung_erneuerung=row.REPLACE_ME,
            # schubsicherung=row.REPLACE_ME,
            strangref=hydraulischer_strang.t_id,
            t_id=QWAT.pipe.make_tid(row.id+10000000),  # TODO : not too clean...
            # ueberdeckung=row.REPLACE_ME,
            # unterhalt=row.REPLACE_ME,
            # unterhaltspflichtiger=row.REPLACE_ME,
            # verbindungsart=row.REPLACE_ME,
            # verlegeart=row.REPLACE_ME,
            # wasserqualitaet=row.REPLACE_ME,
            # zulaessiger_bauteil_betriebsdruck=row.REPLACE_ME,
            zustand=row.fk_status_REL.value_en,
            
        )
        session.add(leitung)
        print(".", end="")
    print("done")
    session.commit()



###############################################
# Import                                      #
###############################################

def import_():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

    print("Importing WASSER.hydraulischer_knoten -> QWAT.node")
    for row in session.query(WASSER.hydraulischer_knoten):
        # AVAILABLE FIELDS IN WASSER.hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

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
        session.add(node)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing WASSER.hydraulischer_knoten, WASSER.hydrant -> QWAT.hydrant")
    for row in session.query(WASSER.hydraulischer_knoten):
    # TODO : somehow join WASSER.hydrant
        # AVAILABLE FIELDS IN WASSER.hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

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
        session.add(hydrant)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing WASSER.hydraulischer_knoten, WASSER.wasserbehaelter -> QWAT.tank")
    for row in session.query(WASSER.hydraulischer_knoten):
    # TODO : somehow join WASSER.wasserbehaelter
        # AVAILABLE FIELDS IN WASSER.hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

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
        session.add(tank)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing WASSER.hydraulischer_knoten, WASSER.foerderanlage -> QWAT.pump")
    for row in session.query(WASSER.hydraulischer_knoten):
    # TODO : somehow join WASSER.foerderanlage
        # AVAILABLE FIELDS IN WASSER.hydraulischer_knoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_knoten ---
        # bemerkung, druck, geometrie, knotentyp, name_nummer, t_id, verbrauch

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
        session.add(pump)
        print(".", end="")
    print("done")
    session.commit()

    print("Importing WASSER.hydraulischer_strang, WASSER.leitung -> QWAT.pipe")
    for row in session.query(WASSER.hydraulischer_strang):
    # TODO : somehow join WASSER.leitung
        # AVAILABLE FIELDS IN WASSER.hydraulischer_strang

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- hydraulischer_strang ---
        # bemerkung, bisknotenref, durchfluss, fliessgeschwindigkeit, name_nummer, referenz_durchmesser, referenz_laenge, referenz_rauheit, t_id, verbrauch, vonknotenref, zustand

        # --- _relations_ ---
        # bisknotenref_REL, vonknotenref_REL

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
        session.add(pipe)
        print(".", end="")
    print("done")
    session.commit()

