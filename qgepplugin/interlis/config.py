import os

PGHOST = '127.0.0.1'
PGDATABASE = 'qgep_prod'
PGUSER = 'postgres'
PGPASS = 'postgres'
PSQL = r'C:\OSGeo4W64\bin\psql'
ILI2PG = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\interlis\ili2pg-4.4.6-20210122.110757-4-bindist\ili2pg-4.4.6-SNAPSHOT.jar'
ILIVALIDATOR = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\interlis\ilivalidator-1.11.9\ilivalidator-1.11.9.jar'
ILI_FOLDER = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\interlis\ili'
DATA_FOLDER = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\interlis\data'

BASE_ILI_MODEL = os.path.join(ILI_FOLDER, 'Base_d-20181005.ili')
BASE_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'Base_f-20181005.ili')
BASE_SIA_ILI_MODEL = os.path.join(ILI_FOLDER, 'SIA405_Base_d-20181005.ili')
BASE_SIA_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'SIA405_Base_f-20181005.ili')

QGEP_SCHEMA = 'qgep_od'
ABWASSER_SCHEMA = 'pg2ili_abwasser'
ABWASSER_ILI_MODEL = os.path.join(ILI_FOLDER, 'VSA_KEK_2019_2_d_LV95-20210120.ili')
ABWASSER_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'VSA_KEK_2019_2_d_LV95-20210120.ili')  # TODO : french version doesn't exist yet
ABWASSER_ILI_MODEL_NAME = 'VSA_KEK_2019_LV95'

QWAT_SCHEMA = 'qwat_od'
WASSER_SCHEMA = 'pg2ili_wasser'
WASSER_ILI_MODEL = os.path.join(ILI_FOLDER, 'SIA405_Wasser_2015_2_d-20181005.ili')
WASSER_ILI_MODEL_FR = os.path.join(ILI_FOLDER, 'SIA405_Eaux_2015_2_f-20181005.ili')
WASSER_ILI_MODEL_NAME = 'SIA405_WASSER_2015_LV95'
WASSER_ILI_MODEL_NAME_FR = 'SIA405_EAUX_2015_LV95'
