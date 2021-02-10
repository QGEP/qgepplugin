# Interlis / QGEP oddities

## QGEP

- `qgep_od.file.fk_data_media` doesn't have a FK constraint to `qgep_od.data_media.obj_id`

## SIA405_Abwasser

- `Deckel.Fabrikat` looks like a typo, shouldn't it be `Deckel.Fabrikant` ? (comment is `Name der Herstellerfirma`)

## QGEP-SIA405 differences

- `qgep_od.maintenance_event` has a N-M relation to `qgep_od.wastewater_structure`, making fields like `inspection.inspected_length` or `damage.distance` ambigous. Corresponding SIA405_Abwasser classes have a N-1 relation instead, which looks like a better fit.



