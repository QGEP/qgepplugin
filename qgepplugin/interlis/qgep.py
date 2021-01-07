from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

import xml.etree.ElementTree as ET
import xml.dom.minidom


from . import utils
from . import config

from .datamodels.qgep import Classes as QGEP
from .datamodels.wasser2015 import Classes as WASSER

###############################################
# Actual export (see qgep_generator to pregenerate some of this code)
###############################################

MAPPING = {
    'wastewater_structure': {
        'accessibility': {
            None: None,
            3444: 'ueberdeckt',
            3447: 'unbekannt',
            3446: 'unzugaenglich',
            3445: 'zugaenglich',
        }
    },
    'manhole': {
        'function': {
            None: None,
            4532: 'Absturzbauwerk',
            5344: 'andere',
            4533: 'Be_Entlueftung',
            3267: 'Dachwasserschacht',
            3266: 'Einlaufschacht',
            3472: 'Entwaesserungsrinne',
            228: 'Geleiseschacht',
            204: 'Kontrollschacht',
            1008: 'Oelabscheider',
            4536: 'Pumpwerk',
            5346: 'Regenueberlauf',
            2742: 'Schlammsammler',
            5347: 'Schwimmstoffabscheider',
            4537: 'Spuelschacht',
            4798: 'Trennbauwerk',
            5345: 'unbekannt',
        },
    },
}

