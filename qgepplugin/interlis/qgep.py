import psycopg2
import os
import sys
import collections

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from geoalchemy2 import Geometry

# from . import utils
# from . import config
import utils
import config

utils.setup_test_db()

# CREATE TEMPORARY SCHEMA
utils.create_ili_schema(config.QGEP_ILI_SCHEMA, config.QGEP_ILI_MODEL)


engine = utils.create_engine()


###############################################
# QGEP datamodel
###############################################

QGEPManhole = utils.class_factory("manhole", ["wastewater_structure"], config.QGEP_SCHEMA)
utils.prepare(config.QGEP_SCHEMA, engine)

###############################################
# INTERLIS datamodel
###############################################

SIANormschacht = utils.class_factory("normschacht", [], config.QGEP_ILI_SCHEMA)
utils.prepare(config.QGEP_ILI_SCHEMA, engine)


###############################################
# Actual export
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

session = Session(engine)

print("Exporting manhole -> normschacht")
for row in session.query(QGEPManhole):
    session.add(
        SIANormschacht(
            bezeichnung=row.identifier,
            t_ili_tid=row.obj_id,
            obj_id=row.obj_id,
            zugaenglichkeit=MAPPING['wastewater_structure']['accessibility'][row.accessibility],
            dimension1=min(4000, row.dimension1 or 0),
            dimension2=min(4000, row.dimension2 or 0),
            funktion=MAPPING['manhole']['function'][row.function],
        )
    )
    print(".", end="")
print("done !")

session.commit()

# EXPORT TEMPORARY SCHEMA
utils.export_ili_schema(config.QGEP_ILI_SCHEMA, config.QGEP_ILI_MODEL_NAME)


## TODO
# abwasserbauwerk_baulicherzustand
# abwasserbauwerk_betreiber_assoc
# abwasserbauwerk_eigentuemer_assoc
# abwasserbauwerk_finanzierung
# abwasserbauwerk_sanierungsbedarf
# abwasserbauwerk_symbol
# abwasserbauwerk_text
# abwasserbauwerk_wbw_bauart
# abwasserbauwerk_zugaenglichkeit
# abwasserknoten
# abwassernetzelement_abwasserbauwerk_assoc
# astatus
# bankett
# bankett_art
# bauwerksteil_instandstellung
# deckel
# deckel_deckelform
# deckel_entlueftung
# deckel_lagegenauigkeit
# deckel_material
# deckel_schlammeimer
# deckel_verschluss
# einleitstelle
# einleitstelle_relevanz
# einstiegshilfe
# einstiegshilfe_art
# halignment
# haltung
# haltung_alternativverlauf
# haltung_innenschutz
# haltung_lagebestimmung
# haltung_material
# haltung_nachhaltungspunkt_assoc
# haltung_reliner_art
# haltung_reliner_bautechnik
# haltung_reliner_material
# haltung_rohrprofil_assoc
# haltung_text
# haltung_vonhaltungspunkt_assoc
# haltungspunkt
# haltungspunkt_abwassernetzelement_assoc
# haltungspunkt_auslaufform
# haltungspunkt_hoehengenauigkeit
# kanal
# kanal_bettung_umhuellung
# kanal_funktionhierarchisch
# kanal_funktionhydraulisch
# kanal_nutzungsart_geplant
# kanal_nutzungsart_ist
# kanal_verbindungsart
# metaattribute
# normschacht_funktion
# normschacht_material
# normschacht_oberflaechenzulauf
# organisation
# organisation_teil_vonassoc
# plantyp
# rohrprofil
# rohrprofil_profiltyp
# sia4055_lv95sia405_abwasser_deckel_lagegenauigkeit
# sia4055_lv95sia405_abwasser_haltung_lagebestimmung
# sia4055_lv95sia405_abwasser_rohrprofil_profiltyp
# sia4055_lv95sia405_abwasser_spezialbauwerk_funktion
# sia4055_lv95sia405_bwssr_lk_kanal_funktionhierarchisch
# sia4055_lv95sia405_bwssr_lk_normschacht_funktion
# sia405_15_lv95sia405_abwassr_lk_abwasserbauwerk
# sia405_15_lv95sia405_abwassr_lk_abwasserbauwerk_text
# sia405_15_lv95sia405_abwassr_lk_abwasserbauwerk_textassoc
# sia405_15_lv95sia405_abwassr_lk_abwasserknoten
# sia405_15_lv95sia405_abwassr_lk_abwassernetzelement
# sia405_15_lv95sia405_abwassr_lk_deckel
# sia405_15_lv95sia405_abwassr_lk_einleitstelle
# sia405_15_lv95sia405_abwassr_lk_haltung
# sia405_15_lv95sia405_abwassr_lk_haltung_text
# sia405_15_lv95sia405_abwassr_lk_haltung_textassoc
# sia405_15_lv95sia405_abwassr_lk_haltungspunkt
# sia405_15_lv95sia405_abwassr_lk_kanal
# sia405_15_lv95sia405_abwassr_lk_normschacht
# sia405_15_lv95sia405_abwassr_lk_rohrprofil
# sia405_15_lv95sia405_abwassr_lk_spezialbauwerk
# sia405_15_lv95sia405_abwassr_lk_versickerungsanlage
# spezialbauwerk
# spezialbauwerk_bypass
# spezialbauwerk_funktion
# spezialbauwerk_notueberlauf
# spezialbauwerk_regenbecken_anordnung
# statuswerte
# t_ili2db_attrname
# t_ili2db_basket
# t_ili2db_classname
# t_ili2db_column_prop
# t_ili2db_dataset
# t_ili2db_inheritance
# t_ili2db_model
# t_ili2db_settings
# t_ili2db_table_prop
# t_ili2db_trafo
# trockenwetterfallrohr
# trockenwetterrinne
# trockenwetterrinne_material
# valignment
# versickerungsanlage
# versickerungsanlage_art
# versickerungsanlage_beschriftung
# versickerungsanlage_maengel
# versickerungsanlage_notueberlauf
# versickerungsanlage_saugwagen
# versickerungsanlage_versickerungswasser
# versickerungsanlage_wasserdichtheit

## IN PROGRESS
# normschacht <- manhole

## DONE
