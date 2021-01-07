    print("Exporting QGEP.organisation -> SIA405_EAUX_USEES_2015.ORGANISATION")
    for row in session.query(QGEP.organisation):
        # AVAILABLE FIELDS FROM organisation
        # fk_dataowner, fk_provider, identifier, last_modification, obj_id, remark, uid
        # AVAILABLE FIELDS FROM _relations_
        # REF_rel_connection_object_operator, REF_rel_maintenance_event_operating_company, REF_rel_measuring_point_operator, REF_rel_od_accident_fk_dataprovider, REF_rel_od_aquifier_fk_dataprovider, REF_rel_od_bathing_area_fk_dataprovider, REF_rel_od_catchment_area_fk_dataprovider, REF_rel_od_connection_object_fk_dataowner, REF_rel_od_connection_object_fk_dataprovider, REF_rel_od_control_center_fk_dataprovider, REF_rel_od_damage_fk_dataowner, REF_rel_od_data_media_fk_dataprovider, REF_rel_od_file_fk_dataprovider, REF_rel_od_fish_pass_fk_dataowner, REF_rel_od_hazard_source_fk_dataowner, REF_rel_od_hazard_source_fk_dataprovider, REF_rel_od_hq_relation_fk_dataowner, REF_rel_od_hydr_geom_relation_fk_dataprovider, REF_rel_od_hydr_geometry_fk_dataprovider, REF_rel_od_hydraulic_char_data_fk_dataprovider, REF_rel_od_maintenance_event_fk_dataprovider, REF_rel_od_measurement_result_fk_dataowner, REF_rel_od_measurement_series_fk_dataprovider, REF_rel_od_measuring_device_fk_dataprovider, REF_rel_od_measuring_point_fk_dataowner, REF_rel_od_mechanical_pretreatment_fk_dataprovider, REF_rel_od_mutation_fk_dataowner, REF_rel_od_organisation_fk_dataprovider, REF_rel_od_overflow_char_fk_dataowner, REF_rel_od_overflow_fk_dataowner, REF_rel_od_pipe_profile_fk_dataowner, REF_rel_od_profile_geometry_fk_dataprovider, REF_rel_od_reach_point_fk_dataowner, REF_rel_od_retention_body_fk_dataowner, REF_rel_od_river_bank_fk_dataprovider, REF_rel_od_river_bed_fk_dataowner, REF_rel_od_sector_water_body_fk_dataprovider, REF_rel_od_sludge_treatment_fk_dataowner, REF_rel_od_structure_part_fk_dataowner, REF_rel_od_substance_fk_dataprovider, REF_rel_od_surface_runoff_parameters_fk_dataprovider, REF_rel_od_surface_water_bodies_fk_dataprovider, REF_rel_od_throttle_shut_off_unit_fk_dataprovider, REF_rel_od_waste_water_treatment_fk_dataprovider, REF_rel_od_wastewater_networkelement_fk_dataprovider, REF_rel_od_wastewater_structure_fk_dataowner, REF_rel_od_wastewater_structure_fk_dataprovider, REF_rel_od_wastewater_structure_symbol_fk_dataprovider, REF_rel_od_water_catchment_fk_dataprovider, REF_rel_od_water_control_structure_fk_dataowner, REF_rel_od_water_course_segment_fk_dataprovider, REF_rel_od_wwtp_energy_use_fk_dataprovider, REF_rel_od_zone_fk_dataowner, REF_rel_txt_symbol_fk_dataprovider, REF_rel_wastewater_structure_owner, organisation

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.ORGANISATION",
            {"TID": QGEP.organisation.make_tid(row.obj_id)},
        )
        # FIELDS TO MAP TO SIA405_EAUX_USEES_2015.ORGANISATION

        # --- SIA405_EAUX_USEES_2015.ORGANISATION ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME
        # ET.SubElement(e, "UID").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.cover -> SIA405_EAUX_USEES_2015.COUVERCLE")
    for row in session.query(QGEP.cover):
        # AVAILABLE FIELDS FROM cover
        # brand, cover_shape, diameter, fastening, level, material, obj_id, positional_accuracy, situation_geometry, sludge_bucket, venting
        # AVAILABLE FIELDS FROM _relations_
        # REF_rel_wastewater_structure_cover, cover_cover_shape, cover_fastening, cover_material, cover_positional_accuracy, cover_sludge_bucket, cover_venting, structure_part

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.COUVERCLE",
            {"TID": QGEP.cover.make_tid(row.obj_id)},
        )
        # FIELDS TO MAP TO SIA405_EAUX_USEES_2015.COUVERCLE

        # --- SIA405_EAUX_USEES_2015.COUVERCLE ---
        # ET.SubElement(e, "FORME_COUVERCLE").text = row.REPLACE_ME
        # ET.SubElement(e, "DIAMETRE").text = row.REPLACE_ME
        # ET.SubElement(e, "AERATION").text = row.REPLACE_ME
        # ET.SubElement(e, "FABRICANT").text = row.REPLACE_ME
        # ET.SubElement(e, "COTE").text = row.REPLACE_ME
        # ET.SubElement(e, "SITUATION").text = row.REPLACE_ME
        # ET.SubElement(e, "DETERMINATION_PLANIMETRIQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "MATERIAU").text = row.REPLACE_ME
        # ET.SubElement(e, "RAMASSE_BOUES").text = row.REPLACE_ME
        # ET.SubElement(e, "FERMETURE").text = row.REPLACE_ME

        # --- SIA405_EAUX_USEES_2015.ELEMENT_OUVRAGE ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME
        # ET.SubElement(e, "REMISE_EN_ETAT").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.manhole -> SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD")
    for row in session.query(QGEP.manhole):
        # AVAILABLE FIELDS FROM wastewater_structure
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # AVAILABLE FIELDS FROM manhole
        # _orientation, dimension1, dimension2, function, material, obj_id, surface_inflow
        # AVAILABLE FIELDS FROM _relations_
        # REF_oorel_od_discharge_point_wastewater_structure, REF_oorel_od_infiltration_installation_wastewater_structure, REF_oorel_od_special_structure_wastewater_structure, REF_oorel_od_wwtp_structure_wastewater_structure, REF_rel_maintenance_event_wastewater_structure_wastewater_structure, REF_rel_measuring_point_wastewater_structure, REF_rel_mechanical_pretreatment_wastewater_structure, REF_rel_structure_part_wastewater_structure, REF_rel_symbol_wastewater_structure, REF_rel_text_wastewater_structure, REF_rel_wastewater_networkelement_wastewater_structure, REF_rel_wastewater_structure_symbol_wastewater_structure, REF_rel_wastewater_structure_text_wastewater_structure, cover, manhole_function, manhole_material, manhole_surface_inflow, organisation, wastewater_node, wastewater_structure_accessibility, wastewater_structure_financing, wastewater_structure_renovation_necessity, wastewater_structure_rv_construction_type, wastewater_structure_status, wastewater_structure_structure_condition

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD",
            {"TID": QGEP.manhole.make_tid(row.obj_id)},
        )
        # FIELDS TO MAP TO SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD

        # --- SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD ---
        # ET.SubElement(e, "DIMENSION1").text = row.REPLACE_ME
        # ET.SubElement(e, "DIMENSION2").text = row.REPLACE_ME
        # ET.SubElement(e, "FONCTION").text = row.REPLACE_ME
        # ET.SubElement(e, "MATERIAU").text = row.REPLACE_ME
        # ET.SubElement(e, "ARRIVEE_EAUX_SUP").text = row.REPLACE_ME

        # --- SIA405_EAUX_USEES_2015.OUVRAGE_RESEAU_AS ---
        # ET.SubElement(e, "DOSSIER").text = row.REPLACE_ME
        # ET.SubElement(e, "ANNEE_DE_CONSTRUCTION").text = row.REPLACE_ME
        # ET.SubElement(e, "ETAT_CONSTRUCTIF").text = row.REPLACE_ME
        # ET.SubElement(e, "LOT_CONSTRUCTION").text = row.REPLACE_ME
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME
        # ET.SubElement(e, "COUTS_BRUTS").text = row.REPLACE_ME
        # ET.SubElement(e, "GEOMETRIE_DETAILLEE").text = row.REPLACE_ME
        # ET.SubElement(e, "ANNEE_DE_REMPLACEMENT").text = row.REPLACE_ME
        # ET.SubElement(e, "FINANCEMENT").text = row.REPLACE_ME
        # ET.SubElement(e, "INTERVALLE_INSPECTION").text = row.REPLACE_ME
        # ET.SubElement(e, "NECESSITE_ASSAINIR").text = row.REPLACE_ME
        # ET.SubElement(e, "LIEU_DIT").text = row.REPLACE_ME
        # ET.SubElement(e, "ETAT").text = row.REPLACE_ME
        # ET.SubElement(e, "SUBVENTIONS").text = row.REPLACE_ME
        # ET.SubElement(e, "VR_ANNEE_REFERENCE").text = row.REPLACE_ME
        # ET.SubElement(e, "VR_TYPE_CONSTRUCTION").text = row.REPLACE_ME
        # ET.SubElement(e, "VALEUR_REMPLACEMENT").text = row.REPLACE_ME
        # ET.SubElement(e, "ACCES").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

