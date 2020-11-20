#!/bin/bash

# Create schema fernwirkkabel
java -jar ili2pg-4.1.0.jar --schemaimport --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema fernwirkkabel --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol SIA405_Fernwirkkabel_2012_LV95.ili

# Import fernwirkkabel data
java -jar ili2pg-4.1.0.jar --import --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema fernwirkkabel --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol --dataset horw horw_fww.XTF

# Create schema schutzrohr
java -jar ili2pg-4.1.0.jar --schemaimport --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema schutzrohr --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol SIA405_Schutzrohr_2012_LV95.ili

# Import schutzrohr data
java -jar ili2pg-4.1.0.jar --import --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema schutzrohr --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol --dataset horw horw_srw.XTF

# Create schema wasser
java -jar ili2pg-4.1.0.jar --schemaimport --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema wasser --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol SIA405_Wasser_2015_LV95.ili

# Import wasser data
java -jar ili2pg-4.1.0.jar --import --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema wasser --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol --dataset horw horw_was.XTF

# Create schema abwasser
java -jar ili2pg-4.1.0.jar --schemaimport --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema wasser --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol SIA405_Abwasser_2015_LV95.ili
