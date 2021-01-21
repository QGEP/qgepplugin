    print("Exporting QWAT.node -> WASSER.hydraulischer_knoten")
    for row in session.query(QWAT.node):
        # AVAILABLE FIELDS IN QWAT.node

        # --- node ---
        # _geometry_alt1_used, _geometry_alt2_used, _pipe_node_type, _pipe_orientation, _pipe_schema_visible, _printmaps, fk_district, fk_pressurezone, fk_printmap, geometry, geometry_alt1, geometry_alt2, id, update_geometry_alt1, update_geometry_alt2

        # --- _relations_ ---
        # fk_district_REL, fk_pressurezone_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten

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
        session.add(hydraulischer_knoten)
        print(".", end="")
    print("done")

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
        # BWREL_meter_id_fkey, BWREL_part_id_fkey, BWREL_pipe_fk_node_a, BWREL_pipe_fk_node_b, BWREL_samplingpoint_id_fkey, BWREL_subscriber_id_fkey, fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_material_REL, fk_model_inf_REL, fk_model_sup_REL, fk_object_reference_REL, fk_output_REL, fk_precision_REL, fk_precisionalti_REL, fk_pressurezone_REL, fk_provider_REL, fk_status_REL, label_1_visible_REL, label_2_visible_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten

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
        session.add(hydraulischer_knoten)
        hydrant = WASSER.hydrant(
            # FIELDS TO MAP TO WASSER.hydrant

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
        session.add(hydrant)
        print(".", end="")
    print("done")

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
        # BWREL_chamber_id_fkey, BWREL_cover_fk_installation, BWREL_installation_fk_parent, BWREL_meter_id_fkey, BWREL_part_id_fkey, BWREL_pipe_fk_node_a, BWREL_pipe_fk_node_b, BWREL_pressurecontrol_id_fkey, BWREL_samplingpoint_id_fkey, BWREL_source_id_fkey, BWREL_subscriber_id_fkey, BWREL_treatment_id_fkey, cistern1_fk_type_REL, cistern2_fk_type_REL, fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_object_reference_REL, fk_overflow_REL, fk_parent_REL, fk_precision_REL, fk_precisionalti_REL, fk_pressurezone_REL, fk_remote_REL, fk_status_REL, fk_tank_firestorage_REL, fk_watertype_REL, label_1_visible_REL, label_2_visible_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten

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
        session.add(hydraulischer_knoten)
        wasserbehaelter = WASSER.wasserbehaelter(
            # FIELDS TO MAP TO WASSER.wasserbehaelter

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
        session.add(wasserbehaelter)
        print(".", end="")
    print("done")

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
        # BWREL_chamber_id_fkey, BWREL_cover_fk_installation, BWREL_installation_fk_parent, BWREL_meter_id_fkey, BWREL_part_id_fkey, BWREL_pipe_fk_node_a, BWREL_pipe_fk_node_b, BWREL_pressurecontrol_id_fkey, BWREL_samplingpoint_id_fkey, BWREL_source_id_fkey, BWREL_subscriber_id_fkey, BWREL_treatment_id_fkey, fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_object_reference_REL, fk_parent_REL, fk_pipe_in_REL, fk_pipe_out_REL, fk_precision_REL, fk_precisionalti_REL, fk_pressurezone_REL, fk_pump_operating_REL, fk_pump_type_REL, fk_remote_REL, fk_status_REL, fk_watertype_REL, label_1_visible_REL, label_2_visible_REL

        hydraulischer_knoten = WASSER.hydraulischer_knoten(
            # FIELDS TO MAP TO WASSER.hydraulischer_knoten

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
        session.add(hydraulischer_knoten)
        foerderanlage = WASSER.foerderanlage(
            # FIELDS TO MAP TO WASSER.foerderanlage

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
        session.add(foerderanlage)
        print(".", end="")
    print("done")

    print("Exporting QWAT.pipe -> WASSER.hydraulischer_strang, WASSER.leitung")
    for row in session.query(QWAT.pipe):
        # AVAILABLE FIELDS IN QWAT.pipe

        # --- pipe ---
        # _diff_elevation, _geometry_alt1_used, _geometry_alt2_used, _length2d, _length3d, _printmaps, _schema_visible, _valve_closed, _valve_count, fk_bedding, fk_distributor, fk_district, fk_folder, fk_function, fk_installmethod, fk_locationtype, fk_material, fk_node_a, fk_node_b, fk_parent, fk_precision, fk_pressurezone, fk_printmap, fk_protection, fk_status, fk_watertype, geometry, geometry_alt1, geometry_alt2, id, label_1_text, label_1_visible, label_2_text, label_2_visible, pressure_nominal, remark, schema_force_visible, tunnel_or_bridge, update_geometry_alt1, update_geometry_alt2, year, year_end, year_rehabilitation

        # --- _relations_ ---
        # BWREL_crossing_pipe1, BWREL_crossing_pipe2, BWREL_leak_fk_pipe, BWREL_meter_fk_pipe, BWREL_part_fk_pipe, BWREL_pipe_fk_parent, BWREL_pump_fk_pipe_in, BWREL_pump_fk_pipe_out, BWREL_subscriber_fk_pipe, BWREL_valve_fk_pipe, fk_bedding_REL, fk_distributor_REL, fk_district_REL, fk_folder_REL, fk_function_REL, fk_installmethod_REL, fk_material_REL, fk_node_a_REL, fk_node_b_REL, fk_parent_REL, fk_precision_REL, fk_pressurezone_REL, fk_protection_REL, fk_status_REL, fk_watertype_REL, label_1_visible_REL, label_2_visible_REL, schema_force_visible_REL

        hydraulischer_strang = WASSER.hydraulischer_strang(
            # FIELDS TO MAP TO WASSER.hydraulischer_strang

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
        session.add(hydraulischer_strang)
        leitung = WASSER.leitung(
            # FIELDS TO MAP TO WASSER.leitung

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
        session.add(leitung)
        print(".", end="")
    print("done")

