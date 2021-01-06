import os

PGHOST = '127.0.0.1'
PGDATABASE = 'qgep_prod'
PGUSER = 'postgres'
PGPASS = 'postgres'
PSQL = r'C:\OSGeo4W64\bin\psql'
ILI2PG = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\interlis\ili2pg-4.4.2\ili2pg-4.4.2.jar'
ILI_FOLDER = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\interlis\ili'

BASE_ILI_MODEL = os.path.join(ILI_FOLDER, 'Base_d-20181005.ili')
BASE_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'Base_f-20181005.ili')
BASE_SIA_ILI_MODEL = os.path.join(ILI_FOLDER, 'SIA405_Base_d-20181005.ili')
BASE_SIA_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'SIA405_Base_f-20181005.ili')

QGEP_SCHEMA = 'qgep_od'
ABWASSER_SCHEMA = 'pg2ili_abwasser'
ABWASSER_ILI_MODEL = os.path.join(ILI_FOLDER, 'SIA405_Abwasser_2015_2_d-20180417.ili')
ABWASSER_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'SIA405_Eaux_usees_2015_2_f-20180417.ili')
ABWASSER_ILI_MODEL_NAME = 'SIA405_ABWASSER_2015_LV95'

QWAT_SCHEMA = 'qwat_od'
WASSER_SCHEMA = 'pg2ili_wasser'
WASSER_ILI_MODEL = os.path.join(ILI_FOLDER, 'SIA405_Wasser_2015_2_d-20181005.ili')
WASSER_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'SIA405_Eaux_2015_2_f-20181005.ili')
WASSER_ILI_MODEL_NAME = 'SIA405_WASSER_2015_LV95'
WASSER_ILI_MODEL_NAME_FR = 'SIA405_EAUX_2015_LV95'
