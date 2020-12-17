print("Exporting QWAT.pipe -> WASSER.conduite")
for row in session.query(QWAT.pipe):
    # AVAILABLE ROW FIELDS : id, fk_parent, fk_function, fk_installmethod, fk_material, fk_distributor, fk_precision, fk_bedding, fk_protection, fk_status, fk_watertype, fk_locationtype, fk_folder, year, year_rehabilitation, year_end, tunnel_or_bridge, pressure_nominal, remark, _valve_count, _valve_closed, label_1_visible, label_1_text, label_2_visible, label_2_text, fk_node_a, fk_node_b, fk_district, fk_pressurezone, fk_printmap, _length2d, _length3d, _diff_elevation, _printmaps, _geometry_alt1_used, _geometry_alt2_used, update_geometry_alt1, update_geometry_alt2, geometry, geometry_alt1, geometry_alt2, schema_force_visible, _schema_visible
    session.add(
        WASSER.conduite(
            # t_id=row.REPLACE_ME,
            # t_ili_tid=row.REPLACE_ME,
            # nom_numero=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # fonction=row.REPLACE_ME,
            # materiau=row.REPLACE_ME,
            # diametre_interieur=row.REPLACE_ME,
            # diametre_exterieur=row.REPLACE_ME,
            # diametre=row.REPLACE_ME,
            # largeur_nominale=row.REPLACE_ME,
            # qualite_eau=row.REPLACE_ME,
            # determination_planimetrique=row.REPLACE_ME,
            # etat=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # genre_de_raccordement=row.REPLACE_ME,
            # isolation_exterieure=row.REPLACE_ME,
            # isolation_interieure=row.REPLACE_ME,
            # mode_de_pose=row.REPLACE_ME,
            # assurance_contre_la_poussee=row.REPLACE_ME,
            # couverture=row.REPLACE_ME,
            # rehabilitation_renovation=row.REPLACE_ME,
            # lit_de_pose=row.REPLACE_ME,
            # protection_cathodique=row.REPLACE_ME,
            # zone_de_pression=row.REPLACE_ME,
            # pression_de_fonctionnement_admissible=row.REPLACE_ME,
            # pression_exploitation=row.REPLACE_ME,
            # rugosite_hydraulique=row.REPLACE_ME,
            # longueur=row.REPLACE_ME,
            # entretien=row.REPLACE_ME,
            # acondition=row.REPLACE_ME,
            # proprietaire=row.REPLACE_ME,
            # exploitant=row.REPLACE_ME,
            # concessionnaire=row.REPLACE_ME,
            # responsable_entretien=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # tronconref=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
    )
    print(".", end="")
print("done")

print("Exporting QWAT.hydrant -> WASSER.hydrant")
for row in session.query(QWAT.hydrant):
    # AVAILABLE ROW FIELDS : id, fk_provider, fk_model_sup, fk_model_inf, fk_material, fk_output, underground, marked, pressure_static, pressure_dynamic, flow, observation_date, observation_source
    session.add(
        WASSER.hydrant(
            # t_id=row.REPLACE_ME,
            # t_ili_tid=row.REPLACE_ME,
            # nom_numero=row.REPLACE_ME,
            # genre=row.REPLACE_ME,
            # materiau=row.REPLACE_ME,
            # dimension=row.REPLACE_ME,
            # fabricant=row.REPLACE_ME,
            # pression_de_distribution=row.REPLACE_ME,
            # pression_ecoulement=row.REPLACE_ME,
            # soutirage=row.REPLACE_ME,
            # atype=row.REPLACE_ME,
            # acondition=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # symboleori=row.REPLACE_ME,
            # determination_planimetrique=row.REPLACE_ME,
            # altitude=row.REPLACE_ME,
            # determination_altimetrique=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # zone_de_pression=row.REPLACE_ME,
            # proprietaire=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # noeudref=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
    )
    print(".", end="")
print("done")

print("Exporting QWAT.tank -> WASSER.reservoir_d_eau")
for row in session.query(QWAT.tank):
    # AVAILABLE ROW FIELDS : id, fk_overflow, fk_tank_firestorage, storage_total, storage_supply, storage_fire, altitude_overflow, altitude_apron, height_max, fire_valve, fire_remote, _litrepercm, cistern1_fk_type, cistern1_dimension_1, cistern1_dimension_2, cistern1_storage, _cistern1_litrepercm, cistern2_fk_type, cistern2_dimension_1, cistern2_dimension_2, cistern2_storage, _cistern2_litrepercm
    session.add(
        WASSER.reservoir_d_eau(
            # t_id=row.REPLACE_ME,
            # t_ili_tid=row.REPLACE_ME,
            # nom_numero=row.REPLACE_ME,
            # genre=row.REPLACE_ME,
            # materiau=row.REPLACE_ME,
            # revetement=row.REPLACE_ME,
            # hauteur_de_refoulement=row.REPLACE_ME,
            # capacite_de_stockage=row.REPLACE_ME,
            # reserve_eau_alimentation=row.REPLACE_ME,
            # reserve_eau_incendie=row.REPLACE_ME,
            # puissance=row.REPLACE_ME,
            # acondition=row.REPLACE_ME,
            # geometrie=row.REPLACE_ME,
            # symboleori=row.REPLACE_ME,
            # determination_planimetrique=row.REPLACE_ME,
            # altitude=row.REPLACE_ME,
            # determination_altimetrique=row.REPLACE_ME,
            # annee_de_construction=row.REPLACE_ME,
            # zone_de_pression=row.REPLACE_ME,
            # proprietaire=row.REPLACE_ME,
            # remarque=row.REPLACE_ME,
            # noeudref=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
    )
    print(".", end="")
print("done")

