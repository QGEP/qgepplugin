from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from .. import utils

from .model_qgep import QGEP
from .model_abwasser import ABWASSER


def import_():

    session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)

    print("Importing ABWASSER.organisation, ABWASSER.metaattribute -> QGEP.organisation")
    for row, metaattribute in session.query(ABWASSER.organisation, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN organisation

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- organisation ---
        # auid, bemerkung, bezeichnung, t_id

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        organisation = QGEP.organisation(
            # FIELDS TO MAP TO QGEP.organisation

            # --- organisation ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # uid=row.REPLACE_ME,
        )
        session.add(organisation)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.kanal, ABWASSER.metaattribute -> QGEP.channel")
    for row, metaattribute in session.query(ABWASSER.kanal, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN kanal

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- kanal ---
        # bettung_umhuellung, funktionhierarchisch, funktionhydraulisch, nutzungsart_geplant, nutzungsart_ist, rohrlaenge, spuelintervall, t_id, verbindungsart

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        channel = QGEP.channel(
            # FIELDS TO MAP TO QGEP.channel

            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- channel ---
            # bedding_encasement=row.REPLACE_ME,
            # connection_type=row.REPLACE_ME,
            # function_hierarchic=row.REPLACE_ME,
            # function_hydraulic=row.REPLACE_ME,
            # jetting_interval=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # pipe_length=row.REPLACE_ME,
            # usage_current=row.REPLACE_ME,
            # usage_planned=row.REPLACE_ME,
        )
        session.add(channel)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.normschacht, ABWASSER.metaattribute -> QGEP.manhole")
    for row, metaattribute in session.query(ABWASSER.normschacht, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN normschacht

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- normschacht ---
        # dimension1, dimension2, funktion, material, oberflaechenzulauf, t_id

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        manhole = QGEP.manhole(
            # FIELDS TO MAP TO QGEP.manhole

            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- manhole ---
            # _orientation=row.REPLACE_ME,
            # dimension1=row.REPLACE_ME,
            # dimension2=row.REPLACE_ME,
            # function=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # surface_inflow=row.REPLACE_ME,
        )
        session.add(manhole)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.einleitstelle, ABWASSER.metaattribute -> QGEP.discharge_point")
    for row, metaattribute in session.query(ABWASSER.einleitstelle, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN einleitstelle

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- einleitstelle ---
        # hochwasserkote, relevanz, t_id, terrainkote, wasserspiegel_hydraulik

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        discharge_point = QGEP.discharge_point(
            # FIELDS TO MAP TO QGEP.discharge_point

            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- discharge_point ---
            # fk_sector_water_body=row.REPLACE_ME,
            # highwater_level=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # relevance=row.REPLACE_ME,
            # terrain_level=row.REPLACE_ME,
            # upper_elevation=row.REPLACE_ME,
            # waterlevel_hydraulic=row.REPLACE_ME,
        )
        session.add(discharge_point)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.spezialbauwerk, ABWASSER.metaattribute -> QGEP.special_structure")
    for row, metaattribute in session.query(ABWASSER.spezialbauwerk, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN spezialbauwerk

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- spezialbauwerk ---
        # bypass, funktion, notueberlauf, regenbecken_anordnung, t_id

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        special_structure = QGEP.special_structure(
            # FIELDS TO MAP TO QGEP.special_structure

            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- special_structure ---
            # bypass=row.REPLACE_ME,
            # emergency_spillway=row.REPLACE_ME,
            # function=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # stormwater_tank_arrangement=row.REPLACE_ME,
            # upper_elevation=row.REPLACE_ME,
        )
        session.add(special_structure)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.versickerungsanlage, ABWASSER.metaattribute -> QGEP.infiltration_installation")
    for row, metaattribute in session.query(ABWASSER.versickerungsanlage, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN versickerungsanlage

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- versickerungsanlage ---
        # art, beschriftung, dimension1, dimension2, gwdistanz, maengel, notueberlauf, saugwagen, schluckvermoegen, t_id, versickerungswasser, wasserdichtheit, wirksameflaeche

        # --- _relations_ ---
        # betreiberref_REL, eigentuemerref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        infiltration_installation = QGEP.infiltration_installation(
            # FIELDS TO MAP TO QGEP.infiltration_installation

            # --- wastewater_structure ---
            # _bottom_label=row.REPLACE_ME,
            # _cover_label=row.REPLACE_ME,
            # _depth=row.REPLACE_ME,
            # _function_hierarchic=row.REPLACE_ME,
            # _input_label=row.REPLACE_ME,
            # _label=row.REPLACE_ME,
            # _output_label=row.REPLACE_ME,
            # _usage_current=row.REPLACE_ME,
            # accessibility=row.REPLACE_ME,
            # contract_section=row.REPLACE_ME,
            # detail_geometry_geometry=row.REPLACE_ME,
            # financing=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_main_cover=row.REPLACE_ME,
            # fk_main_wastewater_node=row.REPLACE_ME,
            # fk_operator=row.REPLACE_ME,
            # fk_owner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # gross_costs=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # inspection_interval=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location_name=row.REPLACE_ME,
            # records=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_necessity=row.REPLACE_ME,
            # replacement_value=row.REPLACE_ME,
            # rv_base_year=row.REPLACE_ME,
            # rv_construction_type=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # structure_condition=row.REPLACE_ME,
            # subsidies=row.REPLACE_ME,
            # year_of_construction=row.REPLACE_ME,
            # year_of_replacement=row.REPLACE_ME,

            # --- infiltration_installation ---
            # absorption_capacity=row.REPLACE_ME,
            # defects=row.REPLACE_ME,
            # dimension1=row.REPLACE_ME,
            # dimension2=row.REPLACE_ME,
            # distance_to_aquifer=row.REPLACE_ME,
            # effective_area=row.REPLACE_ME,
            # emergency_spillway=row.REPLACE_ME,
            # fk_aquifier=row.REPLACE_ME,
            # kind=row.REPLACE_ME,
            # labeling=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # seepage_utilization=row.REPLACE_ME,
            # upper_elevation=row.REPLACE_ME,
            # vehicle_access=row.REPLACE_ME,
            # watertightness=row.REPLACE_ME,
        )
        session.add(infiltration_installation)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.rohrprofil, ABWASSER.metaattribute -> QGEP.pipe_profile")
    for row, metaattribute in session.query(ABWASSER.rohrprofil, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN rohrprofil

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- rohrprofil ---
        # bemerkung, bezeichnung, hoehenbreitenverhaeltnis, profiltyp, t_id

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        pipe_profile = QGEP.pipe_profile(
            # FIELDS TO MAP TO QGEP.pipe_profile

            # --- pipe_profile ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # height_width_ratio=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # profile_type=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
        )
        session.add(pipe_profile)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.haltungspunkt, ABWASSER.metaattribute -> QGEP.reach_point")
    for row, metaattribute in session.query(ABWASSER.haltungspunkt, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN haltungspunkt

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- haltungspunkt ---
        # abwassernetzelementref, auslaufform, bemerkung, bezeichnung, hoehengenauigkeit, kote, lage, lage_anschluss, t_id

        # --- _relations_ ---
        # abwassernetzelementref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        reach_point = QGEP.reach_point(
            # FIELDS TO MAP TO QGEP.reach_point

            # --- reach_point ---
            # elevation_accuracy=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_networkelement=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # level=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # outlet_shape=row.REPLACE_ME,
            # position_of_connection=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # situation_geometry=row.REPLACE_ME,
        )
        session.add(reach_point)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.abwasserknoten, ABWASSER.metaattribute -> QGEP.wastewater_node")
    for row, metaattribute in session.query(ABWASSER.abwasserknoten, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN abwasserknoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwassernetzelement ---
        # abwasserbauwerkref, bemerkung, bezeichnung

        # --- abwasserknoten ---
        # lage, rueckstaukote, sohlenkote, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        wastewater_node = QGEP.wastewater_node(
            # FIELDS TO MAP TO QGEP.wastewater_node

            # --- wastewater_networkelement ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,

            # --- wastewater_node ---
            # backflow_level=row.REPLACE_ME,
            # bottom_level=row.REPLACE_ME,
            # fk_hydr_geometry=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # situation_geometry=row.REPLACE_ME,
        )
        session.add(wastewater_node)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.haltung, ABWASSER.metaattribute -> QGEP.reach")
    for row, metaattribute in session.query(ABWASSER.haltung, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN haltung

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwassernetzelement ---
        # abwasserbauwerkref, bemerkung, bezeichnung

        # --- haltung ---
        # innenschutz, laengeeffektiv, lagebestimmung, lichte_hoehe, material, nachhaltungspunktref, plangefaelle, reibungsbeiwert, reliner_art, reliner_bautechnik, reliner_material, reliner_nennweite, ringsteifigkeit, rohrprofilref, t_id, verlauf, vonhaltungspunktref, wandrauhigkeit

        # --- _relations_ ---
        # abwasserbauwerkref_REL, nachhaltungspunktref_REL, rohrprofilref_REL, vonhaltungspunktref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        reach = QGEP.reach(
            # FIELDS TO MAP TO QGEP.reach

            # --- wastewater_networkelement ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,

            # --- reach ---
            # clear_height=row.REPLACE_ME,
            # coefficient_of_friction=row.REPLACE_ME,
            # elevation_determination=row.REPLACE_ME,
            # fk_pipe_profile=row.REPLACE_ME,
            # fk_reach_point_from=row.REPLACE_ME,
            # fk_reach_point_to=row.REPLACE_ME,
            # horizontal_positioning=row.REPLACE_ME,
            # inside_coating=row.REPLACE_ME,
            # length_effective=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # progression_geometry=row.REPLACE_ME,
            # reliner_material=row.REPLACE_ME,
            # reliner_nominal_size=row.REPLACE_ME,
            # relining_construction=row.REPLACE_ME,
            # relining_kind=row.REPLACE_ME,
            # ring_stiffness=row.REPLACE_ME,
            # slope_building_plan=row.REPLACE_ME,
            # wall_roughness=row.REPLACE_ME,
        )
        session.add(reach)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.trockenwetterfallrohr, ABWASSER.metaattribute -> QGEP.dryweather_downspout")
    for row, metaattribute in session.query(ABWASSER.trockenwetterfallrohr, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN trockenwetterfallrohr

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- trockenwetterfallrohr ---
        # durchmesser, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        dryweather_downspout = QGEP.dryweather_downspout(
            # FIELDS TO MAP TO QGEP.dryweather_downspout

            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- dryweather_downspout ---
            # diameter=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
        session.add(dryweather_downspout)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.einstiegshilfe, ABWASSER.metaattribute -> QGEP.access_aid")
    for row, metaattribute in session.query(ABWASSER.einstiegshilfe, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN einstiegshilfe

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- einstiegshilfe ---
        # art, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        access_aid = QGEP.access_aid(
            # FIELDS TO MAP TO QGEP.access_aid

            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- access_aid ---
            # kind=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
        session.add(access_aid)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.trockenwetterrinne, ABWASSER.metaattribute -> QGEP.dryweather_flume")
    for row, metaattribute in session.query(ABWASSER.trockenwetterrinne, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN trockenwetterrinne

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- trockenwetterrinne ---
        # material, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        dryweather_flume = QGEP.dryweather_flume(
            # FIELDS TO MAP TO QGEP.dryweather_flume

            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- dryweather_flume ---
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
        session.add(dryweather_flume)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.deckel, ABWASSER.metaattribute -> QGEP.cover")
    for row, metaattribute in session.query(ABWASSER.deckel, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN deckel

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- deckel ---
        # deckelform, durchmesser, entlueftung, fabrikat, kote, lage, lagegenauigkeit, material, schlammeimer, t_id, verschluss

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        cover = QGEP.cover(
            # FIELDS TO MAP TO QGEP.cover

            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- cover ---
            # brand=row.REPLACE_ME,
            # cover_shape=row.REPLACE_ME,
            # diameter=row.REPLACE_ME,
            # fastening=row.REPLACE_ME,
            # level=row.REPLACE_ME,
            # material=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # positional_accuracy=row.REPLACE_ME,
            # situation_geometry=row.REPLACE_ME,
            # sludge_bucket=row.REPLACE_ME,
            # venting=row.REPLACE_ME,
        )
        session.add(cover)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.bankett, ABWASSER.metaattribute -> QGEP.benching")
    for row, metaattribute in session.query(ABWASSER.bankett, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN bankett

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- bankett ---
        # art, t_id

        # --- _relations_ ---
        # abwasserbauwerkref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        benching = QGEP.benching(
            # FIELDS TO MAP TO QGEP.benching

            # --- structure_part ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # fk_wastewater_structure=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # renovation_demand=row.REPLACE_ME,

            # --- benching ---
            # kind=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
        session.add(benching)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.untersuchung, ABWASSER.metaattribute -> QGEP.examination")
    for row, metaattribute in session.query(ABWASSER.untersuchung, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN untersuchung

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- erhaltungsereignis ---
        # abwasserbauwerkref, art, astatus, ausfuehrende_firmaref, ausfuehrender, bemerkung, bezeichnung, datengrundlage, dauer, detaildaten, ergebnis, grund, kosten, zeitpunkt

        # --- untersuchung ---
        # bispunktbezeichnung, erfassungsart, fahrzeug, geraet, haltungspunktref, inspizierte_laenge, t_id, videonummer, vonpunktbezeichnung, witterung

        # --- _relations_ ---
        # abwasserbauwerkref_REL, ausfuehrende_firmaref_REL, haltungspunktref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        examination = QGEP.examination(
            # FIELDS TO MAP TO QGEP.examination

            # --- maintenance_event ---
            # active_zone=row.REPLACE_ME,
            # base_data=row.REPLACE_ME,
            # cost=row.REPLACE_ME,
            # data_details=row.REPLACE_ME,
            # duration=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_operating_company=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # kind=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # operator=row.REPLACE_ME,
            # reason=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
            # result=row.REPLACE_ME,
            # status=row.REPLACE_ME,
            # time_point=row.REPLACE_ME,

            # --- examination ---
            # equipment=row.REPLACE_ME,
            # fk_reach_point=row.REPLACE_ME,
            # from_point_identifier=row.REPLACE_ME,
            # inspected_length=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # recording_type=row.REPLACE_ME,
            # to_point_identifier=row.REPLACE_ME,
            # vehicle=row.REPLACE_ME,
            # videonumber=row.REPLACE_ME,
            # weather=row.REPLACE_ME,
        )
        session.add(examination)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.normschachtschaden, ABWASSER.metaattribute -> QGEP.damage_manhole")
    for row, metaattribute in session.query(ABWASSER.normschachtschaden, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN normschachtschaden

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- schaden ---
        # anmerkung, ansichtsparameter, einzelschadenklasse, streckenschaden, untersuchungref, verbindung, videozaehlerstand

        # --- normschachtschaden ---
        # distanz, quantifizierung1, quantifizierung2, schachtbereich, schachtschadencode, schadenlageanfang, schadenlageende, t_id

        # --- _relations_ ---
        # untersuchungref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        damage_manhole = QGEP.damage_manhole(
            # FIELDS TO MAP TO QGEP.damage_manhole

            # --- damage ---
            # comments=row.REPLACE_ME,
            # connection=row.REPLACE_ME,
            # damage_begin=row.REPLACE_ME,
            # damage_end=row.REPLACE_ME,
            # damage_reach=row.REPLACE_ME,
            # distance=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_examination=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # quantification1=row.REPLACE_ME,
            # quantification2=row.REPLACE_ME,
            # single_damage_class=row.REPLACE_ME,
            # video_counter=row.REPLACE_ME,
            # view_parameters=row.REPLACE_ME,

            # --- damage_manhole ---
            # manhole_damage_code=row.REPLACE_ME,
            # manhole_shaft_area=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
        session.add(damage_manhole)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.kanalschaden, ABWASSER.metaattribute -> QGEP.damage_channel")
    for row, metaattribute in session.query(ABWASSER.kanalschaden, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN kanalschaden

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- schaden ---
        # anmerkung, ansichtsparameter, einzelschadenklasse, streckenschaden, untersuchungref, verbindung, videozaehlerstand

        # --- kanalschaden ---
        # distanz, kanalschadencode, quantifizierung1, quantifizierung2, schadenlageanfang, schadenlageende, t_id

        # --- _relations_ ---
        # untersuchungref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        damage_channel = QGEP.damage_channel(
            # FIELDS TO MAP TO QGEP.damage_channel

            # --- damage ---
            # comments=row.REPLACE_ME,
            # connection=row.REPLACE_ME,
            # damage_begin=row.REPLACE_ME,
            # damage_end=row.REPLACE_ME,
            # damage_reach=row.REPLACE_ME,
            # distance=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_examination=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # quantification1=row.REPLACE_ME,
            # quantification2=row.REPLACE_ME,
            # single_damage_class=row.REPLACE_ME,
            # video_counter=row.REPLACE_ME,
            # view_parameters=row.REPLACE_ME,

            # --- damage_channel ---
            # channel_damage_code=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
        )
        session.add(damage_channel)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.datentraeger, ABWASSER.metaattribute -> QGEP.data_media")
    for row, metaattribute in session.query(ABWASSER.datentraeger, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN datentraeger

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- datentraeger ---
        # art, bemerkung, bezeichnung, pfad, standort, t_id

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        data_media = QGEP.data_media(
            # FIELDS TO MAP TO QGEP.data_media

            # --- data_media ---
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # kind=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # location=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # path=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
        )
        session.add(data_media)
        print(".", end="")
    print("done")

    print("Importing ABWASSER.datei, ABWASSER.metaattribute -> QGEP.file")
    for row, metaattribute in session.query(ABWASSER.datei, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN datei

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- datei ---
        # art, bemerkung, bezeichnung, datentraegerref, klasse, objekt, relativpfad, t_id

        # --- _relations_ ---
        # datentraegerref_REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _relations_ ---
        # sia405_baseclass_metaattribute_REL

        file = QGEP.file(
            # FIELDS TO MAP TO QGEP.file

            # --- file ---
            # class=row.REPLACE_ME,
            # fk_data_media=row.REPLACE_ME,
            # fk_dataowner=row.REPLACE_ME,
            # fk_provider=row.REPLACE_ME,
            # identifier=row.REPLACE_ME,
            # kind=row.REPLACE_ME,
            # last_modification=row.REPLACE_ME,
            # obj_id=row.REPLACE_ME,
            # object=row.REPLACE_ME,
            # path_relative=row.REPLACE_ME,
            # remark=row.REPLACE_ME,
        )
        session.add(file)
        print(".", end="")
    print("done")

    session.commit()
