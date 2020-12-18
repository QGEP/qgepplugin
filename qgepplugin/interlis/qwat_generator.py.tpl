    TABLE_MAPPING = {
        QWAT.node: [WASSER.noeud_hydraulique],
        QWAT.hydrant: [WASSER.noeud_hydraulique, WASSER.hydrant],
        QWAT.tank: [WASSER.noeud_hydraulique, WASSER.reservoir_d_eau],
        QWAT.pump: [WASSER.noeud_hydraulique, WASSER.station_de_pompage],
        QWAT.pipe: [WASSER.troncon_hydraulique, WASSER.conduite],
        # NOT MAPPED YET
        # AVAILABLE WASSER CLASSES : autres, autres_genre, baseclass, branchement_d_immeuble, branchement_d_immeuble_branchement_d_immeuble, branchement_d_immeuble_piece_isolante, composant, composant_genre, composant_materiau, composant_raccordement, conduite, conduite_assurance_contre_la_poussee, conduite_determination_planimetrique, conduite_fonction, conduite_genre_de_raccordement, conduite_isolation_exterieure, conduite_isolation_interieure, conduite_lit_de_pose, conduite_materiau, conduite_mode_de_pose, conduite_protection_cathodique, conduite_qualite_eau, conduite_rehabilitation_renovation, conduite_troncon_assoc, connexion_tubulaire, connexion_tubulaire_assurance_contre_la_poussee, connexion_tubulaire_genre, construction_speciale, construction_speciale_genre, construction_speciale_ligne, construction_speciale_materiau, construction_speciale_surface, determination_planimetrique, etat, etatvaleurs, halignment, hydrant, hydrant_genre, hydrant_materiau, installation, installation_d_approvisionnement_en_eau, installation_d_approvisionnement_en_eau_genre, installation_determination_altimetrique, installation_determination_planimetrique, installation_genre, installation_materiau, lieu_de_fuite, lieu_de_fuite_cause, lieu_de_fuite_genre, metaattributs, noeud_de_conduite, noeud_de_conduite_determination_altimetrique, noeud_de_conduite_determination_planimetrique, noeud_de_conduite_noeud_assoc, noeud_hydraulique, noeud_hydraulique_type_de_noeud, organe_de_fermeture, organe_de_fermeture_commande, organe_de_fermeture_etat_de_la_connexion, organe_de_fermeture_genre, organe_de_fermeture_materiau, organe_de_fermeture_sens_de_fermeture, point_de_conduite, point_de_conduite_determination_altimetrique, point_de_conduite_determination_planimetrique, point_de_conduite_genre, reservoir_d_eau, reservoir_d_eau_genre, reservoir_d_eau_materiau, sia4055_lv95sia405_eaux_conduite_fonction, sia4055_lv95sia405_eaux_conduite_materiau, sia4055_lv95sia405_eaux_construction_speciale_genre, sia4055_lv95sia405_eaux_cs_conduite_determination_planmtrque, sia4055_lv95sia405_eaux_installation_genre, sia405_15_lv95sia405_eaux_cs_conduite, sia405_15_lv95sia405_eaux_cs_conduite_texte, sia405_15_lv95sia405_eaux_cs_conduite_texteassoc, sia405_15_lv95sia405_eaux_cs_construction_speciale, sia405_15_lv95sia405_eaux_cs_construction_speciale_ligne, sia405_15_lv95sia405_eaux_cs_construction_speciale_lignessoc, sia405_15_lv95sia405_eaux_cs_construction_speciale_surface, sia405_15_lv95sia405_eaux_cs_construction_speciale_surfcssoc, sia405_15_lv95sia405_eaux_cs_construction_speciale_texte, sia405_15_lv95sia405_eaux_cs_construction_speciale_textessoc, sia405_15_lv95sia405_eaux_cs_installation, sia405_15_lv95sia405_eaux_cs_noeud_de_conduite, sia405_15_lv95sia405_eaux_cs_noeud_de_conduite_texte, sia405_15_lv95sia405_eaux_cs_noeud_de_conduite_texteassoc, sia405_baseclass, sia405_symbolepos, sia405_textepos, station_de_pompage, station_de_pompage_genre, symbolepos, t_ili2db_attrname, t_ili2db_basket, t_ili2db_classname, t_ili2db_dataset, t_ili2db_inheritance, t_ili2db_model, t_ili2db_settings, textepos, troncon_hydraulique, type_de_plan, valignment
        # QWAT.bedding: [WASSER.REPLACE_ME],
        # QWAT.chamber: [WASSER.REPLACE_ME],
        # QWAT.cistern: [WASSER.REPLACE_ME],
        # QWAT.consumptionzone: [WASSER.REPLACE_ME],
        # QWAT.cover: [WASSER.REPLACE_ME],
        # QWAT.cover_type: [WASSER.REPLACE_ME],
        # QWAT.crossing: [WASSER.REPLACE_ME],
        # QWAT.damage: [WASSER.REPLACE_ME],
        # QWAT.distributor: [WASSER.REPLACE_ME],
        # QWAT.district: [WASSER.REPLACE_ME],
        # QWAT.folder: [WASSER.REPLACE_ME],
        # QWAT.hydrant_material: [WASSER.REPLACE_ME],
        # QWAT.hydrant_model_inf: [WASSER.REPLACE_ME],
        # QWAT.hydrant_model_sup: [WASSER.REPLACE_ME],
        # QWAT.hydrant_output: [WASSER.REPLACE_ME],
        # QWAT.hydrant_provider: [WASSER.REPLACE_ME],
        # QWAT.installation: [WASSER.REPLACE_ME],
        # QWAT.leak: [WASSER.REPLACE_ME],
        # QWAT.leak_cause: [WASSER.REPLACE_ME],
        # QWAT.meter: [WASSER.REPLACE_ME],
        # QWAT.meter_reference: [WASSER.REPLACE_ME],
        # QWAT.network_element: [WASSER.REPLACE_ME],
        # QWAT.nominal_diameter: [WASSER.REPLACE_ME],
        # QWAT.object_reference: [WASSER.REPLACE_ME],
        # QWAT.overflow: [WASSER.REPLACE_ME],
        # QWAT.part: [WASSER.REPLACE_ME],
        # QWAT.part_type: [WASSER.REPLACE_ME],
        # QWAT.pipe_function: [WASSER.REPLACE_ME],
        # QWAT.pipe_installmethod: [WASSER.REPLACE_ME],
        # QWAT.pipe_material: [WASSER.REPLACE_ME],
        # QWAT.pipe_protection: [WASSER.REPLACE_ME],
        # QWAT.precision: [WASSER.REPLACE_ME],
        # QWAT.precisionalti: [WASSER.REPLACE_ME],
        # QWAT.pressurecontrol_type: [WASSER.REPLACE_ME],
        # QWAT.pressurezone: [WASSER.REPLACE_ME],
        # QWAT.printmap: [WASSER.REPLACE_ME],
        # QWAT.protectionzone: [WASSER.REPLACE_ME],
        # QWAT.protectionzone_type: [WASSER.REPLACE_ME],
        # QWAT.pump_operating: [WASSER.REPLACE_ME],
        # QWAT.pump_type: [WASSER.REPLACE_ME],
        # QWAT.remote: [WASSER.REPLACE_ME],
        # QWAT.remote_type: [WASSER.REPLACE_ME],
        # QWAT.samplingpoint: [WASSER.REPLACE_ME],
        # QWAT.source: [WASSER.REPLACE_ME],
        # QWAT.source_quality: [WASSER.REPLACE_ME],
        # QWAT.source_type: [WASSER.REPLACE_ME],
        # QWAT.status: [WASSER.REPLACE_ME],
        # QWAT.subscriber: [WASSER.REPLACE_ME],
        # QWAT.subscriber_reference: [WASSER.REPLACE_ME],
        # QWAT.subscriber_type: [WASSER.REPLACE_ME],
        # QWAT.survey_type: [WASSER.REPLACE_ME],
        # QWAT.surveypoint: [WASSER.REPLACE_ME],
        # QWAT.tank_firestorage: [WASSER.REPLACE_ME],
        # QWAT.treatment: [WASSER.REPLACE_ME],
        # QWAT.valve: [WASSER.REPLACE_ME],
        # QWAT.valve_actuation: [WASSER.REPLACE_ME],
        # QWAT.valve_function: [WASSER.REPLACE_ME],
        # QWAT.valve_type: [WASSER.REPLACE_ME],
        # QWAT.visible: [WASSER.REPLACE_ME],
        # QWAT.watertype: [WASSER.REPLACE_ME],
        # QWAT.worker: [WASSER.REPLACE_ME],
    }