def export():

    root = ET.Element('TRANSFER')
    headersection = ET.SubElement(root, 'HEADERSECTION')
    datasection = ET.SubElement(root, 'DATASECTION')

    session = Session(utils.create_engine())

    print("Exporting QGEP.organisation -> SIA405_EAUX_USEES_2015.ORGANISATION")
    for row in session.query(QGEP.organisation):
        # AVAILABLE FIELDS FROM organisation
        # fk_dataowner, fk_provider, identifier, last_modification, obj_id, remark, uid
        # AVAILABLE FIELDS FROM _relations_
        # REL_rel_od_organisation_fk_dataowner, REL_rel_od_organisation_fk_dataprovider

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.ORGANISATION",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.ORGANISATION ---
        ET.SubElement(e, "REMARQUE").text = row.remark
        ET.SubElement(e, "DESIGNATION").text = row.identifier
        ET.SubElement(e, "UID").text = row.obj_id

        # --- SIA405_Base_f.SIA405_BaseClass ---
        ET.SubElement(e, "OBJ_ID").text = row.obj_id
        meta_root = ET.SubElement(e, "METAATTRIBUTS")
        meta = ET.SubElement(meta_root, "SIA405_Base.METAATTRIBUTS")
        if row.fk_dataowner_REL:
            ET.SubElement(meta, "MAITRE_DES_DONNEES").text = row.fk_dataowner_REL.identifier
        if row.fk_provider_REL:
            ET.SubElement(meta, "FOURNISSEUR_DES_DONNEES").text = row.fk_provider_REL.identifier
        ET.SubElement(meta, "DERNIERE_MODIFICATION").text = str(row.last_modification)

        print(".", end="")
    print("done")

    print("Exporting QGEP.wastewater_structure -> SIA405_EAUX_USEES_2015.OUVRAGE_RESEAU_AS")
    for row in session.query(QGEP.wastewater_structure):
        # AVAILABLE FIELDS FROM wastewater_structure
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, obj_id, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_oorel_od_discharge_point_wastewater_structure, BWREL_oorel_od_infiltration_installation_wastewater_structure, BWREL_oorel_od_special_structure_wastewater_structure, BWREL_oorel_od_wwtp_structure_wastewater_structure, BWREL_rel_maintenance_event_wastewater_structure_wastewater_structure, BWREL_rel_measuring_point_wastewater_structure, BWREL_rel_mechanical_pretreatment_wastewater_structure, BWREL_rel_structure_part_wastewater_structure, BWREL_rel_symbol_wastewater_structure, BWREL_rel_text_wastewater_structure, BWREL_rel_wastewater_networkelement_wastewater_structure, BWREL_rel_wastewater_structure_symbol_wastewater_structure, BWREL_rel_wastewater_structure_text_wastewater_structure, accessibility_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.OUVRAGE_RESEAU_AS",
            {"TID": row.obj_id},
        )

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

    print("Exporting QGEP.channel -> SIA405_EAUX_USEES_2015.CANALISATION")
    for row in session.query(QGEP.channel):
        # AVAILABLE FIELDS FROM wastewater_structure
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # AVAILABLE FIELDS FROM channel
        # bedding_encasement, connection_type, function_hierarchic, function_hydraulic, jetting_interval, obj_id, pipe_length, usage_current, usage_planned
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_oorel_od_discharge_point_wastewater_structure, BWREL_oorel_od_infiltration_installation_wastewater_structure, BWREL_oorel_od_special_structure_wastewater_structure, BWREL_oorel_od_wwtp_structure_wastewater_structure, BWREL_rel_maintenance_event_wastewater_structure_wastewater_structure, BWREL_rel_measuring_point_wastewater_structure, BWREL_rel_mechanical_pretreatment_wastewater_structure, BWREL_rel_structure_part_wastewater_structure, BWREL_rel_symbol_wastewater_structure, BWREL_rel_text_wastewater_structure, BWREL_rel_wastewater_networkelement_wastewater_structure, BWREL_rel_wastewater_structure_symbol_wastewater_structure, BWREL_rel_wastewater_structure_text_wastewater_structure, accessibility_REL, bedding_encasement_REL, connection_type_REL, financing_REL, fk_dataowner_REL, fk_main_cover_REL, fk_main_wastewater_node_REL, fk_operator_REL, fk_owner_REL, fk_provider_REL, function_hierarchic_REL, function_hydraulic_REL, renovation_necessity_REL, rv_construction_type_REL, status_REL, structure_condition_REL, usage_current_REL, usage_planned_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.CANALISATION",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.CANALISATION ---
        # ET.SubElement(e, "LIT_DE_POSE").text = row.REPLACE_ME
        # ET.SubElement(e, "FONCTION_HIERARCHIQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "FONCTION_HYDRAULIQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "GENRE_UTILISATION_PREVU").text = row.REPLACE_ME
        # ET.SubElement(e, "GENRE_UTILISATION_ACTUEL").text = row.REPLACE_ME
        # ET.SubElement(e, "L_TUYAU").text = row.REPLACE_ME
        # ET.SubElement(e, "INTERVALLE_CURAGE").text = row.REPLACE_ME
        # ET.SubElement(e, "RACCORDEMENT").text = row.REPLACE_ME

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

    print("Exporting QGEP.manhole -> SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD")
    for row in session.query(QGEP.manhole):
        # AVAILABLE FIELDS FROM wastewater_structure
        # _bottom_label, _cover_label, _depth, _function_hierarchic, _input_label, _label, _output_label, _usage_current, accessibility, contract_section, detail_geometry_geometry, financing, fk_dataowner, fk_main_cover, fk_main_wastewater_node, fk_operator, fk_owner, fk_provider, gross_costs, identifier, inspection_interval, last_modification, location_name, records, remark, renovation_necessity, replacement_value, rv_base_year, rv_construction_type, status, structure_condition, subsidies, year_of_construction, year_of_replacement
        # AVAILABLE FIELDS FROM manhole
        # _orientation, dimension1, dimension2, function, material, obj_id, surface_inflow
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_oorel_od_discharge_point_wastewater_structure, BWREL_oorel_od_infiltration_installation_wastewater_structure, BWREL_oorel_od_special_structure_wastewater_structure, BWREL_oorel_od_wwtp_structure_wastewater_structure, BWREL_rel_maintenance_event_wastewater_structure_wastewater_structure, BWREL_rel_measuring_point_wastewater_structure, BWREL_rel_mechanical_pretreatment_wastewater_structure, BWREL_rel_structure_part_wastewater_structure, BWREL_rel_symbol_wastewater_structure, BWREL_rel_text_wastewater_structure, BWREL_rel_wastewater_networkelement_wastewater_structure, BWREL_rel_wastewater_structure_symbol_wastewater_structure, BWREL_rel_wastewater_structure_text_wastewater_structure, REL_fkey_vl_manhole_function, REL_fkey_vl_manhole_material, REL_fkey_vl_manhole_surface_inflow, REL_fkey_vl_wastewater_structure_accessibility, REL_fkey_vl_wastewater_structure_financing, REL_fkey_vl_wastewater_structure_renovation_necessity, REL_fkey_vl_wastewater_structure_rv_construction_type, REL_fkey_vl_wastewater_structure_status, REL_fkey_vl_wastewater_structure_structure_condition, REL_rel_od_wastewater_structure_fk_dataowner, REL_rel_od_wastewater_structure_fk_dataprovider, REL_rel_wastewater_structure_cover, REL_rel_wastewater_structure_main_wastewater_node, REL_rel_wastewater_structure_operator, REL_rel_wastewater_structure_owner

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD",
            {"TID": row.obj_id},
        )
        # FIELDS TO MAP TO SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD

        # --- SIA405_EAUX_USEES_2015.CHAMBRE_STANDARD ---
        ET.SubElement(e, "DIMENSION1").text = str(row.dimension1)
        ET.SubElement(e, "DIMENSION2").text = str(row.dimension2)
        ET.SubElement(e, "FONCTION").text = row.function_REL.value_fr if row.function_REL else ""
        ET.SubElement(e, "MATERIAU").text = row.material_REL.value_fr if row.material_REL else ""
        ET.SubElement(e, "ARRIVEE_EAUX_SUP").text = str(row.surface_inflow)

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

    print("Exporting QGEP.discharge_point -> SIA405_EAUX_USEES_2015.EXUTOIRE")
    for row in session.query(QGEP.discharge_point):
        # AVAILABLE FIELDS FROM discharge_point
        # fk_sector_water_body, highwater_level, obj_id, relevance, terrain_level, upper_elevation, waterlevel_hydraulic
        # AVAILABLE FIELDS FROM _relations_
        # fk_sector_water_body_REL, obj_id_REL, relevance_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.EXUTOIRE",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.EXUTOIRE ---
        # ET.SubElement(e, "COTE_CRUE").text = row.REPLACE_ME
        # ET.SubElement(e, "SIGNIFIANCE").text = row.REPLACE_ME
        # ET.SubElement(e, "COTE_TERRAIN").text = row.REPLACE_ME
        # ET.SubElement(e, "NIVEAU_EAU_HYDRAULIQUE").text = row.REPLACE_ME

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

    print("Exporting QGEP.special_structure -> SIA405_EAUX_USEES_2015.OUVRAGE_SPECIAL")
    for row in session.query(QGEP.special_structure):
        # AVAILABLE FIELDS FROM special_structure
        # bypass, emergency_spillway, function, obj_id, stormwater_tank_arrangement, upper_elevation
        # AVAILABLE FIELDS FROM _relations_
        # bypass_REL, emergency_spillway_REL, function_REL, obj_id_REL, stormwater_tank_arrangement_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.OUVRAGE_SPECIAL",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.OUVRAGE_SPECIAL ---
        # ET.SubElement(e, "BYPASS").text = row.REPLACE_ME
        # ET.SubElement(e, "FONCTION").text = row.REPLACE_ME
        # ET.SubElement(e, "TROP_PLEIN_DE_SECOURS").text = row.REPLACE_ME
        # ET.SubElement(e, "BEP_DISPOSITION").text = row.REPLACE_ME

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

    print("Exporting QGEP.infiltration_installation -> SIA405_EAUX_USEES_2015.INSTALLATION_INFILTRATION")
    for row in session.query(QGEP.infiltration_installation):
        # AVAILABLE FIELDS FROM infiltration_installation
        # absorption_capacity, defects, dimension1, dimension2, distance_to_aquifer, effective_area, emergency_spillway, fk_aquifier, kind, labeling, obj_id, seepage_utilization, upper_elevation, vehicle_access, watertightness
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_rel_mechanical_pretreatment_infiltration_installation, BWREL_rel_retention_body_infiltration_installation, defects_REL, emergency_spillway_REL, fk_aquifier_REL, kind_REL, labeling_REL, obj_id_REL, seepage_utilization_REL, vehicle_access_REL, watertightness_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.INSTALLATION_INFILTRATION",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.INSTALLATION_INFILTRATION ---
        # ET.SubElement(e, "GENRE").text = row.REPLACE_ME
        # ET.SubElement(e, "SIGNALISATION").text = row.REPLACE_ME
        # ET.SubElement(e, "DIMENSION1").text = row.REPLACE_ME
        # ET.SubElement(e, "DIMENSION2").text = row.REPLACE_ME
        # ET.SubElement(e, "DISTANCE_AQUIFERE").text = row.REPLACE_ME
        # ET.SubElement(e, "LACUNES").text = row.REPLACE_ME
        # ET.SubElement(e, "TROP_PLEIN_DE_SECOURS").text = row.REPLACE_ME
        # ET.SubElement(e, "VEHICULE_D_ASPIRATION").text = row.REPLACE_ME
        # ET.SubElement(e, "CAPACITE_ABSORPTION_SOL").text = row.REPLACE_ME
        # ET.SubElement(e, "EAU_INFILTRATION").text = row.REPLACE_ME
        # ET.SubElement(e, "ETANCHEITE").text = row.REPLACE_ME
        # ET.SubElement(e, "SURFACE_UTILE").text = row.REPLACE_ME

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

    print("Exporting QGEP.pipe_profile -> SIA405_EAUX_USEES_2015.PROFIL_TUYAU")
    for row in session.query(QGEP.pipe_profile):
        # AVAILABLE FIELDS FROM pipe_profile
        # fk_dataowner, fk_provider, height_width_ratio, identifier, last_modification, obj_id, profile_type, remark
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_rel_profile_geometry_pipe_profile, BWREL_rel_reach_pipe_profile, fk_dataowner_REL, fk_provider_REL, profile_type_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.PROFIL_TUYAU",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.PROFIL_TUYAU ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME
        # ET.SubElement(e, "RAPPORT_HAUTEUR_LARGEUR").text = row.REPLACE_ME
        # ET.SubElement(e, "TYPE_PROFIL").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.wastewater_networkelement -> SIA405_EAUX_USEES_2015.ELEMENT_RESEAU_EVACUATION")
    for row in session.query(QGEP.wastewater_networkelement):
        # AVAILABLE FIELDS FROM wastewater_networkelement
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, obj_id, remark
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_rel_catchment_area_wastewater_networkelement_rw_current, BWREL_rel_catchment_area_wastewater_networkelement_rw_planned, BWREL_rel_catchment_area_wastewater_networkelement_ww_current, BWREL_rel_catchment_area_wastewater_networkelement_ww_planned, BWREL_rel_connection_object_wastewater_networkelement, BWREL_rel_reach_point_wastewater_networkelement, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.ELEMENT_RESEAU_EVACUATION",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.ELEMENT_RESEAU_EVACUATION ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.reach_point -> SIA405_EAUX_USEES_2015.POINT_TRONCON")
    for row in session.query(QGEP.reach_point):
        # AVAILABLE FIELDS FROM reach_point
        # elevation_accuracy, fk_dataowner, fk_provider, fk_wastewater_networkelement, identifier, last_modification, level, obj_id, outlet_shape, position_of_connection, remark, situation_geometry
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_rel_examination_reach_point, BWREL_rel_reach_reach_point_from, BWREL_rel_reach_reach_point_to, elevation_accuracy_REL, fk_dataowner_REL, fk_provider_REL, fk_wastewater_networkelement_REL, outlet_shape_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.POINT_TRONCON",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.POINT_TRONCON ---
        # ET.SubElement(e, "FORME_SORTIE").text = row.REPLACE_ME
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME
        # ET.SubElement(e, "PRECISION_ALTIMETRIQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "COTE").text = row.REPLACE_ME
        # ET.SubElement(e, "SITUATION").text = row.REPLACE_ME
        # ET.SubElement(e, "SITUATION_POINT_RACCORD").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.wastewater_node -> SIA405_EAUX_USEES_2015.NOEUD_RESEAU")
    for row in session.query(QGEP.wastewater_node):
        # AVAILABLE FIELDS FROM wastewater_networkelement
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark
        # AVAILABLE FIELDS FROM wastewater_node
        # backflow_level, bottom_level, fk_hydr_geometry, obj_id, situation_geometry
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_rel_catchment_area_wastewater_networkelement_rw_current, BWREL_rel_catchment_area_wastewater_networkelement_rw_planned, BWREL_rel_catchment_area_wastewater_networkelement_ww_current, BWREL_rel_catchment_area_wastewater_networkelement_ww_planned, BWREL_rel_connection_object_wastewater_networkelement, BWREL_rel_hydraulic_char_data_wastewater_node, BWREL_rel_overflow_overflow_to, BWREL_rel_overflow_wastewater_node, BWREL_rel_reach_point_wastewater_networkelement, BWREL_rel_throttle_shut_off_unit_wastewater_node, BWREL_rel_wastewater_structure_main_wastewater_node, fk_dataowner_REL, fk_hydr_geometry_REL, fk_provider_REL, fk_wastewater_structure_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.NOEUD_RESEAU",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.NOEUD_RESEAU ---
        # ET.SubElement(e, "SITUATION").text = row.REPLACE_ME
        # ET.SubElement(e, "COTE_REFOULEMENT").text = row.REPLACE_ME
        # ET.SubElement(e, "COTE_RADIER").text = row.REPLACE_ME

        # --- SIA405_EAUX_USEES_2015.ELEMENT_RESEAU_EVACUATION ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.reach -> SIA405_EAUX_USEES_2015.TRONCON")
    for row in session.query(QGEP.reach):
        # AVAILABLE FIELDS FROM wastewater_networkelement
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, remark
        # AVAILABLE FIELDS FROM reach
        # clear_height, coefficient_of_friction, elevation_determination, fk_pipe_profile, fk_reach_point_from, fk_reach_point_to, horizontal_positioning, inside_coating, length_effective, material, obj_id, progression_geometry, reliner_material, reliner_nominal_size, relining_construction, relining_kind, ring_stiffness, slope_building_plan, wall_roughness
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_rel_catchment_area_wastewater_networkelement_rw_current, BWREL_rel_catchment_area_wastewater_networkelement_rw_planned, BWREL_rel_catchment_area_wastewater_networkelement_ww_current, BWREL_rel_catchment_area_wastewater_networkelement_ww_planned, BWREL_rel_connection_object_wastewater_networkelement, BWREL_rel_reach_point_wastewater_networkelement, BWREL_rel_reach_text_reach, BWREL_rel_text_reach, elevation_determination_REL, fk_dataowner_REL, fk_pipe_profile_REL, fk_provider_REL, fk_reach_point_from_REL, fk_reach_point_to_REL, fk_wastewater_structure_REL, horizontal_positioning_REL, inside_coating_REL, material_REL, reliner_material_REL, relining_construction_REL, relining_kind_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.TRONCON",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.TRONCON ---
        # ET.SubElement(e, "PROTECTION_INTERIEURE").text = row.REPLACE_ME
        # ET.SubElement(e, "L_EFFECTIVE").text = row.REPLACE_ME
        # ET.SubElement(e, "DETERMINATION_PLANIMETRIQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "HAUTEUR_MAX_PROFIL").text = row.REPLACE_ME
        ET.SubElement(e, "MATERIAU").text = row.material_REL.value_fr
        # ET.SubElement(e, "PENTE_PLAN").text = row.REPLACE_ME
        # ET.SubElement(e, "K_STRICKLER").text = row.REPLACE_ME
        # ET.SubElement(e, "RELINING_GENRE").text = row.REPLACE_ME
        # ET.SubElement(e, "RELINING_TECHNIQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "RELINING_MATERIAUX").text = row.REPLACE_ME
        # ET.SubElement(e, "RELINER_DIAMETRE_NOMINALE").text = row.REPLACE_ME
        # ET.SubElement(e, "RIGIDITE_ANNULAIRE").text = row.REPLACE_ME
        # ET.SubElement(e, "TRACE").text = row.REPLACE_ME
        # ET.SubElement(e, "K_COLEBROOK").text = row.REPLACE_ME

        # --- SIA405_EAUX_USEES_2015.ELEMENT_RESEAU_EVACUATION ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.structure_part -> SIA405_EAUX_USEES_2015.ELEMENT_OUVRAGE")
    for row in session.query(QGEP.structure_part):
        # AVAILABLE FIELDS FROM structure_part
        # fk_dataowner, fk_provider, fk_wastewater_structure, identifier, last_modification, obj_id, remark, renovation_demand
        # AVAILABLE FIELDS FROM _relations_
        # BWREL_oorel_od_access_aid_structure_part, BWREL_oorel_od_backflow_prevention_structure_part, BWREL_oorel_od_benching_structure_part, BWREL_oorel_od_cover_structure_part, BWREL_oorel_od_dryweather_downspout_structure_part, BWREL_oorel_od_dryweather_flume_structure_part, BWREL_oorel_od_electric_equipment_structure_part, BWREL_oorel_od_electromechanical_equipment_structure_part, BWREL_oorel_od_solids_retention_structure_part, BWREL_oorel_od_tank_cleaning_structure_part, BWREL_oorel_od_tank_emptying_structure_part, fk_dataowner_REL, fk_provider_REL, fk_wastewater_structure_REL, renovation_demand_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.ELEMENT_OUVRAGE",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.ELEMENT_OUVRAGE ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME
        # ET.SubElement(e, "REMISE_EN_ETAT").text = row.REPLACE_ME

        # --- SIA405_Base_f.SIA405_BaseClass ---
        # ET.SubElement(e, "OBJ_ID").text = row.REPLACE_ME
        # ET.SubElement(e, "METAATTRIBUTS").text = row.REPLACE_ME
        print(".", end="")
    print("done")

    print("Exporting QGEP.dryweather_downspout -> SIA405_EAUX_USEES_2015.TUYAU_CHUTE")
    for row in session.query(QGEP.dryweather_downspout):
        # AVAILABLE FIELDS FROM dryweather_downspout
        # diameter, obj_id
        # AVAILABLE FIELDS FROM _relations_
        # obj_id_REL

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.TUYAU_CHUTE",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.TUYAU_CHUTE ---
        # ET.SubElement(e, "DIAMETRE").text = row.REPLACE_ME

        # --- SIA405_EAUX_USEES_2015.ELEMENT_OUVRAGE ---
        # ET.SubElement(e, "REMARQUE").text = row.REPLACE_ME
        # ET.SubElement(e, "DESIGNATION").text = row.REPLACE_ME
        # ET.SubElement(e, "REMISE_EN_ETAT").text = row.REPLACE_ME

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
        # BWREL_rel_wastewater_structure_cover, REL_fkey_vl_cover_cover_shape, REL_fkey_vl_cover_fastening, REL_fkey_vl_cover_material, REL_fkey_vl_cover_positional_accuracy, REL_fkey_vl_cover_sludge_bucket, REL_fkey_vl_cover_venting, REL_oorel_od_cover_structure_part

        e = ET.SubElement(
            datasection,
            "SIA405_EAUX_USEES_2015.COUVERCLE",
            {"TID": row.obj_id},
        )

        # --- SIA405_EAUX_USEES_2015.COUVERCLE ---
        # ET.SubElement(e, "FORME_COUVERCLE").text = row.REPLACE_ME
        ET.SubElement(e, "DIAMETRE").text = str(row.diameter)
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

    with open('output.xml', 'w') as handler:
        handler.write(xml.dom.minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml())
