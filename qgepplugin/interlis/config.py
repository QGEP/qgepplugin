import os

BASE = os.path.dirname(__file__)

PGHOST = "127.0.0.1"
PGDATABASE = "qgep_prod"
PGUSER = "postgres"
PGPASS = "postgres"
JAVA = r"java"
ILI2PG = os.path.join(BASE, 'bin', 'ili2pg-4.4.6-20210122.110757-4-bindist', 'ili2pg-4.4.6-SNAPSHOT.jar')
ILIVALIDATOR = os.path.join(BASE, 'bin', 'ilivalidator-1.11.9', 'ilivalidator-1.11.9.jar')
ILI_FOLDER = os.path.join(BASE, "ili")
DATA_FOLDER = os.path.join(BASE, "data")

QGEP_SCHEMA = "qgep_od"
ABWASSER_SCHEMA = "pg2ili_abwasser"
ABWASSER_ILI_MODEL = os.path.join(ILI_FOLDER, "VSA_KEK_2019_2_d_LV95-20210120.ili")
ABWASSER_ILI_MODEL_NAME = "VSA_KEK_2019_LV95"

QWAT_SCHEMA = "qwat_od"
WASSER_SCHEMA = "pg2ili_wasser"
WASSER_ILI_MODEL = os.path.join(ILI_FOLDER, "SIA405_Wasser_2015_2_d-20181005.ili")
WASSER_ILI_MODEL_NAME = "SIA405_WASSER_2015_LV95"
