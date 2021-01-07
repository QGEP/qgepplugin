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
            {"TID": QGEP.manhole.make_tid(row.obj_id)},
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


    # Exporting QGEP.reach
    for row in session.query(QGEP.reach):
        e = ET.SubElement(
            datasection,
            'SIA405_ABWASSER_2015_LV95.SIA405_Abwasser.Haltung',
            {"TID": QGEP.reach.make_tid(row.obj_id)},
        )

        ET.SubElement(e, "OBJ_ID").text = QGEP.manhole.make_tid(row.obj_id)
        ET.SubElement(e, "Bezeichnung").text = row.identifier
        ET.SubElement(e, "Material").text = str(row.material)
        

    with open('output.xml', 'w') as handler:
        handler.write(xml.dom.minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml())
