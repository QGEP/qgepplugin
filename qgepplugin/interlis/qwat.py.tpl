print("Exporting QWAT.pipe -> WASSER.conduite")
for row in session.query(QWAT.pipe):
    # AVAILABLE ROW FIELDS (from relationships : REF_crossing_pipe1, REF_pump_fk_pipe_out, bedding, distributor, district, folder, node, pipe, pipe_function, pipe_installmethod, pipe_material, pipe_protection, precision, pressurezone, status, visible, watertype)
    # AVAILABLE ROW FIELDS (from pipe : _diff_elevation, _geometry_alt1_used, _geometry_alt2_used, _length2d, _length3d, _printmaps, _schema_visible, _valve_closed, _valve_count, fk_bedding, fk_distributor, fk_district, fk_folder, fk_function, fk_installmethod, fk_locationtype, fk_material, fk_node_a, fk_node_b, fk_parent, fk_precision, fk_pressurezone, fk_printmap, fk_protection, fk_status, fk_watertype, geometry, geometry_alt1, geometry_alt2, id, label_1_text, label_1_visible, label_2_text, label_2_visible, pressure_nominal, remark, schema_force_visible, tunnel_or_bridge, update_geometry_alt1, update_geometry_alt2, year, year_end, year_rehabilitation)
    session.add(
        WASSER.conduite(
            # REF_conduite_texte_conduiteref_fkey=row.REPLACE_ME,
            # REF_lieu_de_fuite_conduiteref_fkey=row.REPLACE_ME,
            # REF_metaattributs_conduite_metaattributs_fkey=row.REPLACE_ME,
            # _decl_class_registry=row.REPLACE_ME,
            # _sa_class_manager=row.REPLACE_ME,
            # _sa_decl_prepare=row.REPLACE_ME,
            # _sa_raise_deferred_config=row.REPLACE_ME,
            # acondition=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # assurance_contre_la_poussee=row.REPLACE_ME,
            # classes=row.REPLACE_ME,
            # concessionnaire=row.REPLACE_ME,
            # couverture=row.REPLACE_ME,
            # determination_planimetrique=row.REPLACE_ME,
            # diametre=row.REPLACE_ME,
            # diametre_exterieur=row.REPLACE_ME,
            # diametre_interieur=row.REPLACE_ME,
            # entretien=row.REPLACE_ME,
            # etat=row.REPLACE_ME,
            # exploitant=row.REPLACE_ME,
            # fonction=row.REPLACE_ME,
            # genre_de_raccordement=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # isolation_exterieure=row.REPLACE_ME,
            # isolation_interieure=row.REPLACE_ME,
            # largeur_nominale=row.REPLACE_ME,
            # lit_de_pose=row.REPLACE_ME,
            # longueur=row.REPLACE_ME,
            # materiau=row.REPLACE_ME,
            # metadata=row.REPLACE_ME,
            # mode_de_pose=row.REPLACE_ME,
            # nom_numero=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # prepare=row.REPLACE_ME,
            # pression_de_fonctionnement_admissible=row.REPLACE_ME,
            # pression_exploitation=row.REPLACE_ME,
            # proprietaire=row.REPLACE_ME,
            # protection_cathodique=row.REPLACE_ME,
            # qualite_eau=row.REPLACE_ME,
            # rehabilitation_renovation=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # responsable_entretien=row.REPLACE_ME,
            # rugosite_hydraulique=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # t_ili_tid=row.REPLACE_ME,
            # troncon_hydraulique=row.REPLACE_ME,
            # tronconref=row.REPLACE_ME,
            # zone_de_pression=row.REPLACE_ME,
        )
    )
    print(".", end="")
print("done")

