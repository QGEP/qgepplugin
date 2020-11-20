for n in $(java -jar ilivalidator-1.11.1.jar a_horw_abw.ITF 2>&1 | grep "already exists in" | cut -d ' ' -f 3 | sed 's/:*$//g' | sort -n -r); do
    sed -i "${n}d" a_horw_abw.ITF
done

java -jar ili2pg-4.1.0.jar --import --sqlEnableNull --dbhost postgis --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw_gemeindegis --dbschema abwasser --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol --dataset horw a_horw_abw.ITF

java -jar ili2pg-4.1.0.jar --import --sqlEnableNull --dbhost postgis --dbport 5432 --defaultSrsCode 2056 --dbdatabase horw_gemeindegis --dbschema abwasser --dbusr postgres --dbpwd postgres --disableValidation --skipReferenceErrors --skipPolygonBuildingErrors --createBasketCol --dataset horw a_horw_abw.ITF
