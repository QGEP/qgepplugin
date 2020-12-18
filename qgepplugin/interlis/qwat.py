from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from . import utils
from . import config

from .datamodels.qwat import Classes as QWAT
from .datamodels.wasser2015 import Classes as WASSER

###############################################
# Actual export (see qwat_generator to pregenerate some of this code)
###############################################

def export():

    session = Session(utils.create_engine())

    print("Exporting QWAT.node -> WASSER.noeud_hydraulique")
    # Some QWAT.node are abstract (have entries for subclasses, such as hydrant) and some are concrete (no subclass entry).
    # Here's we just insert the concrete ones, the abstract ones will be inserted later.
    # TODO : can't sqlalchemy manage this ? tried with session.merge instead of session.add, but it doesn't work
    # alternatively we could delete the abstract nodes just before adding the subclasses below
    network_elements_ids = set()
    network_elements_ids.update(o[0] for o in session.query(QWAT.hydrant.id).all())
    network_elements_ids.update(o[0] for o in session.query(QWAT.tank.id).all())
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
        # REF_pipe_fk_node_b, district, pressurezone

        noeud_hydraulique = WASSER.noeud_hydraulique(
            # FIELDS TO MAP TO WASSER.noeud_hydraulique

            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='noeud_hydraulique',

            # --- sia405_baseclass ---
            obj_id=row.id,
            t_id=QWAT.node.make_tid(row.id),

            # --- noeud_hydraulique ---
            # consommation=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            nom_numero="???",
            # pression=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # type_de_noeud=row.REPLACE_ME,
        )
        session.add(noeud_hydraulique)
        print(".", end="")
    print("done")
    
    print("Exporting QWAT.hydrant -> WASSER.noeud_hydraulique, WASSER.hydrant")
    for row in session.query(QWAT.hydrant):
        # AVAILABLE FIELDS IN QWAT.hydrant

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, update_geometry_alt1, update_geometry_alt2

        # --- network_element ---
        # altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end

        # --- hydrant ---
        # fk_material, fk_model_inf, fk_model_sup, fk_output, fk_provider, flow, id, marked, observation_date, observation_source, pressure_dynamic, pressure_static, underground

        # --- _relations_ ---
        # REF_meter_id_fkey, REF_part_id_fkey, REF_pipe_fk_node_b, REF_samplingpoint_id_fkey, REF_subscriber_id_fkey, distributor, district, folder, hydrant_material, hydrant_model_inf, hydrant_model_sup, hydrant_output, hydrant_provider, object_reference, precision, precisionalti, pressurezone, status, visible

        noeud_hydraulique = WASSER.noeud_hydraulique(
            # FIELDS TO MAP TO WASSER.noeud_hydraulique

            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='noeud_hydraulique',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- noeud_hydraulique ---
            # consommation=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            nom_numero='???',
            # pression=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            t_id=QWAT.hydrant.make_tid(row.id),
            # type_de_noeud=row.REPLACE_ME,
        )
        session.add(noeud_hydraulique)
        hydrant = WASSER.hydrant(
            # FIELDS TO MAP TO WASSER.hydrant

            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='hydrant',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- noeud_de_conduite ---
            # altitude=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # determination_altimetrique=row.REPLACE_ME,
            determination_planimetrique='???',
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            noeudref=noeud_hydraulique.t_id,
            # proprietaire=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            symboleori=0,  # ???
            # zone_de_pression=row.REPLACE_ME,

            # --- hydrant ---
            # acondition=row.REPLACE_ME,
            # atype=row.REPLACE_ME,
            # dimension=row.REPLACE_ME,
            # fabricant=row.REPLACE_ME,
            # genre=row.REPLACE_ME,
            # materiau=row.REPLACE_ME,
            nom_numero="???",
            # pression_de_distribution=row.REPLACE_ME,
            # pression_ecoulement=row.REPLACE_ME,
            # soutirage=row.REPLACE_ME,
            t_id=QWAT.hydrant.make_tid(row.id+10000000),  # TODO : not too clean...

        )
        session.add(hydrant)
        print(".", end="")
    print("done")

    print("Exporting QWAT.tank -> WASSER.noeud_hydraulique, WASSER.reservoir_d_eau")
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
        # REF_chamber_id_fkey, REF_cover_fk_installation, REF_installation_fk_parent, REF_meter_id_fkey, REF_part_id_fkey, REF_pipe_fk_node_b, REF_pressurecontrol_id_fkey, REF_pump_id_fkey, REF_samplingpoint_id_fkey, REF_source_id_fkey, REF_subscriber_id_fkey, REF_treatment_id_fkey, cistern, distributor, district, folder, installation, object_reference, overflow, precision, precisionalti, pressurezone, remote_type, status, tank_firestorage, visible, watertype

        noeud_hydraulique = WASSER.noeud_hydraulique(
            # FIELDS TO MAP TO WASSER.noeud_hydraulique

            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='noeud_hydraulique',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- noeud_hydraulique ---
            # consommation=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            nom_numero='???',
            # pression=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            t_id=QWAT.tank.make_tid(row.id),
            # type_de_noeud=row.REPLACE_ME,
        )
        session.add(noeud_hydraulique)
        reservoir_d_eau = WASSER.reservoir_d_eau(
            # FIELDS TO MAP TO WASSER.reservoir_d_eau

            # --- baseclass ---
            # t_ili_tid=QWAT.tank.make_tid(row.id),
            t_type='reservoir_d_eau',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- noeud_de_conduite ---
            # altitude=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # determination_altimetrique=row.REPLACE_ME,
            determination_planimetrique='???',
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            noeudref=noeud_hydraulique.t_id,
            # proprietaire=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            symboleori=0,  # ???
            # zone_de_pression=row.REPLACE_ME,

            # --- reservoir_d_eau ---
            # acondition=row.REPLACE_ME,
            capacite_de_stockage=row.storage_total or 0,
            # genre=row.REPLACE_ME,
            hauteur_de_refoulement=row.altitude_overflow or 0,
            # materiau=row.REPLACE_ME,
            nom_numero="???",
            # puissance=row.REPLACE_ME,
            reserve_eau_alimentation=row.storage_supply or 0,
            reserve_eau_incendie=row.storage_fire or 0,
            # revetement=row.REPLACE_ME,
            t_id=QWAT.tank.make_tid(row.id+10000000),  # TODO : not too clean...
        )
        session.add(reservoir_d_eau)
        print(".", end="")
    print("done")

    print("Exporting QWAT.pipe -> WASSER.troncon_hydraulique, WASSER.conduite")
    for row in session.query(QWAT.pipe):
        # AVAILABLE FIELDS IN QWAT.pipe

        # --- pipe ---
        # _diff_elevation, _geometry_alt1_used, _geometry_alt2_used, _length2d, _length3d, _printmaps, _schema_visible, _valve_closed, _valve_count, fk_bedding, fk_distributor, fk_district, fk_folder, fk_function, fk_installmethod, fk_locationtype, fk_material, fk_node_a, fk_node_b, fk_parent, fk_precision, fk_pressurezone, fk_printmap, fk_protection, fk_status, fk_watertype, geometry, geometry_alt1, geometry_alt2, id, label_1_text, label_1_visible, label_2_text, label_2_visible, pressure_nominal, remark, schema_force_visible, tunnel_or_bridge, update_geometry_alt1, update_geometry_alt2, year, year_end, year_rehabilitation

        # --- _relations_ ---
        # REF_crossing_pipe1, REF_leak_fk_pipe, REF_meter_fk_pipe, REF_part_fk_pipe, REF_pipe_fk_parent, REF_pump_fk_pipe_in, REF_subscriber_fk_pipe, REF_valve_fk_pipe, bedding, distributor, district, folder, node, pipe, pipe_function, pipe_installmethod, pipe_material, pipe_protection, precision, pressurezone, status, visible, watertype

        troncon_hydraulique = WASSER.troncon_hydraulique(
            # FIELDS TO MAP TO WASSER.troncon_hydraulique

            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='troncon_hydraulique',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- troncon_hydraulique ---
            # acondition=row.REPLACE_ME,
            aunoeudref=QWAT.node.make_tid(row.fk_node_b),
            # consommation=row.REPLACE_ME,
            # debit=row.REPLACE_ME,
            dunoeudref=QWAT.node.make_tid(row.fk_node_a),
            nom_numero="???",
            reference_diametre=0,  # ???,
            reference_longueur=0,  # ???
            reference_rugosite=0,  # ???,
            # remarque=row.REPLACE_ME,
            t_id=QWAT.pipe.make_tid(row.id),
            # vitesse_ecoulement=row.REPLACE_ME,
        )
        session.add(troncon_hydraulique)
        conduite = WASSER.conduite(
            # FIELDS TO MAP TO WASSER.conduite

            # --- baseclass ---
            t_ili_tid=row.id,
            t_type='conduite',

            # --- sia405_baseclass ---
            obj_id=row.id,

            # --- conduite ---
            acondition=row.status.value_en,
            annee_de_construction=max(1800, row.year or 0),
            # assurance_contre_la_poussee=row.REPLACE_ME,
            # concessionnaire=row.REPLACE_ME,
            # couverture=row.REPLACE_ME,
            # determination_planimetrique=row.REPLACE_ME,
            # diametre=row.REPLACE_ME,
            # diametre_exterieur=row.REPLACE_ME,
            # diametre_interieur=row.REPLACE_ME,
            # entretien=row.REPLACE_ME,
            etat="?",
            # exploitant=row.REPLACE_ME,
            # fonction=row.REPLACE_ME,
            # genre_de_raccordement=row.REPLACE_ME,
            geometrie=ST_Force2D(ST_Transform(row.geometry, 2056)),
            # isolation_exterieure=row.REPLACE_ME,
            # isolation_interieure=row.REPLACE_ME,
            # largeur_nominale=row.REPLACE_ME,
            # lit_de_pose=row.REPLACE_ME,
            longueur=row._length2d,
            materiau=row.pipe_material.value_fr,
            # mode_de_pose=row.REPLACE_ME,
            nom_numero="???",
            # pression_de_fonctionnement_admissible=row.REPLACE_ME,
            # pression_exploitation=row.REPLACE_ME,
            # proprietaire=row.REPLACE_ME,
            # protection_cathodique=row.REPLACE_ME,
            # qualite_eau=row.REPLACE_ME,
            # rehabilitation_renovation=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # responsable_entretien=row.REPLACE_ME,
            # rugosite_hydraulique=row.REPLACE_ME,
            t_id=QWAT.pipe.make_tid(row.id+10000000),  # TODO : not too clean...
            tronconref=troncon_hydraulique.t_id,
            zone_de_pression=row.pressurezone.name,
        )
        session.add(conduite)
        print(".", end="")
    print("done")
    session.commit()

    # EXPORT TEMPORARY SCHEMA
    utils.export_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_NAME)