print("Exporting QWAT.hydrant -> WASSER.hydrant")
for row in session.query(QWAT.hydrant):
    # AVAILABLE ROW FIELDS (from relationships : REF_meter_id_fkey, REF_part_id_fkey, REF_samplingpoint_id_fkey, REF_subscriber_id_fkey, distributor, folder, hydrant_material, hydrant_model_inf, hydrant_model_sup, hydrant_output, hydrant_provider, node, object_reference, precision, precisionalti, status, visible)
    # AVAILABLE ROW FIELDS (from hydrant : fk_material, fk_model_inf, fk_model_sup, fk_output, fk_provider, flow, id, marked, observation_date, observation_source, pressure_dynamic, pressure_static, underground)
    # AVAILABLE ROW FIELDS (from network_element : altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end)
    session.add(
        WASSER.hydrant(
            # REF_metaattributs_hydrant_metaattributs_fkey=row.REPLACE_ME,
            # REF_noeud_de_conduite_texte_noeud_de_conduitrf_hydrant_fkey=row.REPLACE_ME,
            # REF_position_plan_d_ensemble_objet_hydrant_fkey=row.REPLACE_ME,
            # _decl_class_registry=row.REPLACE_ME,
            # _sa_class_manager=row.REPLACE_ME,
            # _sa_decl_prepare=row.REPLACE_ME,
            # _sa_raise_deferred_config=row.REPLACE_ME,
            # acondition=row.REPLACE_ME,
            # altitude=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # atype=row.REPLACE_ME,
            # classes=row.REPLACE_ME,
            # determination_altimetrique=row.REPLACE_ME,
            # determination_planimetrique=row.REPLACE_ME,
            # dimension=row.REPLACE_ME,
            # fabricant=row.REPLACE_ME,
            # genre=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # materiau=row.REPLACE_ME,
            # metadata=row.REPLACE_ME,
            # noeud_hydraulique=row.REPLACE_ME,
            # noeudref=row.REPLACE_ME,
            # nom_numero=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # prepare=row.REPLACE_ME,
            # pression_de_distribution=row.REPLACE_ME,
            # pression_ecoulement=row.REPLACE_ME,
            # proprietaire=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # soutirage=row.REPLACE_ME,
            # symboleori=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # t_ili_tid=row.REPLACE_ME,
            # zone_de_pression=row.REPLACE_ME,
        )
    )
    print(".", end="")
print("done")

print("Exporting QWAT.tank -> WASSER.reservoir_d_eau")
for row in session.query(QWAT.tank):
    # AVAILABLE ROW FIELDS (from relationships : REF_chamber_id_fkey, REF_cover_fk_installation, REF_installation_fk_parent, REF_meter_id_fkey, REF_part_id_fkey, REF_pressurecontrol_id_fkey, REF_pump_id_fkey, REF_samplingpoint_id_fkey, REF_source_id_fkey, REF_subscriber_id_fkey, REF_treatment_id_fkey, cistern, distributor, folder, installation, node, object_reference, overflow, precision, precisionalti, remote_type, status, tank_firestorage, visible, watertype)
    # AVAILABLE ROW FIELDS (from tank : _cistern1_litrepercm, _cistern2_litrepercm, _litrepercm, altitude_apron, altitude_overflow, cistern1_dimension_1, cistern1_dimension_2, cistern1_fk_type, cistern1_storage, cistern2_dimension_1, cistern2_dimension_2, cistern2_fk_type, cistern2_storage, fire_remote, fire_valve, fk_overflow, fk_tank_firestorage, height_max, id, storage_fire, storage_supply, storage_total)
    # AVAILABLE ROW FIELDS (from network_element : altitude, fk_distributor, fk_folder, fk_locationtype, fk_object_reference, fk_precision, fk_precisionalti, fk_status, identification, label_1_rotation, label_1_text, label_1_visible, label_1_x, label_1_y, label_2_rotation, label_2_text, label_2_visible, label_2_x, label_2_y, orientation, remark, year, year_end)
    # AVAILABLE ROW FIELDS (from installation : eca, fk_parent, fk_remote, fk_watertype, geometry_polygon, name, open_water_surface, parcel)
    session.add(
        WASSER.reservoir_d_eau(
            # REF_metaattributs_reservoir_d_eau_metttrbuts_fkey=row.REPLACE_ME,
            # REF_noeud_de_conduite_texte_noeud_d_cndtrf_rsrvr_d_eau_fkey=row.REPLACE_ME,
            # REF_position_plan_d_ensemble_objet_reservoir_d_eau_fkey=row.REPLACE_ME,
            # _decl_class_registry=row.REPLACE_ME,
            # _sa_class_manager=row.REPLACE_ME,
            # _sa_decl_prepare=row.REPLACE_ME,
            # _sa_raise_deferred_config=row.REPLACE_ME,
            # acondition=row.REPLACE_ME,
            # altitude=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # capacite_de_stockage=row.REPLACE_ME,
            # classes=row.REPLACE_ME,
            # determination_altimetrique=row.REPLACE_ME,
            # determination_planimetrique=row.REPLACE_ME,
            # genre=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # hauteur_de_refoulement=row.REPLACE_ME,
            # materiau=row.REPLACE_ME,
            # metadata=row.REPLACE_ME,
            # noeud_hydraulique=row.REPLACE_ME,
            # noeudref=row.REPLACE_ME,
            # nom_numero=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # prepare=row.REPLACE_ME,
            # proprietaire=row.REPLACE_ME,
            # puissance=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # reserve_eau_alimentation=row.REPLACE_ME,
            # reserve_eau_incendie=row.REPLACE_ME,
            # revetement=row.REPLACE_ME,
            # symboleori=row.REPLACE_ME,
            # t_id=row.REPLACE_ME,
            # t_ili_tid=row.REPLACE_ME,
            # zone_de_pression=row.REPLACE_ME,
        )
    )
    print(".", end="")
print("done")

