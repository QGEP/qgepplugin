from functools import lru_cache

from sqlalchemy.orm import Session
from sqlalchemy import inspect
from geoalchemy2.functions import ST_Transform, ST_Force2D, ST_Force3D
import warnings

from .. import utils

from .model_qgep import QGEP
from .model_abwasser import ABWASSER


def import_(precommit_callback=None):
    """
    Imports data from the ili2pg model into the QGEP model.

    Args:
        precommit_callback: optional callable that gets invoked with the sqlalchemy's session,
                            allowing for a GUI to  filter objects before committing. It MUST either
                            commit or rollback and close the session.
    """

    # We use two different sessions for reading and writing so it's easier to
    # review imports and to keep the door open to getting data from another
    # connection / database type.
    abwasser_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    qgep_session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)

    def get_vl_code(vl_table, value):
        """
        Gets a value list code from the value_de name. Returns None and a warning if not found.
        """
        # TODO : memoize (and get the whole table at once) to improve N+1 performance issue
        # TODO : return "other" (or other applicable value) rather than None, or even throwing an exception, would probably be better
        row = qgep_session.query(vl_table).filter(vl_table.value_de == value).first()
        if row is None:
            warnings.warn(f'⚠️ Could not find value `{value}` in value list "{vl_table.__table__.schema}.{vl_table.__name__}". Setting to None instead.')
            return None
        return row.code

    def get_pk(relation):
        """
        Returns the primary key for a relation
        """
        if relation is None:
            return None
        return relation.obj_id

    @lru_cache(maxsize=None)
    def get_or_create_organisation(name):
        """
        Gets an organisation ID from it's name (and creates an entry if not existing)
        """
        instance = qgep_session.query(QGEP.organisation).filter(QGEP.organisation.identifier == name).first()
        if instance:
            return instance.obj_id
        else:
            instance = QGEP.organisation(identifier=name)
            qgep_session.add(instance)
            return instance.obj_id


    def metaattribute_common(metaattribute):
        """
        Common parameters for metaattributes
        """
        return {
            "fk_dataowner": get_or_create_organisation(metaattribute.datenherr),
            "fk_provider": get_or_create_organisation(metaattribute.datenlieferant),
            "last_modification": metaattribute.letzte_aenderung,
        }

    def base_common(row):
        """
        Returns common attributes for base
        """
        return {
            "obj_id": row.obj_id,
        }

    def wastewater_structure_common(row):
        """
        Returns common attributes for wastewater_structure
        """
        return {
            "accessibility": get_vl_code(QGEP.wastewater_structure_accessibility, row.zugaenglichkeit),
            # "contract_section": row.REPLACE_ME,  # TODO : not sure, is it akten or baulos ?
            "detail_geometry_geometry": ST_Force3D(row.detailgeometrie),
            "financing": get_vl_code(QGEP.wastewater_structure_financing, row.finanzierung),
            # "fk_main_cover": row.REPLACE_ME,  # TODO : NOT MAPPED, but I think this is not standard SIA405 ?
            # "fk_main_wastewater_node": row.REPLACE_ME,  # TODO : NOT MAPPED, but I think this is not standard SIA405 ?
            "fk_operator": get_pk(row.betreiberref__REL),
            "fk_owner": get_pk(row.eigentuemerref__REL),
            "gross_costs": row.bruttokosten,
            "identifier": row.bezeichnung,
            "inspection_interval": row.inspektionsintervall,
            "location_name": row.standortname,
            # "records": row.REPLACE_ME,  # TODO : not sure, is it akten or baulos ?
            "remark": row.bemerkung,
            "renovation_necessity": get_vl_code(QGEP.wastewater_structure_renovation_necessity, row.sanierungsbedarf),
            "replacement_value": row.wiederbeschaffungswert,
            "rv_base_year": row.wbw_basisjahr,
            "rv_construction_type": get_vl_code(QGEP.wastewater_structure_rv_construction_type, row.wbw_bauart),
            "status": get_vl_code(QGEP.wastewater_structure_status, row.astatus),
            "structure_condition": get_vl_code(QGEP.wastewater_structure_structure_condition, row.baulicherzustand),
            "subsidies": row.subventionen,
            "year_of_construction": row.baujahr,
            "year_of_replacement": row.ersatzjahr,
        }

    def wastewater_network_element_common(row):
        """
        Returns common attributes for network_element
        """
        return {
            "fk_wastewater_structure": get_pk(row.abwasserbauwerkref__REL),
            "identifier": row.bezeichnung,
            "remark": row.bemerkung,
        }


    print("Importing ABWASSER.organisation, ABWASSER.metaattribute -> QGEP.organisation")
    for row, metaattribute in abwasser_session.query(ABWASSER.organisation, ABWASSER.metaattribute).join(ABWASSER.metaattribute):
        # TODO : this may create multiple copies of the same organisation in certain circumstances.
        # Ideally we don't want to flush so we can review organisation creation like any other
        # data before commiting.
        # See corresponding test case : tests.TestRegressions.test_self_referencing_organisation

        organisation = QGEP.organisation(
            # --- organisation ---
            fk_dataowner=get_or_create_organisation(metaattribute.datenherr),
            fk_provider=get_or_create_organisation(metaattribute.datenlieferant),
            identifier=row.bezeichnung,
            last_modification=metaattribute.letzte_aenderung,
            obj_id=row.obj_id,
            remark=row.bemerkung,
            uid=row.auid,
        )
        qgep_session.add(organisation)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.kanal, ABWASSER.metaattribute -> QGEP.channel")
    for row, metaattribute in abwasser_session.query(ABWASSER.kanal, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN kanal

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- kanal ---
        # bettung_umhuellung, funktionhierarchisch, funktionhydraulisch, nutzungsart_geplant, nutzungsart_ist, rohrlaenge, spuelintervall, t_id, verbindungsart

        # --- _bwrel_ ---
        # abwassernetzelement__BWREL_abwasserbauwerkref, bauwerksteil__BWREL_abwasserbauwerkref, erhaltungsereignis__BWREL_abwasserbauwerkref, haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, sia405_symbolpos__BWREL_abwasserbauwerkref, sia405_textpos__BWREL_abwasserbauwerkref, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # betreiberref__REL, eigentuemerref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        channel = QGEP.channel(

            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- wastewater_structure ---
            **wastewater_structure_common(row),

            # --- channel ---
            bedding_encasement=get_vl_code(QGEP.channel_bedding_encasement, row.bettung_umhuellung),
            connection_type=get_vl_code(QGEP.channel_connection_type, row.verbindungsart),
            function_hierarchic=get_vl_code(QGEP.channel_function_hierarchic, row.funktionhierarchisch),
            function_hydraulic=get_vl_code(QGEP.channel_function_hydraulic, row.funktionhydraulisch),
            jetting_interval=row.spuelintervall,
            pipe_length=row.rohrlaenge,
            usage_current=get_vl_code(QGEP.channel_usage_current, row.nutzungsart_ist),
            usage_planned=get_vl_code(QGEP.channel_usage_planned, row.nutzungsart_geplant),
        )
        qgep_session.add(channel)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.normschacht, ABWASSER.metaattribute -> QGEP.manhole")
    for row, metaattribute in abwasser_session.query(ABWASSER.normschacht, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN normschacht

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- normschacht ---
        # dimension1, dimension2, funktion, material, oberflaechenzulauf, t_id

        # --- _bwrel_ ---
        # abwassernetzelement__BWREL_abwasserbauwerkref, bauwerksteil__BWREL_abwasserbauwerkref, erhaltungsereignis__BWREL_abwasserbauwerkref, haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, sia405_symbolpos__BWREL_abwasserbauwerkref, sia405_textpos__BWREL_abwasserbauwerkref, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # betreiberref__REL, eigentuemerref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        manhole = QGEP.manhole(
            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- wastewater_structure ---
            **wastewater_structure_common(row),

            # --- manhole ---
            # _orientation=row.REPLACE_ME,
            dimension1=row.dimension1,
            dimension2=row.dimension2,
            function=get_vl_code(QGEP.manhole_function, row.funktion),
            material=get_vl_code(QGEP.manhole_material, row.material),
            surface_inflow=get_vl_code(QGEP.manhole_surface_inflow, row.oberflaechenzulauf),
        )
        qgep_session.add(manhole)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.einleitstelle, ABWASSER.metaattribute -> QGEP.discharge_point")
    for row, metaattribute in abwasser_session.query(ABWASSER.einleitstelle, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN einleitstelle

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- einleitstelle ---
        # hochwasserkote, relevanz, t_id, terrainkote, wasserspiegel_hydraulik

        # --- _bwrel_ ---
        # abwassernetzelement__BWREL_abwasserbauwerkref, bauwerksteil__BWREL_abwasserbauwerkref, erhaltungsereignis__BWREL_abwasserbauwerkref, haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, sia405_symbolpos__BWREL_abwasserbauwerkref, sia405_textpos__BWREL_abwasserbauwerkref, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # betreiberref__REL, eigentuemerref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        discharge_point = QGEP.discharge_point(
            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- wastewater_structure ---
            **wastewater_structure_common(row),

            # --- discharge_point ---
            # fk_sector_water_body=row.REPLACE_ME, # TODO : NOT MAPPED
            highwater_level=row.hochwasserkote,
            relevance=get_vl_code(QGEP.discharge_point_relevance, row.relevanz),
            terrain_level=row.terrainkote,
            # upper_elevation=row.REPLACE_ME, # TODO : NOT MAPPED
            waterlevel_hydraulic=row.wasserspiegel_hydraulik,
        )
        qgep_session.add(discharge_point)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.spezialbauwerk, ABWASSER.metaattribute -> QGEP.special_structure")
    for row, metaattribute in abwasser_session.query(ABWASSER.spezialbauwerk, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN spezialbauwerk

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- spezialbauwerk ---
        # bypass, funktion, notueberlauf, regenbecken_anordnung, t_id

        # --- _bwrel_ ---
        # abwassernetzelement__BWREL_abwasserbauwerkref, bauwerksteil__BWREL_abwasserbauwerkref, erhaltungsereignis__BWREL_abwasserbauwerkref, haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, sia405_symbolpos__BWREL_abwasserbauwerkref, sia405_textpos__BWREL_abwasserbauwerkref, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # betreiberref__REL, eigentuemerref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        special_structure = QGEP.special_structure(
            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- wastewater_structure ---
            **wastewater_structure_common(row),

            # --- special_structure ---
            bypass=get_vl_code(QGEP.special_structure_bypass, row.bypass),
            emergency_spillway=get_vl_code(QGEP.special_structure_emergency_spillway, row.notueberlauf),
            function=get_vl_code(QGEP.special_structure_function, row.funktion),
            stormwater_tank_arrangement=get_vl_code(QGEP.special_structure_stormwater_tank_arrangement, row.regenbecken_anordnung),
            # upper_elevation=row.REPLACE_ME,   # TODO : NOT MAPPED
        )
        qgep_session.add(special_structure)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.versickerungsanlage, ABWASSER.metaattribute -> QGEP.infiltration_installation")
    for row, metaattribute in abwasser_session.query(ABWASSER.versickerungsanlage, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN versickerungsanlage

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwasserbauwerk ---
        # akten, astatus, baujahr, baulicherzustand, baulos, bemerkung, betreiberref, bezeichnung, bruttokosten, detailgeometrie, eigentuemerref, ersatzjahr, finanzierung, inspektionsintervall, sanierungsbedarf, standortname, subventionen, wbw_basisjahr, wbw_bauart, wiederbeschaffungswert, zugaenglichkeit

        # --- versickerungsanlage ---
        # art, beschriftung, dimension1, dimension2, gwdistanz, maengel, notueberlauf, saugwagen, schluckvermoegen, t_id, versickerungswasser, wasserdichtheit, wirksameflaeche

        # --- _bwrel_ ---
        # abwassernetzelement__BWREL_abwasserbauwerkref, bauwerksteil__BWREL_abwasserbauwerkref, erhaltungsereignis__BWREL_abwasserbauwerkref, haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, sia405_symbolpos__BWREL_abwasserbauwerkref, sia405_textpos__BWREL_abwasserbauwerkref, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # betreiberref__REL, eigentuemerref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        infiltration_installation = QGEP.infiltration_installation(
            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- wastewater_structure ---
            **wastewater_structure_common(row),

            # --- infiltration_installation ---
            absorption_capacity=row.schluckvermoegen,
            defects=get_vl_code(QGEP.infiltration_installation_defects, row.maengel),
            dimension1=row.dimension1,
            dimension2=row.dimension2,
            distance_to_aquifer=row.gwdistanz,
            effective_area=row.wirksameflaeche,
            emergency_spillway=get_vl_code(QGEP.infiltration_installation_emergency_spillway, row.notueberlauf),
            # fk_aquifier=row.REPLACE_ME,  # TODO : NOT MAPPED
            kind=get_vl_code(QGEP.infiltration_installation_kind, row.art),
            labeling=get_vl_code(QGEP.infiltration_installation_labeling, row.beschriftung),
            seepage_utilization=get_vl_code(QGEP.infiltration_installation_seepage_utilization, row.versickerungswasser),
            # upper_elevation=row.REPLACE_ME,  # TODO : NOT MAPPED
            vehicle_access=get_vl_code(QGEP.infiltration_installation_vehicle_access, row.saugwagen),
            watertightness=get_vl_code(QGEP.infiltration_installation_watertightness, row.wasserdichtheit),
        )
        qgep_session.add(infiltration_installation)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.rohrprofil, ABWASSER.metaattribute -> QGEP.pipe_profile")
    for row, metaattribute in abwasser_session.query(ABWASSER.rohrprofil, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN rohrprofil

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- rohrprofil ---
        # bemerkung, bezeichnung, hoehenbreitenverhaeltnis, profiltyp, t_id

        # --- _bwrel_ ---
        # haltung__BWREL_rohrprofilref, haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        pipe_profile = QGEP.pipe_profile(
            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- pipe_profile ---
            height_width_ratio=row.hoehenbreitenverhaeltnis,
            identifier=row.bezeichnung,
            profile_type=get_vl_code(QGEP.pipe_profile_profile_type, row.profiltyp),
            remark=row.bemerkung,
        )
        qgep_session.add(pipe_profile)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.haltungspunkt, ABWASSER.metaattribute -> QGEP.reach_point")
    for row, metaattribute in abwasser_session.query(ABWASSER.haltungspunkt, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN haltungspunkt

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- haltungspunkt ---
        # abwassernetzelementref, auslaufform, bemerkung, bezeichnung, hoehengenauigkeit, kote, lage, lage_anschluss, t_id

        # --- _bwrel_ ---
        # haltung__BWREL_nachhaltungspunktref, haltung__BWREL_vonhaltungspunktref, haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id, untersuchung__BWREL_haltungspunktref

        # --- _rel_ ---
        # abwassernetzelementref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        reach_point = QGEP.reach_point(
            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- reach_point ---
            elevation_accuracy=get_vl_code(QGEP.reach_point_elevation_accuracy, row.hoehengenauigkeit),
            fk_wastewater_networkelement=get_pk(row.abwassernetzelementref__REL),  # this fails for now, but probably only because we flush too soon
            identifier=row.bezeichnung,
            level=row.kote,
            outlet_shape=get_vl_code(QGEP.reach_point_outlet_shape, row.hoehengenauigkeit),
            position_of_connection=row.lage_anschluss,
            remark=row.bemerkung,
            situation_geometry=ST_Force3D(row.lage),
        )
        qgep_session.add(reach_point)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.abwasserknoten, ABWASSER.metaattribute -> QGEP.wastewater_node")
    for row, metaattribute in abwasser_session.query(ABWASSER.abwasserknoten, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN abwasserknoten

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwassernetzelement ---
        # abwasserbauwerkref, bemerkung, bezeichnung

        # --- abwasserknoten ---
        # lage, rueckstaukote, sohlenkote, t_id

        # --- _bwrel_ ---
        # haltung_alternativverlauf__BWREL_t_id, haltungspunkt__BWREL_abwassernetzelementref, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # abwasserbauwerkref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

        wastewater_node = QGEP.wastewater_node(
            **base_common(row),
            **metaattribute_common(metaattribute),

            # --- wastewater_networkelement ---
            **wastewater_network_element_common(row),

            # --- wastewater_node ---
            # fk_hydr_geometry=row.REPLACE_ME,  # TODO : NOT MAPPED
            backflow_level=row.rueckstaukote,
            bottom_level=row.sohlenkote,
            situation_geometry=row.lage,
        )
        qgep_session.add(wastewater_node)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.haltung, ABWASSER.metaattribute -> QGEP.reach")
    for row, metaattribute in abwasser_session.query(ABWASSER.haltung, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN haltung

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- abwassernetzelement ---
        # abwasserbauwerkref, bemerkung, bezeichnung

        # --- haltung ---
        # innenschutz, laengeeffektiv, lagebestimmung, lichte_hoehe, material, nachhaltungspunktref, plangefaelle, reibungsbeiwert, reliner_art, reliner_bautechnik, reliner_material, reliner_nennweite, ringsteifigkeit, rohrprofilref, t_id, verlauf, vonhaltungspunktref, wandrauhigkeit

        # --- _bwrel_ ---
        # haltung_alternativverlauf__BWREL_haltungref, haltung_alternativverlauf__BWREL_t_id, haltungspunkt__BWREL_abwassernetzelementref, metaattribute__BWREL_sia405_baseclass_metaattribute, sia405_textpos__BWREL_haltungref, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # abwasserbauwerkref__REL, nachhaltungspunktref__REL, rohrprofilref__REL, vonhaltungspunktref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

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
        qgep_session.add(reach)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.trockenwetterfallrohr, ABWASSER.metaattribute -> QGEP.dryweather_downspout")
    for row, metaattribute in abwasser_session.query(ABWASSER.trockenwetterfallrohr, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN trockenwetterfallrohr

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- trockenwetterfallrohr ---
        # durchmesser, t_id

        # --- _bwrel_ ---
        # haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # abwasserbauwerkref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

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
        qgep_session.add(dryweather_downspout)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.einstiegshilfe, ABWASSER.metaattribute -> QGEP.access_aid")
    for row, metaattribute in abwasser_session.query(ABWASSER.einstiegshilfe, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN einstiegshilfe

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- einstiegshilfe ---
        # art, t_id

        # --- _bwrel_ ---
        # haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # abwasserbauwerkref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

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
        qgep_session.add(access_aid)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.trockenwetterrinne, ABWASSER.metaattribute -> QGEP.dryweather_flume")
    for row, metaattribute in abwasser_session.query(ABWASSER.trockenwetterrinne, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN trockenwetterrinne

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- trockenwetterrinne ---
        # material, t_id

        # --- _bwrel_ ---
        # haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # abwasserbauwerkref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

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
        qgep_session.add(dryweather_flume)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.deckel, ABWASSER.metaattribute -> QGEP.cover")
    for row, metaattribute in abwasser_session.query(ABWASSER.deckel, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN deckel

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- deckel ---
        # deckelform, durchmesser, entlueftung, fabrikat, kote, lage, lagegenauigkeit, material, schlammeimer, t_id, verschluss

        # --- _bwrel_ ---
        # haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # abwasserbauwerkref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

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
        qgep_session.add(cover)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.bankett, ABWASSER.metaattribute -> QGEP.benching")
    for row, metaattribute in abwasser_session.query(ABWASSER.bankett, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        # AVAILABLE FIELDS IN bankett

        # --- baseclass ---
        # t_ili_tid, t_type

        # --- sia405_baseclass ---
        # obj_id

        # --- bauwerksteil ---
        # abwasserbauwerkref, bemerkung, bezeichnung, instandstellung

        # --- bankett ---
        # art, t_id

        # --- _bwrel_ ---
        # haltung_alternativverlauf__BWREL_t_id, metaattribute__BWREL_sia405_baseclass_metaattribute, symbolpos__BWREL_t_id, textpos__BWREL_t_id

        # --- _rel_ ---
        # abwasserbauwerkref__REL

        # AVAILABLE FIELDS IN metaattribute

        # --- metaattribute ---
        # datenherr, datenlieferant, letzte_aenderung, sia405_baseclass_metaattribute, t_id, t_seq

        # --- _rel_ ---
        # sia405_baseclass_metaattribute__REL

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
        qgep_session.add(benching)
        print(".", end="")
    print("done")
    qgep_session.flush()

    ########################################
    # VSA_KEK classes
    ########################################

    print("Importing ABWASSER.untersuchung, ABWASSER.metaattribute -> QGEP.examination")
    for row, metaattribute in abwasser_session.query(ABWASSER.untersuchung, ABWASSER.metaattribute).join(ABWASSER.metaattribute):

        warnings.warn("QGEP examination.active_zone has no equivalent in the interlis model. This field will be null.")
        examination = QGEP.examination(
            # --- maintenance_event ---
            # active_zone=row.REPLACE_ME,  # TODO : found no matching field for this in interlis, confirm this is ok
            base_data=row.datengrundlage,
            cost=row.kosten,
            data_details=row.detaildaten,
            duration=row.dauer,
            fk_dataowner=get_or_create_organisation(metaattribute.datenherr),
            fk_provider=get_or_create_organisation(metaattribute.datenlieferant),
            fk_operating_company=row.ausfuehrende_firmaref__REL.obj_id,
            identifier=row.bezeichnung,
            kind=get_vl_code(QGEP.maintenance_event_kind, row.art),
            last_modification=metaattribute.letzte_aenderung,
            operator=row.ausfuehrender,
            reason=row.grund,
            remark=row.bemerkung,
            result=row.ergebnis,
            status=get_vl_code(QGEP.maintenance_event_status, row.astatus),
            time_point=row.zeitpunkt,

            # --- examination ---
            equipment=row.geraet,
            fk_reach_point=row.haltungspunktref__REL.obj_id if row.haltungspunktref__REL else None,
            from_point_identifier=row.vonpunktbezeichnung,
            inspected_length=row.inspizierte_laenge,
            obj_id=row.obj_id,
            recording_type=get_vl_code(QGEP.examination_recording_type, row.erfassungsart),
            to_point_identifier=row.bispunktbezeichnung,
            vehicle=row.fahrzeug,
            videonumber=row.videonummer,
            weather=get_vl_code(QGEP.examination_weather, row.witterung),
        )
        qgep_session.add(examination)

        # In QGEP, relation between maintenance_event and wastewater_structure is done with
        # an association table instead of a foreign key on maintenance_event.
        # NOTE : this may change in future versions of VSA_KEK
        if row.abwasserbauwerkref:
            # TODO : for now, this will not work unless the related wastewaterstructures are part of the import,
            # as ili2pg imports dangling references as NULL.
            # The day ili2pg works, we probably need to double-check whether the referenced wastewater structure exists prior
            # to creating this association.
            # Soft matching based on from/to_point_identifier will be done in the GUI data checking process.
            exam_to_wastewater_structure = QGEP.re_maintenance_event_wastewater_structure(
                fk_wastewater_structure=row.abwasserbauwerkref,
                fk_maintenance_event=row.obj_id,
            )
            qgep_session.add(exam_to_wastewater_structure)

        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.normschachtschaden, ABWASSER.metaattribute -> QGEP.damage_manhole")
    for row, metaattribute in abwasser_session.query(ABWASSER.normschachtschaden, ABWASSER.metaattribute).join(ABWASSER.metaattribute):
        # Note : in QGEP, some attributes are on the base damage class,
        # while they are on the normschachtschaden/kanalschaden subclasses
        # in the ili2pg mode.
        # Concerned attributes : distanz, quantifizierung1, quantifizierung2, schadenlageanfang, schadenlageende

        damage_manhole = QGEP.damage_manhole(
            # --- damage ---
            comments=row.anmerkung,
            connection=get_vl_code(QGEP.damage_connection, row.verbindung),
            damage_begin=row.schadenlageanfang,
            damage_end=row.schadenlageende,
            damage_reach=row.streckenschaden,
            distance=row.distanz,
            fk_dataowner=get_or_create_organisation(metaattribute.datenherr),
            fk_examination=row.untersuchungref__REL.obj_id if row.untersuchungref__REL else None,
            fk_provider=get_or_create_organisation(metaattribute.datenlieferant),
            last_modification=metaattribute.letzte_aenderung,
            quantification1=row.quantifizierung1,
            quantification2=row.quantifizierung2,
            single_damage_class=get_vl_code(QGEP.damage_single_damage_class, row.einzelschadenklasse),
            video_counter=row.videozaehlerstand,
            view_parameters=row.ansichtsparameter,

            # --- damage_manhole ---
            manhole_damage_code=get_vl_code(QGEP.damage_manhole_manhole_damage_code, row.schachtschadencode),
            manhole_shaft_area=get_vl_code(QGEP.damage_manhole_manhole_shaft_area, row.schachtbereich),
            obj_id=row.obj_id,
        )
        qgep_session.add(damage_manhole)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.kanalschaden, ABWASSER.metaattribute -> QGEP.damage_channel")
    for row, metaattribute in abwasser_session.query(ABWASSER.kanalschaden, ABWASSER.metaattribute).join(ABWASSER.metaattribute):
        # Note : in QGEP, some attributes are on the base damage class,
        # while they are on the normschachtschaden/kanalschaden subclasses
        # in the ili2pg mode.
        # Concerned attributes : distanz, quantifizierung1, quantifizierung2, schadenlageanfang, schadenlageende

        damage_channel = QGEP.damage_channel(
            # --- damage ---
            comments=row.anmerkung,
            connection=get_vl_code(QGEP.damage_connection, row.verbindung),
            damage_begin=row.schadenlageanfang,
            damage_end=row.schadenlageende,
            damage_reach=row.streckenschaden,
            distance=row.distanz,
            fk_dataowner=get_or_create_organisation(metaattribute.datenherr),
            fk_examination=row.untersuchungref__REL.obj_id if row.untersuchungref__REL else None,
            fk_provider=get_or_create_organisation(metaattribute.datenlieferant),
            last_modification=metaattribute.letzte_aenderung,
            quantification1=row.quantifizierung1,
            quantification2=row.quantifizierung2,
            single_damage_class=get_vl_code(QGEP.damage_single_damage_class, row.einzelschadenklasse),
            video_counter=row.videozaehlerstand,
            view_parameters=row.ansichtsparameter,

            # --- damage_channel ---
            channel_damage_code=get_vl_code(QGEP.damage_channel_channel_damage_code, row.kanalschadencode),
            obj_id=row.obj_id,
        )
        qgep_session.add(damage_channel)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.datentraeger, ABWASSER.metaattribute -> QGEP.data_media")
    for row, metaattribute in abwasser_session.query(ABWASSER.datentraeger, ABWASSER.metaattribute).join(ABWASSER.metaattribute):
        data_media = QGEP.data_media(
            # --- data_media ---
            fk_dataowner=get_or_create_organisation(metaattribute.datenherr),
            fk_provider=get_or_create_organisation(metaattribute.datenlieferant),
            identifier=row.bezeichnung,
            kind=get_vl_code(QGEP.data_media_kind, row.art),
            last_modification=metaattribute.letzte_aenderung,
            location=row.standort,
            obj_id=row.obj_id,
            path=row.pfad,
            remark=row.bemerkung,
        )
        qgep_session.add(data_media)
        print(".", end="")
    print("done")
    qgep_session.flush()

    print("Importing ABWASSER.datei, ABWASSER.metaattribute -> QGEP.file")
    for row, metaattribute in abwasser_session.query(ABWASSER.datei, ABWASSER.metaattribute).join(ABWASSER.metaattribute):
        file = QGEP.file(
            # --- file ---
            **{"class": get_vl_code(QGEP.file_class, row.klasse)},  # equivalent to class=get_vl_code(QGEP.file_class, row.klasse), because class is a python keyword
            fk_data_media=row.datentraegerref__REL.obj_id,
            fk_dataowner=get_or_create_organisation(metaattribute.datenherr),
            fk_provider=get_or_create_organisation(metaattribute.datenlieferant),
            identifier=row.bezeichnung,
            kind=get_vl_code(QGEP.file_kind, row.art),
            last_modification=metaattribute.letzte_aenderung,
            obj_id=row.obj_id,
            object=row.objekt,
            path_relative=row.relativpfad,
            remark=row.bemerkung,
        )
        qgep_session.add(file)
        print(".", end="")
    print("done")
    qgep_session.flush()

    # Calling the precommit callback if provided, allowing to filter before final import
    if precommit_callback:
        precommit_callback(qgep_session)
    else:
        qgep_session.commit()
        qgep_session.close()
    abwasser_session.close()
