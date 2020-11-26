# VSA-KEK / SIA 405 import/export

WIP implementation for VSA-KEK/SIA 405 import/export

More information on https://github.com/QGEP/QGEP/issues/600

## Progress

### Creating the Interlis datamodel using ili2pg

Able to create datamodel by adapting `example_scripts_planteam/import_abwasser.sh` (from the planteam project) like this :

```
java -jar qgepplugin\qgepplugin\vsa_kek_sia_405\ili2pg-4.4.2\ili2pg-4.4.2.jar --schemaimport --sqlEnableNull --dbhost 127.0.0.1 --dbport 5432 --defaultSrsCode 2056 --dbdatabase qgep_test_ili --dbschema test5 --dbusr postgres --dbpwd postgres --createBasketCol --coalesceCatalogueRef --createEnumTabs --createNumChecks --coalesceMultiSurface --coalesceMultiLine --coalesceMultiPoint --coalesceArray --beautifyEnumDispName --createUnique --createGeomIdx --createFk --createFkIdx --createMetaInfo --expandMultilingual --importTid --smart1Inheritance --strokeArcs qgepplugin\qgepplugin\vsa_kek_sia_405\example_scripts_planteam\SIA405_Abwasser_2015_LV95.ili
```

But it seems to be using an old `SIA405_Abwasser_2015_LV95.ili` is obsolete (`VERSION "14.09.2015"` in the file).

The same command with `SIA405_Abwasser_2015_2_d-20180417.ili` retrieved from `https://www.sia.ch/de/dienstleistungen/sia-norm/geodaten/` fails with 

```
[...]
Info: create table structure, if not existing...
java.lang.NullPointerException
```

And with `SIA405_Abwasser_3D_2015_2_d-20180417.ili`, il fails with :

```
[...]
Info: ilifile <sia405_interlis_files\SIA405_Abwasser_3D_2015_2_d-20180417.ili>
Error: sia405_interlis_files\SIA405_Abwasser_3D_2015_2_d-20180417.ili:31:SIA405_ABWASSER_3D_2015.SIA405_Abwasser_3D must be declared as ABSTRACT. One of its elements (Abwasserbauwerk) is abstract.
Error: sia405_interlis_files\SIA405_Abwasser_3D_2015_2_d-20180417.ili:31:SIA405_ABWASSER_3D_2015.SIA405_Abwasser_3D must be declared as ABSTRACT. One of its elements (Abwassernetzelement) is abstract.
Error: sia405_interlis_files\SIA405_Abwasser_3D_2015_2_d-20180417.ili:31:SIA405_ABWASSER_3D_2015.SIA405_Abwasser_3D must be declared as ABSTRACT. One of its elements (BauwerksTeil) is abstract.
Error: sia405_interlis_files\SIA405_Abwasser_3D_2015_2_d-20180417.ili:276:SIA405_ABWASSER_3D_2015_LV95.SIA405_Abwasser_3D must be declared as ABSTRACT. One of its elements (Abwasserbauwerk) is abstract.
Error: sia405_interlis_files\SIA405_Abwasser_3D_2015_2_d-20180417.ili:276:SIA405_ABWASSER_3D_2015_LV95.SIA405_Abwasser_3D must be declared as ABSTRACT. One of its elements (Abwassernetzelement) is abstract.
Error: sia405_interlis_files\SIA405_Abwasser_3D_2015_2_d-20180417.ili:276:SIA405_ABWASSER_3D_2015_LV95.SIA405_Abwasser_3D must be declared as ABSTRACT. One of its elements (BauwerksTeil) is abstract.
compiler failed
```

#### Questions 

- [ ] Is `https://www.sia.ch/de/dienstleistungen/sia-norm/geodaten/` the correct place from which to retrieve the current model ?
- [ ] From those ili models, which one exactly do we want to use ? `SIA405_Abwasser_3D_2015_2_d-20180417.ili` or `SIA405_Abwasser_2015_2_d-20180417.ili` ?
- [ ] Any idea of what reason could make ili2pg fail with these newer releases, and even better, how to fix this ? Does it work for you ?


### Trying to replicate Stefan's workflow

Able to create with latest datamodel with older ili2pg (3.12.2 instead of 4.x)
```
# create database qgep_test_ili
# run CREATE EXTENSION postgis;
java -jar qgepplugin\qgepplugin\vsa_kek_sia_405\ili2pg-3.12.2\ili2pg-3.12.2.jar --schemaimport --sqlEnableNull --dbhost 127.0.0.1 --dbport 5432 --defaultSrsCode 2056 --dbdatabase qgep_test_ili --dbschema test5 --dbusr postgres --dbpwd postgres --createBasketCol --coalesceCatalogueRef --createEnumTabs --createNumChecks --coalesceMultiSurface --coalesceMultiLine --coalesceMultiPoint --coalesceArray --beautifyEnumDispName --createUnique --createGeomIdx --createFk --createFkIdx --createMetaInfo --expandMultilingual --importTid --smart1Inheritance --strokeArcs --noSmartMapping qgepplugin\qgepplugin\vsa_kek_sia_405\sia405_interlis_files\SIA405_Abwasser_2015_2_d-20180417.ili
```

In french
```
# create database qgep_test_ili
# run CREATE EXTENSION postgis;
java -jar qgepplugin\qgepplugin\vsa_kek_sia_405\ili2pg-3.12.2\ili2pg-3.12.2.jar --schemaimport --sqlEnableNull --dbhost 127.0.0.1 --dbport 5432 --defaultSrsCode 2056 --dbdatabase qgep_test_ili --dbschema tetfr --dbusr postgres --dbpwd postgres --createBasketCol --coalesceCatalogueRef --createEnumTabs --createNumChecks --coalesceMultiSurface --coalesceMultiLine --coalesceMultiPoint --coalesceArray --beautifyEnumDispName --createUnique --createGeomIdx --createFk --createFkIdx --createMetaInfo --expandMultilingual --importTid --smart1Inheritance --strokeArcs --noSmartMapping qgepplugin\qgepplugin\vsa_kek_sia_405\sia405_interlis_files\SIA405_Eaux_usees_2015_2_f-20180417.ili
```


We'll continue with 3.12.2 for now.

