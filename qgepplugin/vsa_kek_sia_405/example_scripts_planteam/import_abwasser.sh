#!/bin/bash

export ILI2DB_PATH=/home/mkuhn/app/ili2pg-4.3.2.jar
# /home/mkuhn/.local/share/QGIS/QGIS3/profiles/default/python/plugins/QgisModelBaker/libili2db/bin/ili2pg-4.1.0/ili2pg-4.1.0.jar

export PGPASS=postgres
# psql -U postgres -h 212.59.169.130 -d horw -c "DROP SCHEMA abwasser11 CASCADE"

java -jar $ILI2DB_PATH --schemaimport --sqlEnableNull --dbhost 212.59.169.130 --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema abwasser11 --dbusr postgres --dbpwd fantagis --createBasketCol --coalesceCatalogueRef --createEnumTabs --createNumChecks --coalesceMultiSurface --coalesceMultiLine --coalesceMultiPoint --coalesceArray --beautifyEnumDispName --createUnique --createGeomIdx --createFk --createFkIdx --createMetaInfo --expandMultilingual --importTid --smart1Inheritance --strokeArcs SIA405_Abwasser_2015_LV95.ili

# Create schema abwasser
# java -jar $ILI2DB_PATH --schemaimport --sqlEnableNull --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema abwasser --dbusr postgres --dbpwd postgres --createBasketCol \
# --coalesceCatalogueRef \
# --createEnumTabs \
# --createNumChecks \
# --coalesceMultiSurface \
# --coalesceMultiLine \
# --coalesceMultiPoint \
# --coalesceArray \
# --beautifyEnumDispName \
# --createUnique \
# --createGeomIdx \
# --createFk \
# --createFkIdx \
# --createMetaInfo \
# --expandMultilingual \
# --importTid \
# --smart1Inheritance \
# --strokeArcs SIA405_Abwasser_2015_LV95.ili

java -jar $ILI2DB_PATH --import --dbhost localhost --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw --dbschema abwasser --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors horw_abw_mkuhn.XTF
